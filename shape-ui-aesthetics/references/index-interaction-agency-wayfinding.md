# Interaction, Agency & Wayfinding Index

**Decision question:** Do the interface's objects, actions, feedback, control, and recovery match the user's real activity model?

**Material signals:** Users translate their goal into system terms; affordances imply the wrong action; a novel spatial control imports an invalid 2D model; available actions do not fit the task.

**Non-signals:** The task model and action vocabulary are sound and the issue is only visual prominence, reading density, or rendering quality.

## Routes

| Stable ID | Class | Trigger signature | Expected contribution | Exact contract |
|---|---|---|---|---|
| `task-affordance-and-conceptual-model` | Core | Interface objects and available actions do not match the user's activity model. | An aligned task model, lexicon, affordance set, and action vocabulary. | [Load contract](capability-task-affordance-and-conceptual-model.md) |
| `goal-action-feedback-loop` | Core | Users lose the connection between intent, action, system state, and feedback. | A diagnosed loop break and repaired scent, action, state, and feedback chain. | [Load contract](capability-goal-action-feedback-loop.md) |

**Selection seam:** Route the conceptual-model contract when objects, actions, properties, relationships, or terms are wrong. Route the loop contract only after that ontology is accepted and one execution/evaluation hop breaks.

**Cross-domain handoffs:** Signal Human Fit when learned expectations or physical execution fail; Motion when feedback must expose cause; Medium when an input/output technique changes affordance; Information when labels or scent obscure the model; Spatial Composition when wayfinding depends on organization.
