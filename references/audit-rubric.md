# Comprehensive Audit Rubric

Use this rubric to build the coverage ledger and conduct a deliberate page-by-page, state-by-state review. Adapt the matrix to the product; do not claim a dimension was tested when the surface or tools could not expose it.

## Coverage dimensions

Inventory and cross the applicable dimensions:

- Surface: screen, route, template, overlay, sheet, modal, popover, menu, notification, onboarding step, settings area, and error boundary.
- Context: authenticated role, permission level, data density, first use, returning use, offline/poor network, and destructive or sensitive flow.
- Presentation: viewport/window size, orientation, display scale, light/dark/high-contrast theme, zoom or text scale, reduced motion, locale, RTL, and long-content expansion.
- Input: mouse, touch, keyboard, pointer, stylus, game controller, voice, switch, or remote where relevant.
- State: default, hover, focus, pressed, selected, active, checked, indeterminate, disabled, expanded, dragging, loading, skeleton, empty, partial, success, warning, validation, error, offline, and overflow.

Visually inspect every in-scope instance. A repeated instance may share deep state evidence only when source inspection or rendered measurements prove it uses the same component and variant. Still inspect its content, placement, wrapping, surrounding alignment, and accessible name in context. Record the equivalence instead of silently sampling.

Before deep review, define one ledger row as a finite combination of canonical surface/template, distinct component or flow state, test context, and named data exemplar. Group dynamic instances only when they share implementation and presentation rules. For infinite feeds, pagination, user-generated detail routes, calendars, search spaces, or combinatorial data, name representative boundary exemplars such as empty, one item, typical, dense, long content, first/last page, and error. Lock the planned denominator and record later additions. If a dimension cannot be bounded credibly, ask the user to narrow it or mark it blocked/not tested; never imply exhaustive coverage of an unbounded set.

## Product and experience

- Can the primary user, task, value, and intended emotion be stated plainly?
- Does each screen immediately answer: Where am I? What matters now? What can I do? What happens next?
- Does navigation match the user's mental model and preserve orientation, history, and context?
- Are primary and secondary actions prioritized honestly? Are exits, undo, back, cancel, and recovery clear?
- Are steps, decisions, interruptions, data entry, and repeated work minimized without hiding necessary context?
- Do onboarding, empty, loading, success, and error states help the person progress?
- Are permissions, privacy, destructive effects, pricing, and commitments explained before the consequential action?
- Does the experience remain coherent from entry point through completion and return?

## Responsibility and foreseeable harm

- Who is affected besides the active user, and can an action expose, manipulate, exclude, burden, or endanger them?
- Is every collected field or permission necessary for the product's purpose? Are retention, sharing, and deletion understandable and controllable?
- Could the feature be abused, coerced, spammed, weaponized, or used outside its intended context? Are rate limits, reporting, consent, and safeguards proportionate?
- In health, finance, identity, safety, children, employment, or other sensitive contexts, are uncertainty, escalation, human review, and failure consequences designed explicitly?
- For AI output, are provenance, uncertainty, user control, correction, and safe failure appropriate to the stakes? Does the interface avoid false confidence or anthropomorphic manipulation?
- Would constraining or removing the feature serve people better when foreseeable harm outweighs its value?

## Hierarchy, layout, and geometry

- Verify grid, margins, safe areas, container widths, gutters, shared edges, alignment anchors, indentation, and reading order.
- Measure repeated gaps and dimensions. Distinguish intentional rhythm from accidental near-matches.
- Check typographic baselines, cap-height relationships, icon-to-label alignment, optical centering, and visual weight—not only bounding-box centering.
- Inspect proximity and grouping: related items should read together; unrelated groups need sufficient separation.
- Check borders, dividers, strokes, corner radii, shadows, elevation, opacity, translucency, and layer order for consistent purpose and geometry.
- Find clipping, collisions, unintended scrollbars, orphaned elements, stretched assets, subpixel blur, and layout shifts.
- Inspect dense and sparse data, short and long content, minimum and maximum window sizes, and nested scrolling.

## Typography and content

- Check family, size, weight, line height, letter spacing, paragraph width, alignment, hierarchy, contrast, and rendering consistency.
- Ensure text remains legible at supported zoom and text sizes; avoid truncating essential meaning.
- Verify wrapping, line breaks, punctuation, capitalization, numerals, dates, units, localization expansion, and mixed scripts.
- Use direct, specific labels. Similar actions use consistent vocabulary; different actions do not share misleading labels.
- Check instructions, helper text, placeholders, validation, errors, confirmations, and empty-state copy for timing and usefulness.
- Ensure tone serves the product and audience. Remove jargon, redundancy, blame, and decorative copy that competes with the task.

## Color, imagery, and iconography

