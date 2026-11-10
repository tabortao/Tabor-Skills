# Visual Effect Accessibility

**Stable ID:** `visual-effect-accessibility`  
**Class:** Core  
**Primary domain:** Human Fit, Cognition & Inclusion

## Observable trigger

Route here when a visual effect's implementation layer, color channel, compositing method, semantics, focus, hit testing, readability, redundant channel, or fallback risks excluding perception or operation.

## Non-trigger and near miss

Do not route here when the only unresolved risk is temporal comfort, flashing, auto-advance, interruption, or device motion degradation; return `reframe` and signal Motion, Rhythm & Causality. When temporal risk and semantic/effect-layer access are independently material, include that evidence in the contribution so the Director can form a cross-domain cluster. Do not route for a purely decorative background that cannot affect content, interaction, comfort, performance, or meaning.

## Decision question

Which implementation preserves the intended effect while keeping content semantics, readable contrast, operation, fallback, and redundant state evidence intact?

## Interpretation method

Compare candidate implementations—semantic markup, pseudo-elements, overlays, filters, blend modes, SVG, images, or extra layers—by visible fidelity and accessibility consequence. Track alt semantics, reading order, focus, hit testing, dimensions, contrast, zoom, high contrast, browser support, performance, and fallback. Pure CSS has no automatic moral or technical priority over semantic markup.

## Executable design procedure

1. State the effect's product purpose and the information or interaction it touches.
2. List viable implementations and a no-effect baseline.
3. Build a tradeoff matrix for semantics, readability, input, focus, responsiveness, support, performance, and fallback.
4. Choose the least harmful implementation that preserves the effect's essential relationship.
5. Add redundant text, shape, pattern, position, or state channels where color/effect carries meaning.
6. Test alt access, DOM and focus order, pointer events, zoom/reflow, contrast modes, color vision, reduced motion, and unsupported browsers.

## Boundaries and failure modes

- Do not replace meaningful images or text with styled backgrounds that erase semantics.
- Do not accept translucent or blended beauty that makes content hard to read.
- Do not hard-code dimensions that break reflow or allow overlays to intercept controls.
- Verify current browser and assistive support for modern visual effects.
- Remove or simplify the effect when no implementation preserves task and meaning.

## Attached Reference Knowledge

Accessibility can fail at system layers: semantics, perception, operation, or fallback. Redundant channels preserve meaning without requiring identical appearance. Implementation elegance is subordinate to user access and effect purpose.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; effect purpose and exclusion risk; candidate tradeoff; selected implementation; redundant channels; fallback; explicit accessibility consequence and tests; and the onward state.

## Runtime Self-Critique

Ask what disappears when CSS, color, motion, or images are unavailable, whether overlays change interaction, and whether the alternative preserves the authored idea rather than merely disabling it.
