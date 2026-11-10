# Information Density & Progressive Disclosure

**Stable ID:** `information-density-and-disclosure`  
**Class:** Core  
**Primary domain:** Information, Attention & Typography

## Observable trigger

Route here when users must hold, compare, or infer too much at once, or when necessary complexity is exposed or hidden at the wrong moment.

## Non-trigger and near miss

Do not route here merely because a screen contains many items. Dense expert interfaces can reduce effort when relationships stay visible. If the problem is only poor grouping or too many removable choices, address those causes without hiding necessary information.

## Decision question

Which complexity must remain visible, which can be removed or carried by the system, and how should the rest be staged without destroying comparison, control, or trust?

## Interpretation method

Measure cognitive burden as simultaneous recall, comparison, inference, decision, and exception handling—not item count. Group by user meaning and task relation. Separate eliminable complexity from complexity that must be allocated among system, defaults, workflow, documentation, team, and user. Reveal primary evidence and common action by default; expose details, exceptions, advanced control, and explanation at the point of need.

## Executable design procedure

1. Map the current task and mark every fact users must remember, compare, infer, or choose simultaneously.
2. Remove duplication and irrelevant choice before adding disclosure.
3. Chunk by meaningful task relation, not arbitrary number.
4. Allocate unavoidable complexity explicitly between system and user; preserve visibility into consequential automation.
5. Define default, expanded, exception, audit, and recovery layers.
6. Keep comparison targets together and avoid burying prerequisites behind sequential disclosure.
7. Test novice, expert, stress, interruption, assistive, and error-recovery conditions with real content.

## Boundaries and failure modes

- Do not invoke a fixed item limit such as seven.
- Do not ship system complexity to users or hide consequential rules in an opaque black box.
- Do not make sparse appearance the goal when dense visibility supports expert comparison.
- Preserve consent, auditability, undo, and error recovery for automated defaults.
- Return `reframe` and signal Information, Attention & Typography when text structure rather than complexity allocation is the burden, or when staging itself creates unsupported recall.

## Attached Reference Knowledge

Recognition and meaningful chunking reduce working-memory cost. Progressive disclosure is responsibility allocation, not concealment. Visible complexity can be humane when it matches the task; hidden complexity can be harmful when it removes agency or explainability.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; observed cognitive burden; complexity allocation; default and on-demand layers; comparison and control protections; user-mode cases; validation obligation; and the onward state.

## Runtime Self-Critique

Ask what users must remember after each disclosure, what the system has hidden, whether comparisons remain possible, and whether visual sparsity has displaced rather than reduced burden.
