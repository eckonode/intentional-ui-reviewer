# Intentional UI Reviewer

Intentional UI Reviewer is a reusable Codex skill for evidence-backed UI/UX audits. It reviews live interfaces, screenshots, and design references for visual precision, interaction quality, accessibility, product coherence, and system consistency.

The skill draws on principles of purposeful, restrained, human-centered design without copying Apple’s visual identity. It distinguishes between a new design, a preservation-focused polish engagement, and an explicitly authorized redesign before recommending changes.

## What it reviews

- Product purpose, audience fit, information architecture, task efficiency, feedback, recovery, and trust
- Layout, grids, spacing, optical alignment, borders, radii, clipping, elevation, and responsive reflow
- Typography, copy, hierarchy, truncation, icons, imagery, color semantics, contrast, and themes
- Controls and their interaction states, including focus, pressed, selected, disabled, loading, validation, and error states
- Accessibility, keyboard use, zoom, reduced motion, RTL, high contrast, and applicable WCAG 2.2 criteria
- Perceived performance, layout shifts, motion continuity, and immediate feedback
- Reference parity using an optional Pillow-based image comparison helper

## Install

Copy this repository into your personal Codex skills directory so that `SKILL.md` is located at:

```text
$CODEX_HOME/skills/intentional-ui-reviewer/SKILL.md
```

Then invoke it explicitly with `$intentional-ui-reviewer` or ask Codex to perform a UI/UX audit.

Pillow is optional and is only required for `scripts/compare_images.py`.

## Outputs

The skill produces a chat summary and a saved audit bundle containing:

- `report.md`
- `coverage.md`
- Organized evidence files

It audits before remediation and does not implement fixes unless the user explicitly requests changes.

## Design philosophy

The included doctrine synthesizes public Apple design guidance and historical material around purpose, simplicity, agency, coherence, accessibility, iteration, and craft. Sources are attributed in `references/intentional-design-principles.md`. The skill does not reproduce Apple themes, colors, fonts, materials, or components.

## License

Released under the [MIT License](LICENSE).

