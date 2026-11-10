# Flexible Responsive Composition

**Stable ID:** `flexible-responsive-composition`  
**Class:** Core  
**Primary domain:** Computational Medium & Embodiment

## Observable trigger

Route here when accepted composition regimes and hierarchy exist, but their implementation depends on accumulating device-specific breakpoint patches or breaks between regimes as content, container, input, or capability changes.

## Non-trigger and near miss

Do not route here when the hierarchy or composition regimes themselves remain unresolved; return `reframe` and signal Spatial Composition. Do not route here when a breakpoint represents an intentional product-mode change, one figure only needs a sizing algorithm, or the defect is unrelated to adaptation.

## Decision question

Which intrinsic and flexible relationships should adapt continuously, and at what content-led thresholds must composition or capability change meaningfully?

## Interpretation method

Start from a flexible base using intrinsic sizing, wrapping, proportional tracks, min/max constraints, responsive media, grid or flex behavior, and local container conditions. Let breakpoints express a real change in information, interaction, or composition—not repair rigid CSS. Separate visual reflow from capability fallback: a smaller or weaker device may require a different medium behavior while preserving the core task and thesis.

## Executable design procedure

1. Audit each breakpoint and classify it as meaningful design change or rigidity patch.
2. Identify fixed widths, absolute positioning, unbounded media, and component assumptions causing failure.
3. Rebuild the base with intrinsic, min/max, wrapping, flexible-track, and container-aware rules.
4. Define content-led thresholds where hierarchy, sequence, control placement, or medium capability must actually change.
5. Preserve semantic and focus order while allowing visual recomposition.
6. Define feature support, input, performance, and reduced-capability fallbacks.
7. Test continuous resizing, long and localized content, zoom/reflow, touch and keyboard, embedded containers, and target devices.

## Boundaries and failure modes

- Do not select thresholds from named device models.
- Do not treat more media queries as evidence of responsiveness.
- Do not force one visual arrangement across genuinely different interaction modes.
- Avoid visual reorder that contradicts reading, focus, or task sequence.
- Gracefully degrade expressive media before state truth, control access, or core content.

## Attached Reference Knowledge

Intrinsic layout lets content and available space negotiate. Container queries localize adaptation; feature queries and progressive enhancement protect capability differences. A breakpoint is justified when the design relation changes, not when a popular viewport number appears.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; rigidity causes; flexible base rules; content-led thresholds; preserved hierarchy and semantics; capability fallbacks; target test matrix; and the onward state.

## Runtime Self-Critique

Resize continuously and ask whether each relationship bends before it breaks, whether every breakpoint expresses a real design change, and whether fallback retains task, protagonist, and agency.