- Check semantic color usage, contrast, theme variants, increased-contrast behavior, and meaning that survives without color.
- Verify brand colors remain intentional across backgrounds, imagery, translucency, overlays, disabled states, and data visualization.
- Inspect gradients, banding, color profiles, raster sharpness, vector rendering, aspect ratios, crops, focal points, and loading transitions.
- Ensure icons share a coherent optical size, stroke, fill, corner language, baseline, and metaphor while remaining distinguishable.
- Pair unfamiliar icons with labels or other discoverable explanation. Decorative imagery must not obscure content or interaction.

## Controls and interaction states

For every distinct control and contextual exception, inspect appearance, affordance, label, target size, focusability, state transition, feedback, error handling, and consistency.

| Control | Required checks |
| --- | --- |
| Button or link | Default, hover, focus, pressed, disabled, loading, label clarity, target size, destination/action distinction, repeated-click behavior |
| Text field or editor | Empty, filled, focus, selection, disabled, read-only, autofill, validation, error, long input, keyboard behavior, label persistence |
| Checkbox, radio, switch | On/off or selected/unselected, indeterminate where relevant, label target, focus, disabled, immediate versus committed effect |
| Tabs, segmented controls, navigation | Selected state, focus, overflow, scroll, route/history behavior, deep links, content continuity |
| Slider, scrubber, range | Minimum/maximum, step, drag, keyboard, value feedback, precision, reset, safe persistence behavior |
| Menu, select, autocomplete | Open/closed, focus movement, typeahead, selection, escape, outside click, scrolling, empty/no-results state |
| Dialog, sheet, popover | Entry focus, modal semantics, background behavior, escape/cancel, destructive confirmation, content overflow, return focus |
| Table, list, grid, card | Scan order, density, sorting/filtering, selection, actions, truncation, responsive collapse, empty/loading/error states |
| Tooltip, toast, notification | Trigger, timing, persistence, dismissal, keyboard/touch access, duplicate behavior, essential-content alternatives |
| Upload, payment, delete, publish | Inspect without executing unless approved; verify consequence, status, cancellation, recovery, privacy, and error states through fixtures or supplied evidence |

## Motion, feedback, and perceived performance

- Motion explains change, preserves continuity, confirms input, or conveys status; it does not merely decorate.
- Check gesture-to-motion alignment, duration, easing, direction, interruption, reversal, scroll behavior, and focus continuity.
- Verify immediate acknowledgement of input, progress for genuine waits, prevention of duplicate actions, and stable final layout.
- Look for jank, flashing, layout shifts, late font/image swaps, stalled controls, inconsistent skeletons, and cumulative delay.
- Respect reduced-motion and other sensory preferences. Essential information cannot exist only in animation, sound, or haptics.

## Responsive, adaptive, and international behavior

- Test meaningful width and height boundaries, not only fashionable device presets.
- Verify reflow, ordering, visibility, density, touch targets, navigation transformations, safe areas, keyboard obstruction, and orientation changes.
- Test zoom/text scaling, long labels, large numbers, missing data, RTL, locale formats, and translated-string expansion where available.
- Preserve the person's context across resize, rotate, theme, platform, and input changes.
- Mark browser viewport resizing as responsive testing, not native device, DPR, touch, or user-agent emulation.

## Accessibility

- Use the relevant platform requirements and WCAG 2.2 for web content.
- Verify semantic roles, accessible names, descriptions, states, relationships, headings, landmarks, reading order, and announcements where tools permit.
- Test keyboard access, visible focus, logical focus order, focus trapping/return, skip mechanisms, and operation without pointer-only gestures.
- Measure text and non-text contrast where applicable. Confirm information survives color-vision differences, forced/high-contrast modes, and missing images.
- Check touch/click targets and spacing against the target platform, not a universal Apple dimension.
- Test zoom, text scaling, reflow, reduced motion, captions/transcripts, alternatives for sound/haptics, and time-limit controls.
- Distinguish direct assistive-technology testing from DOM/code inspection. Do not claim a screen-reader pass based only on labels in source.

## Design-system integrity

- Compare repeated components, tokens, variants, states, and content rules across every page.
- Find one-off values, near-duplicate tokens, drifted variants, inconsistent state logic, and locally patched exceptions.
- Identify the smallest root fix: token before component, component before page override, page before flow, flow before concept.
- In polish mode, keep flow- and concept-level alternatives out of the committed recommendation set unless the user expands scope.

## Evidence discipline

- Measure before prescribing exact values. Use references or the product's own coherent patterns as the source of exact recommendations.
- A pixel difference is evidence of difference, not automatically evidence of harm.
- Record strengths and intentional exceptions so future reviewers do not “fix” them into sameness.
- Every recommendation needs an observable verification criterion.

