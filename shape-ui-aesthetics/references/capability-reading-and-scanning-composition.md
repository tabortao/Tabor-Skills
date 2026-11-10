# Reading & Scanning Composition

**Stable ID:** `reading-and-scanning-composition`  
**Class:** Core  
**Primary domain:** Information, Attention & Typography

## Observable trigger

Route here when operational text is present but costly to locate, parse, compare, verify, or act on because it is repetitive prose, undifferentiated fields, unstable terminology, or visually hostile typography.

## Non-trigger and near miss

Do not route here when the task is immersive long-form reading, when legal or clinical meaning needs accountable rewriting, or when brief text already scans correctly and the problem is tone or conceptual model.

## Decision question

How should content and typography be rewritten and recomposed so users can locate, compare, verify, and act without unnecessary reading?

## Interpretation method

Treat interface reading as expensive and interruptible. Identify text that must be read to complete the task, then distinguish labels, values, status, action, evidence, exception, and explanation. Promote repeated language into headings or field structure, expose differences, segment long numbers, and maintain familiar terms. Use type, contrast, measure, spacing, alignment, and semantic markup to reinforce—not invent—the information structure.

## Executable design procedure

1. List the scanning tasks and the smallest information units each requires.
2. Mark mandatory, supporting, expandable, regulated, and redundant text.
3. Remove repetition and convert prose into fields, lists, labels, values, or comparisons where appropriate.
4. Establish semantic and typographic hierarchy for identity, status, value, unit, action, and explanation.
5. Segment identifiers and numbers according to verification behavior.
6. Test brief glance, side-by-side comparison, narrow viewport, zoom, localization, screen reader order, and interruption recovery.
7. Preserve exact accountable wording where meaning cannot be changed; improve its presentation and layering instead.

## Boundaries and failure modes

- Do not delete legal, safety, clinical, or contractual meaning without accountable authority.
- Avoid small type, long all-caps text, decorative faces, low contrast, patterned text backgrounds, and unstable terminology.
- Do not convert every sentence into fragments when narrative comprehension is the task.
- Do not let visual order contradict DOM or assistive reading order.
- Return `reframe` and signal Interaction, Agency & Wayfinding when terminology reflects the wrong conceptual model, or Information, Attention & Typography when structural staging rather than scanning composition is the root issue.

## Attached Reference Knowledge

Scanning seeks anchors and differences; reading follows when needed. Semantic text effects must preserve copy, selection, zoom, and accessibility. Typography can lower recognition friction but cannot repair incorrect content relationships.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; observed scanning cost; rewritten information structure; typographic hierarchy; preserved exact-meaning content; responsive and assistive obligations; validation task; and the onward state.

## Runtime Self-Critique

Ask whether users can find and compare the decisive facts without reading everything, whether typography reflects semantics, and whether compression removed nuance or accountability.
