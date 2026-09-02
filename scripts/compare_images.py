#!/usr/bin/env python3
"""Compare two UI images without resizing and write privacy-safe diff evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageCms, UnidentifiedImageError
except ImportError as exc:  # pragma: no cover - depends on the host runtime
    raise SystemExit(
        "Pillow is required. Use the workspace dependency runtime when available; "
        "do not install packages without authorization."
    ) from exc


def threshold_value(raw: str) -> int:
    value = int(raw)
    if not 0 <= value <= 255:
        raise argparse.ArgumentTypeError("threshold must be between 0 and 255")
    return value


def background_value(raw: str) -> tuple[int, int, int]:
    value = raw.removeprefix("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("background must use #RRGGBB")
    try:
        return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("background must use #RRGGBB") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare reference and actual images at identical dimensions. "
            "Writes a transparent red difference mask and JSON metrics."
        )
    )
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--actual", required=True, type=Path)
    parser.add_argument("--diff", required=True, type=Path)
    parser.add_argument("--metrics", required=True, type=Path)
    parser.add_argument(
        "--threshold",
        type=threshold_value,
        default=0,
        help="Per-channel difference allowed before a pixel is marked changed (default: 0).",
    )
    parser.add_argument(
        "--background",
        type=background_value,
        help="Composite both images onto an opaque #RRGGBB background before comparison.",
    )
    parser.add_argument(
        "--convert-to-srgb",
        action="store_true",
        help=(
            "Color-manage tagged inputs into sRGB. Untagged inputs are explicitly "
            "assumed to be sRGB."
        ),
    )
    parser.add_argument(
        "--path-root",
        type=Path,
        help="Store input paths relative to this root when possible; otherwise use basenames.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing existing diff or metrics outputs.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes | None) -> str | None:
    return hashlib.sha256(value).hexdigest() if value else None


def resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def portable_path(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            pass
    return path.name


def validate_paths(args: argparse.Namespace) -> None:
    inputs = {resolved(args.reference), resolved(args.actual)}
    outputs = [resolved(args.diff), resolved(args.metrics)]
    if outputs[0] == outputs[1]:
        raise ValueError("--diff and --metrics must be different files")
    if any(output in inputs for output in outputs):
        raise ValueError("output paths must not overwrite either input image")
    if not args.overwrite:
        existing = [str(path) for path in outputs if path.exists()]
        if existing:
            raise FileExistsError(
                "output already exists; choose a new path or pass --overwrite: "
                + ", ".join(existing)
            )


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def json_metadata(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (tuple, list)):
        return [json_metadata(item) for item in value]
    return str(value)


def image_metadata(source: Image.Image) -> dict[str, object]:
    icc_profile = source.info.get("icc_profile")
    if not isinstance(icc_profile, bytes):
        icc_profile = None
    return {
        "dpi": json_metadata(source.info.get("dpi")),
        "gamma": json_metadata(source.info.get("gamma")),
        "icc_profile_present": icc_profile is not None,
        "icc_profile_sha256": sha256_bytes(icc_profile),
        "mode": source.mode,
        "size": list(source.size),
    }


def channel_means(histogram: list[int], pixel_count: int) -> list[float]:
    means: list[float] = []
    for channel_index in range(4):
        offset = channel_index * 256
        total = sum(value * histogram[offset + value] for value in range(256))
        means.append(round(total / pixel_count, 6))
    return means


def maximum_difference(histogram: list[int]) -> int:
    maximum = 0
    for channel_index in range(4):
        offset = channel_index * 256
        for value in range(255, -1, -1):
            if histogram[offset + value]:
                maximum = max(maximum, value)
                break
    return maximum


def difference_mask(raw_diff: Image.Image, threshold: int) -> Image.Image:
    masks = [
        channel.point(lambda value, limit=threshold: 255 if value > limit else 0)
        for channel in raw_diff.split()
    ]
    mask = masks[0]
    for channel_mask in masks[1:]:
        mask = ImageChops.lighter(mask, channel_mask)
    return mask


def difference_metrics(
    reference: Image.Image, actual: Image.Image, threshold: int
) -> tuple[dict[str, object], Image.Image]:
    raw_diff = ImageChops.difference(reference, actual)
    histogram = raw_diff.histogram()
    pixel_count = reference.size[0] * reference.size[1]
    means = channel_means(histogram, pixel_count)
    max_difference = maximum_difference(histogram)
    mask = difference_mask(raw_diff, threshold)
    changed_pixels = mask.histogram()[255]
    bounding_box = mask.getbbox()
    metrics: dict[str, object] = {
        "bounding_box": list(bounding_box) if bounding_box else None,
        "changed_pixel_ratio": round(changed_pixels / pixel_count, 9),
        "changed_pixels": changed_pixels,
        "exact_match": max_difference == 0,
        "max_channel_difference": max_difference,
        "mean_absolute_difference_by_channel_rgba": means,
        "mean_absolute_difference_rgba": round(sum(means) / 4, 6),
        "pixel_count": pixel_count,
        "within_threshold": changed_pixels == 0,
    }
    return metrics, mask


def alpha_summary(image: Image.Image) -> dict[str, int]:
    histogram = image.getchannel("A").histogram()
    return {
        "fully_transparent_pixels": histogram[0],
        "semitransparent_pixels": sum(histogram[1:255]),
        "opaque_pixels": histogram[255],
    }


def normalize_fully_transparent_rgb(image: Image.Image) -> Image.Image:
    red, green, blue, alpha = image.split()
    visible = alpha.point(lambda value: 0 if value == 0 else 255)
    zero = Image.new("L", image.size, 0)
    normalized = [Image.composite(channel, zero, visible) for channel in (red, green, blue)]
    return Image.merge("RGBA", (*normalized, alpha))


def composite_on_background(
    image: Image.Image, background: tuple[int, int, int]
) -> Image.Image:
    canvas = Image.new("RGBA", image.size, (*background, 255))
    return Image.alpha_composite(canvas, image)


def convert_source_to_srgb(source: Image.Image, icc_profile: bytes | None) -> Image.Image:
    rgba = source.convert("RGBA")
    alpha = rgba.getchannel("A")
    rgb = source.convert("RGB")
    if icc_profile:
        source_profile = ImageCms.ImageCmsProfile(BytesIO(icc_profile))
        destination_profile = ImageCms.createProfile("sRGB")
        rgb = ImageCms.profileToProfile(
            rgb,
            source_profile,
            destination_profile,
            outputMode="RGB",
        )
    rgb.putalpha(alpha)
    return rgb


def compare(args: argparse.Namespace) -> int:
    validate_paths(args)

    reference_path = resolved(args.reference)
    actual_path = resolved(args.actual)
    diff_path = resolved(args.diff)
    metrics_path = resolved(args.metrics)
    path_root = resolved(args.path_root) if args.path_root else None

    with Image.open(reference_path) as reference_source, Image.open(actual_path) as actual_source:
        reference_metadata = image_metadata(reference_source)
        actual_metadata = image_metadata(actual_source)
        reference_icc = reference_source.info.get("icc_profile")
        actual_icc = actual_source.info.get("icc_profile")
        reference_icc = reference_icc if isinstance(reference_icc, bytes) else None
        actual_icc = actual_icc if isinstance(actual_icc, bytes) else None

        profile_match = reference_icc == actual_icc
        gamma_match = reference_source.info.get("gamma") == actual_source.info.get("gamma")
        density_match = reference_source.info.get("dpi") == actual_source.info.get("dpi")

        base_metrics: dict[str, object] = {
            "actual": portable_path(actual_path, path_root),
            "actual_metadata": actual_metadata,
            "actual_sha256": sha256_file(actual_path),
            "color_profile_match": profile_match,
            "density_metadata_match": density_match,
            "dimension_match": reference_source.size == actual_source.size,
            "gamma_metadata_match": gamma_match,
            "reference": portable_path(reference_path, path_root),
            "reference_metadata": reference_metadata,
            "reference_sha256": sha256_file(reference_path),
            "threshold": args.threshold,
        }

        if reference_source.size != actual_source.size:
            base_metrics.update(
                {
                    "comparison_performed": False,
                    "definitive_visual_comparison": False,
                    "reason": "Image dimensions differ; inputs were not resized.",
                }
            )
            write_json(metrics_path, base_metrics)
            print(
                f"Dimension mismatch: reference={reference_source.size}, "
                f"actual={actual_source.size}. Metrics written to {metrics_path}",
                file=sys.stderr,
            )
            return 2

        if not profile_match and not args.convert_to_srgb:
            base_metrics.update(
                {
                    "color_profile_policy": "require-match",
                    "comparison_performed": False,
                    "definitive_visual_comparison": False,
                    "reason": (
                        "Embedded ICC profiles differ. Re-run with --convert-to-srgb "
                        "to compare in a declared common color space."
                    ),
                }
            )
            write_json(metrics_path, base_metrics)
            print(
                f"ICC profile mismatch. Metrics written to {metrics_path}",
                file=sys.stderr,
            )
            return 2

        raw_reference = reference_source.convert("RGBA")
        raw_actual = actual_source.convert("RGBA")
        raw_metrics, _ = difference_metrics(raw_reference, raw_actual, 0)

        assumptions: list[str] = []
        if args.convert_to_srgb:
            reference = convert_source_to_srgb(reference_source, reference_icc)
            actual = convert_source_to_srgb(actual_source, actual_icc)
            profile_policy = "converted-to-srgb"
            if reference_icc is None:
                assumptions.append("Reference image was untagged and assumed sRGB.")
            if actual_icc is None:
                assumptions.append("Actual image was untagged and assumed sRGB.")
        else:
            reference = raw_reference
            actual = raw_actual
            profile_policy = (
                "matching-embedded-profile" if reference_icc else "both-untagged"
            )
            if reference_icc is None:
                assumptions.append("Both images were untagged; encoded RGBA values were compared.")

        reference_alpha = alpha_summary(reference)
        actual_alpha = alpha_summary(actual)
        has_semitransparency = (
            reference_alpha["semitransparent_pixels"] > 0
            or actual_alpha["semitransparent_pixels"] > 0
        )

        if args.background is not None:
            reference_visual = composite_on_background(reference, args.background)
            actual_visual = composite_on_background(actual, args.background)
            background_label = "#" + "".join(
                f"{channel:02X}" for channel in args.background
            )
            comparison_basis = f"composited-rgba-on-{background_label}"
        else:
            reference_visual = normalize_fully_transparent_rgb(reference)
            actual_visual = normalize_fully_transparent_rgb(actual)
            background_label = None
            comparison_basis = "normalized-rgba"
            if has_semitransparency:
                assumptions.append(
                    "Semitransparent pixels are background-dependent; no comparison "
                    "background was declared."
                )

        visual_metrics, mask = difference_metrics(
            reference_visual, actual_visual, args.threshold
        )
        gamma_resolved = gamma_match or (
            reference_icc is not None and actual_icc is not None
        )
        definitive = gamma_resolved and (
            args.background is not None or not has_semitransparency
        )

        visualization = Image.new("RGBA", reference_source.size, (255, 32, 80, 0))
        visualization.putalpha(mask)
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        visualization.save(diff_path)

        metrics = {
            **base_metrics,
            **visual_metrics,
            "actual_alpha": actual_alpha,
            "assumptions": assumptions,
            "background": background_label,
            "color_profile_policy": profile_policy,
            "comparison_basis": comparison_basis,
            "comparison_performed": True,
            "converted_mode": "RGBA",
            "definitive_visual_comparison": definitive,
            "raw_encoded_bounding_box": raw_metrics["bounding_box"],
            "raw_encoded_changed_pixel_ratio": raw_metrics["changed_pixel_ratio"],
            "raw_encoded_changed_pixels": raw_metrics["changed_pixels"],
            "raw_encoded_exact_match": raw_metrics["exact_match"],
            "raw_encoded_max_channel_difference": raw_metrics[
                "max_channel_difference"
            ],
            "reference_alpha": reference_alpha,
            "transparent_rgb_normalized": True,
        }
        write_json(metrics_path, metrics)

    print(
        f"Comparison completed for {visual_metrics['pixel_count']} pixels: "
        f"{visual_metrics['changed_pixels']} changed above threshold {args.threshold}. "
        f"Inspect metrics for parity. Diff: {diff_path}. Metrics: {metrics_path}"
    )
    return 0


def main() -> int:
    args = parse_args()
    try:
        return compare(args)
    except (
        FileExistsError,
        ImageCms.PyCMSError,
        OSError,
        UnidentifiedImageError,
        ValueError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

