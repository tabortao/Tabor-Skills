# Loading & Perceived Feedback

**Stable ID:** `loading-and-perceived-feedback`  
**Class:** Core  
**Primary domain:** Motion, Rhythm & Causality

## Observable trigger

Route here when waiting, progress, streaming, save, validation, or responsiveness lacks a truthful perceptual treatment and users cannot tell whether the system heard them, what is happening, or what they can do next.

## Non-trigger and near miss

Do not route here when motion must preview an action outcome, when the problem is a missing backend operation, or when a generic status already truthfully covers an imperceptibly short task.

## Decision question

What immediate and evolving feedback reduces uncertainty, preserves context and control, and communicates real progress or uncertainty without pretending work is faster than it is?

## Interpretation method

Classify response as immediate, determinate, indeterminate, streaming, optimistic, queued, blocked, failed, or intentionally frictional. Acknowledge receipt promptly, then show content-shaped skeletons, real progress, partial results, stage, remaining uncertainty, or contextual work as available. Keep usable content visible and expose cancel, retry, background, and recovery when duration or failure justifies them.

## Executable design procedure

1. Map user uncertainty, backend truth, duration distribution, stages, failure, and cancellation.
2. Define immediate acknowledgement before longer feedback.
3. Choose a truthful pattern: local pending state, skeleton, determinate progress, streaming result, stage label, estimate range, or background task.
4. Preserve context and usable content; avoid full-screen replacement unless the entire task truly blocks.
5. Define partial, success, error, cancel, retry, stale, and offline outcomes.
6. Add identity only where it clarifies the task and does not prolong waiting.
7. Test fast/slow paths, repeated action, assistive announcement, reduced motion, failure, and intentional safety friction.

## Boundaries and failure modes

- Do not fabricate progress, certainty, speed, or completion.
- Avoid generic spinners where stage or content can be communicated.
- Do not make feedback so brief it is invisible or so long it becomes performance.
- Preserve necessary friction for safety, privacy, verification, and high-value commitment.
- Long AI work requires partial results, uncertainty, cancellation, and retry rather than indefinite animation.

## Attached Reference Knowledge

Perceived performance is the relationship between action and intelligible response. Early acknowledgement reduces doubt; content-shaped feedback preserves orientation. Faster is not always more trustworthy when careful processing matters.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; waiting type and uncertainty; immediate acknowledgement; truthful progress/partial pattern; context and control; complete failure/recovery states; accessibility and timing checks; and the onward state.

## Runtime Self-Critique

Ask whether the system tells the truth, whether users can continue or recover, whether context survives, and whether visual activity reduces uncertainty rather than merely occupying time.
