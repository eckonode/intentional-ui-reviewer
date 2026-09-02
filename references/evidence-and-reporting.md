# Evidence and Reporting Contract

Create a report that a product lead can prioritize and a designer or engineer can implement without guessing. Preserve the distinction between what was observed, what was inferred, and what remains untested.

## Report bundle

Honor the user's output location. Otherwise use the workspace-designated user-output directory when one exists, or `<target-slug>-ui-ux-audit-<YYYYMMDD-HHmmss>/` in the current workspace. Confirm the directory does not exist; if it does, append `-2`, `-3`, and so on rather than merging or overwriting audit runs.

```text
<audit-bundle>/
|-- report.md
|-- coverage.md
`-- evidence/
    |-- UI-001-baseline.png
    |-- UI-001-state.png
    |-- UI-001-diff.png
    `-- UI-001-metrics.json
```

Use the smallest evidence set that proves the finding. Prefer masked test data and focused captures. Before saving, inspect for account names, email addresses, avatars, tokens, customer data, private messages, financial or health information, and unrelated content. Crop or redact them with an available permitted tool and note the redaction; if evidence cannot be sanitized without losing its meaning, do not save the capture and use a privacy-safe textual location instead. Never include credentials or secrets.

## Design Intent Contract

Place this near the beginning of `report.md`:

| Field | Recorded value |
| --- | --- |
| Engagement mode | New design / Polish existing design / Authorized redesign |
| Product purpose | Primary human outcome |
| Primary audiences and tasks | Who and what |
| Must preserve | Intentional elements and non-negotiables |
| Source of truth | Design system, reference, platform convention, or none |
| Maximum allowed change level | Token / Component / Page / Flow / Concept |
| Maximum structural impact | Local / Moderate / Substantial |
| Explicit exclusions | Out-of-scope surfaces or changes |

When interaction is possible, ask once and wait for the answer. If the user declines, a reply is unavailable, or the execution context cannot accept one, record `Polish existing design (defaulted; confirmation unavailable)` and preserve the existing system.

## Coverage ledger

Store the full ledger in `coverage.md` and summarize it in the report.

| ID | Surface/page | Component or flow | State | Viewport/device | Theme | Input | Role/data context | Result | Evidence/notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed results:

- **Passed:** directly reviewed with no finding for this row.
- **Failed:** directly reviewed and linked to one or more findings.
- **Blocked:** intended test could not proceed because access, data, hardware, authentication, safety, or tooling was unavailable.
- **Not tested:** included in scope but not exercised; explain why.

An activation or state that the user explicitly excludes before the ledger is built stays outside the denominator and appears under Design Intent Contract exclusions. Create separate in-scope rows for any allowed visual, semantic, or source inspection of that control. If a planned row later cannot be exercised because of safety or missing approval, mark it blocked; never remove it retroactively to raise coverage.

At finalization there are no “pending” rows. Compute:

```text
observed coverage = (passed rows + failed rows) / total planned rows
```

Report counts for passed, failed, blocked, and not tested. A failure counts as observed, not successful. Use “complete” only when coverage is 100% and blocked/not-tested counts are zero.

Define the row unit, canonical grouping rules, dynamic-data exemplars, and initial denominator above the table. Record any later row additions with a reason. Do not use an unbounded collection as a denominator.

## Finding schema

Every finding contains:

- **ID and title**
- **Classification:** Standards violation / Objective reference mismatch / System inconsistency / Expert design judgment
- **Severity:** P0 / P1 / P2 / P3
- **Confidence:** High / Medium / Low
- **Engagement mode**
- **Change level:** Token / Component / Page / Flow / Concept
- **Structural impact:** Local / Moderate / Substantial
- **Location:** surface, route/frame, component, state, viewport/device, theme, input, and role/data context
- **Evidence:** linked artifact, exact visible location, and evidence type
- **Observation:** what happened, without interpretation blended in
- **Measurement:** value, method, environment, tolerance, and source of truth when applicable
- **Principle or standard:** design doctrine, product rule, platform guidance, or WCAG criterion
- **User impact:** affected audience, task, frequency, and consequence
- **Likely root cause:** label as inferred unless confirmed in source
- **Recommended fix:** smallest coherent change within the Design Intent Contract
- **Verification criteria:** observable steps and expected result

