# Task, Affordance & Conceptual Model

**Stable ID:** `task-affordance-and-conceptual-model`  
**Class:** Core  
**Primary domain:** Interaction, Agency & Wayfinding

## Observable trigger

Route here when the interface ontology itself is wrong: its objects, action vocabulary, properties, relationships, or terms do not match the user's activity model, or familiar controls change meaning in a new context.

## Non-trigger and near miss

Do not route here when the ontology is accepted and one specific execution or evaluation hop breaks between intent, action, state, and feedback; return `reframe` and signal Interaction, Agency & Wayfinding. Do not route here for copy polish, target acquisition, or a genuinely missing feature.

## Decision question

What task-centered objects, actions, relationships, terms, and perceptible affordances let users act directly on their goal while preserving necessary system and social constraints?

## Interpretation method

Inspect the activity before the interface. Record subject, goal, tools, community, rules, division of responsibility, sequence, errors, information sources, collaboration, and intended outcome. Build a user conceptual model that exposes only the objects, actions, properties, and relationships needed for the activity.

For each consequential action, audit four affordance dimensions: cognitive understanding, physical executability, functional task effect, and sensory evidence of outcome. Compare the user's model with system structure. Do not assume a familiar two-dimensional control keeps its meaning when moved into a spatial, collaborative, multimodal, or AI-mediated setting.

## Executable design procedure

1. Write the user's goal in their language and reconstruct the real activity, including rules, collaborators, errors, and completion conditions.
2. Extract the minimum task objects, actions, properties, and relationships.
3. Remove or translate implementation concepts that do not belong to the user's work.
4. Build an object/action matrix and identify impossible, ambiguous, overloaded, or missing actions.
5. Define one consistent task lexicon with one term per consequential concept.
6. Audit each key action for cognitive, physical, functional, and sensory affordance.
7. Materialize clear availability, constraints, state changes, feedback, undo or recovery, and collaborative ownership.
8. Validate with representative users and the actual input/output context; revise the model when users repeatedly translate or mispredict.

## Boundaries and failure modes

- Do not disguise organizational, regulatory, or technical complexity that users must genuinely understand.
- Do not claim that a familiar visual control remains familiar after its action, scale, input, or social meaning changes.
- Do not treat this review as accessibility compliance, ergonomics approval, safety certification, or organizational governance.
- Avoid feature growth that multiplies concepts and inconsistent synonyms.
- Signal Human Fit for learned expectation and ability, Motion for causal feedback, Medium for device/input selection, and Spatial Composition for wayfinding.

## Attached Reference Knowledge

CSS appearance can imply affordance but cannot repair a false conceptual model. Spatial interfaces require context-sensitive affordances and must account for tracked and untracked participants, shared attention, perspective, and social rules. Good task lexicons are familiar, task-focused, one-to-one, and stable across states.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; evidence of model mismatch; task model and minimum object/action vocabulary; lexicon corrections; four-part affordance findings; state, feedback, and recovery consequences; professional or context boundaries; validation obligations; and the onward state.

## Runtime Self-Critique

Ask whether users can describe the objects and predict actions in their own terms, whether every important action is perceivable and executable, whether the result is evident, and whether any simplification hides a real rule or shifts burden onto the user.
