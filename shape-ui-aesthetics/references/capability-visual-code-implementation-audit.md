# Visual–Code Implementation Audit

**Stable ID:** `visual-code-implementation-audit`  
**Class:** Core  
**Primary domain:** Coherence, Critique & Evidence

## Observable trigger

Route here when the implemented interface may materially differ from its visual language, when uncontrolled variants accumulate, or when code and rendered state provide conflicting evidence of the system.

## Non-trigger and near miss

Do not route here when an audit already exists and the task is organizational investment, or when the goal is to define a new token grammar rather than diagnose current implementation.

## Decision question

Where do rendered UI, visual roles, interaction states, and implementation primitives diverge, and which discrepancies are highest-value to standardize or remove?

## Interpretation method

Collect three aligned inventories: UI components and state variants; visible color, type, spacing, icon, depth, imagery, and motion expressions; and code selectors, declarations, tokens, component APIs, asset use, and duplication. Compare intended semantic roles with actual rendered and code usage. Prioritize drift that harms task truth, accessibility, adoption, performance, or product grammar.

## Executable design procedure

1. Define product surfaces, states, platforms, and code boundaries in scope.
2. Capture representative rendered variants with real content.
3. Inventory visual values and semantic roles.
4. Inventory code primitives, tokens, selectors, component variants, and dead or duplicate paths.
5. Link visible discrepancies to implementation causes and distinguish legitimate exceptions.
6. Rank corrections by user consequence, reach, risk, and consolidation value.
7. Verify corrected code through rendered, interaction, accessibility, and regression checks.

## Boundaries and failure modes

- Do not infer visual truth from code statistics alone or code truth from screenshots alone.
- Do not collapse purposeful variants for numeric cleanliness.
- Avoid standardization that changes protected behavior or state semantics.
- Include modern token drift, variable sources, component analytics, and accessibility evidence where available.
- Keep the audit diagnostic. When the task is to define a future semantic grammar rather than diagnose current drift, return `reframe` and signal Coherence, Critique & Evidence to the Director.

## Attached Reference Knowledge

UI, visual, and code inventories expose different layers of drift. Their intersection identifies which inconsistencies are systemic and which are intentional. Visible validation is required after implementation changes.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; scoped inventories; visual/code discrepancy map; legitimate exceptions; ranked targets; technical and visual verification; boundary; and the onward state.

## Runtime Self-Critique

Ask whether each claimed discrepancy is visible and code-backed, whether standardization preserves authored exceptions, and whether the rendered result—not the refactor alone—passes.
