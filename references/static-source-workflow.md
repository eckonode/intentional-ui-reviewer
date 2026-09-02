# Static Artifact and Source Workflow

Use this workflow for screenshots, recordings, repositories, component catalogs, tokens, and design-system documentation.

## Screenshots and recordings

Inspect images at original detail when precision matters. Record pixel dimensions, claimed device/viewport, theme, state, scale, and provenance. Review visible hierarchy, layout, alignment, rhythm, type, color, assets, content, and apparent state.

A screenshot cannot prove hover, focus, keyboard order, semantics, responsive behavior, loading/error recovery, animation quality, or target behavior. A recording can show timing and motion but still cannot prove semantics or alternate states. Put these limits in the coverage ledger.

Inspect captures for personal or confidential data before saving them into an audit bundle. Prefer masked fixtures; otherwise crop or redact with an available permitted tool and disclose the redaction. If safe evidence cannot be produced, record a textual location instead.

## Source code and design systems

Use source inspection to discover canonical routes/templates, component reuse, variants, tokens, breakpoints, semantics, fixtures, and state logic. Source can prove shared implementation and explain a root cause; it cannot prove final rendered quality without visual inspection.

- Map one-off values and near-duplicate tokens to visible inconsistencies.
- Define finite data exemplars for unbounded route parameters, feeds, pagination, date ranges, and user content.
- Prefer a token or shared-component fix when it corrects all affected instances without violating intentional exceptions.
- Link recommendations to the product's actual framework and conventions.
- Do not modify source during the audit unless the user explicitly requests remediation.

## Mixed evidence

When both source and captures exist, correlate them: use the render to prove the visible issue and source to confirm reuse, token provenance, or likely root cause. Do not elevate an inference to a confirmed cause without source evidence.

