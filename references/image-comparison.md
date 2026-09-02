# Reference-Image Comparison

Use exact pixel comparison only when reference and actual images represent the same content, viewport, dimensions, theme, fonts, rendering engine, scale/DPR, deterministic state, and color conditions. A difference is evidence, not automatically a defect.

## Helper usage

Use the bundled helper when Pillow is available:

```text
python scripts/compare_images.py --reference reference.png --actual actual.png --diff evidence/UI-001-diff.png --metrics evidence/UI-001-metrics.json --path-root <audit-bundle>
```

Options with semantic consequences:

- The default `--threshold 0` performs exact per-channel comparison. A nonzero threshold must be disclosed and means “within threshold,” not exact parity.
- Add `--background "#FFFFFF"` to compare rendered appearance after compositing transparent or translucent pixels on the declared opaque background.
- By default, mismatched embedded ICC profiles stop comparison. Add `--convert-to-srgb` to color-manage tagged inputs into sRGB; untagged inputs are explicitly assumed sRGB and that assumption is recorded.
- `--path-root` stores input paths relative to a declared bundle root when possible; otherwise metrics use basenames rather than absolute paths.
- Add `--overwrite` only when replacing previously generated evidence is intended.

The helper normalizes hidden RGB beneath fully transparent pixels for the visual comparison and retains raw encoded-pixel differences as separate diagnostic metrics. Without `--background`, semitransparent content is background-dependent and `definitive_visual_comparison` is false.

## Metrics and exit semantics

- Exit `0`: comparison completed. This does **not** mean parity; inspect `exact_match` and `within_threshold`.
- Exit `1`: operational or input error.
- Exit `2`: comparison precondition failed, such as dimensions or ICC profiles not matching.
- `changed_pixels`, `changed_pixel_ratio`, and `bounding_box` use the declared threshold and the visual comparison basis.
- Mean and maximum channel differences are unthresholded values from the visual comparison basis.
- `raw_encoded_*` metrics use threshold `0`, describe unnormalized RGBA differences, and can expose invisible encoding changes.
- ICC presence/hash, gamma, density metadata, profile policy, transparency, comparison basis, and any assumptions appear in the JSON.

Never silently resize mismatched inputs. Never call a color-profile mismatch definitive unless both images were intentionally converted into the declared common space.

## Interpretation

Inspect the generated diff visually and connect it to the Design Intent Contract before assigning severity. A one-pixel shift in a shared alignment system can be systemic; thousands of antialiasing pixels from an unmatched renderer can be irrelevant.

When environments cannot be matched, use overlays, landmarks, computed geometry, tokens, and visual judgment. Label the result diagnostic, not an objective reference failure.