### Classification

- **Standards violation:** a testable accessibility, platform, safety, or product requirement is not met.
- **Objective reference mismatch:** a matched implementation differs measurably from an authoritative reference.
- **System inconsistency:** repeated product rules, tokens, components, labels, or behavior disagree without an intentional exception.
- **Expert design judgment:** a reasoned recommendation based on hierarchy, usability, perception, or craft where no objective rule alone decides the outcome.

### Severity

- **P0 — Blocking:** prevents a core task or creates severe safety, trust, data-loss, or accessibility exclusion.
- **P1 — Major:** substantially harms a core flow, many people, or a repeated foundational component.
- **P2 — Meaningful:** causes notable friction, confusion, inconsistency, or visual degradation but has a workable path around it.
- **P3 — Polish:** localized craft issue with limited task impact.

Severity reflects user and product impact, not how visually irritating the issue feels.

### Confidence

- **High:** directly observed and supported by strong evidence or an authoritative rule.
- **Medium:** evidence is good but the expected intent, frequency, or environment has an unresolved assumption.
- **Low:** artifact or tool limitations make the diagnosis tentative; state the verification needed.

### Change level

- **Token:** shared value such as spacing, type, color, radius, stroke, or motion.
- **Component:** a reusable control or component behavior.
- **Page:** composition or content specific to one surface.
- **Flow:** navigation, sequence, information architecture, or cross-page behavior.
- **Concept:** product direction, interaction model, or visual language.

Change level describes reach, not magnitude. Record structural impact separately:

- **Local:** preserves hierarchy, composition, interaction model, and visual language while correcting a bounded issue.
- **Moderate:** reorganizes a meaningful section or shared component behavior but preserves the product's core model and identity.
- **Substantial:** recomposes a page, relocates navigation, changes a flow, or replaces the visual or interaction language.

In polish mode, supported token/component/page changes may be committed only within the agreed structural impact. Flow/concept ideas and any substantial page recomposition, navigation relocation, or visual-language replacement belong under **Requires scope approval**.

## `report.md` structure

1. **Executive summary** — engagement mode, intended experience, observed coverage, highest-impact issues, and overall confidence.
2. **Design Intent Contract**
3. **Strengths worth preserving** — intentional decisions that work and should survive remediation.
4. **Scope, method, and limitations** — surfaces, tools, environments, references, and untested capabilities.
5. **Coverage summary** — counts and link to `coverage.md`.
6. **Prioritized issue register** — compact table of all findings.
7. **Detailed findings** — complete schema and evidence for each ID.
8. **Systemic patterns and root causes** — shared fixes and affected finding IDs.
9. **Quick wins and structural fixes** — separate minimal improvements from deeper work.
10. **Requires scope approval** — flow/concept opportunities outside polish scope; omit when empty.
11. **Blocked and untested areas**
12. **Verification and regression checklist**

Do not produce a single vanity score. Counts, coverage, evidence, severity, and explicit tradeoffs are more honest.

## Recommendation rules

- Preserve the Design Intent Contract and state why the recommendation fits it.
- Recommend exact values only when a reference, token system, measured repeated pattern, or platform requirement supports them.
- Prefer the smallest root fix that resolves all affected instances without erasing intentional exceptions.
- Separate required remediation from optional exploration.
- Include a verification procedure that another person can run.
- Complete the audit before implementing. If the user asks for fixes, keep the report as the baseline and update verification status after remediation rather than rewriting history.

## Accessibility evidence levels

Label accessibility evidence explicitly:

1. **Directly tested:** observed with the relevant keyboard, device, setting, or assistive technology.
2. **Measured:** contrast, geometry, target size, timing, or a similar value computed from rendered output.
3. **Inspected:** role, name, relationship, or implementation inferred from DOM, source, or design metadata.
4. **Not tested:** capability, device, state, or artifact unavailable.

Do not upgrade inspected evidence to a direct pass. When a screen reader or true device is unavailable, state that limitation and provide a verification procedure.

## Chat handoff

Lead with the outcome: engagement mode, observed coverage, P0/P1 findings, most important systemic pattern, blocked areas, and the saved bundle location. Keep the chat concise; the bundle carries the full evidence.

