# Expressive Medium Selection

**Stable ID:** `expressive-medium-selection`  
**Class:** Core  
**Primary domain:** Computational Medium & Embodiment

## Observable trigger

Route here when the protagonist, ritual, or Signature Move could be embodied through materially different media—DOM/CSS, SVG, Canvas, WebGL/WebGPU, 3D, video, procedural systems, physics, or a hybrid—and the choice changes perception, control, performance, or fallback.

## Non-trigger and near miss

Do not route here when the platform and representation are fixed and only a local implementation detail remains, when the desired perceptual or task effect is not yet defined, or when broken geometry, materials, content, or state—not the medium—causes the failure.

## Decision question

Which computational medium produces the required perceptual and interactive evidence with sufficient control, accessibility, performance, reversibility, and graceful degradation?

## Interpretation method

Name the visible and behavioral effect before naming technology. Decompose it into observable evidence such as silhouette, depth, edge behavior, translucency, temporal stability, direct manipulation, semantic structure, spatial continuity, or procedural variation. State where that evidence must survive: viewport, distance, device, input, motion, content, and hardware tier.

Compare candidate media on fidelity, artifacts, latency, memory, precomputation, update cost, authoring control, semantic accessibility, testing, and revision risk. Use a modern, simple baseline. Accept approximation when it contributes only the intended effect and does not reveal the workaround. Prefer the least complex medium that makes the protagonist and ritual genuinely structural.

For motion representation, distinguish two-state interpolation, explicit keyframe timelines, continuous geometric correspondence, and discrete frame sequences. Do not select a library before deciding the topology and control model.

## Executable design procedure

1. Write an effect evidence contract for the protagonist, ritual, and Signature Move.
2. Lock required content semantics, input, responsive states, accessibility behavior, performance budget, and fallback.
3. List viable media and hybrids; include the simplest semantic baseline.
4. Prototype the highest-risk evidence with identical inputs across candidates.
5. Compare visible fidelity, artifacts, latency, memory, update cost, control, reversibility, testability, and authoring burden.
6. Select the medium whose unique affordance carries the design idea; assign every hybrid layer one clear responsibility.
7. Define upgrade and degradation thresholds, including static, reduced-motion, lower-dimensional, or lower-cost equivalents.
8. Validate real content, resizing, interruption, input modes, target devices, and the failure condition that would invalidate the choice.

## Boundaries and failure modes

- Do not choose 3D, shaders, particles, or Canvas because they signal ambition; require load-bearing evidence.
- Do not force unstable geometric interpolation between incompatible shapes; use a discrete representation when topology demands it.
- Do not hide essential semantics or controls in an inaccessible render surface.
- Do not use perceptual approximation for scientific, safety-critical, or regulated precision without engineering error bounds.
- Reject techniques whose artifacts reveal the proxy, whose fallbacks erase the core task, or whose resource cost prevents truthful interaction.

## Attached Reference Knowledge

DOM/CSS excels at semantics, text, layout, and ordinary state. SVG offers addressable vector structure and scalable illustration. Canvas favors dense immediate drawing with manually rebuilt semantics. WebGL/WebGPU and 3D carry depth, material, particles, and procedural worlds at higher control and resource cost. Hybrids work when responsibilities remain explicit. Multisensory or acoustic expression requires an actual product role and must never be assumed available or appropriate.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; effect evidence contract; candidate comparison; selected medium and unique responsibility; control and resource consequences; accessibility and semantic boundary; fallback and invalidation threshold; cross-domain signals; and the onward state.

## Runtime Self-Critique

Ask whether the medium changes the experience rather than decorating it, whether a simpler medium preserves the same evidence, whether semantics and agency survive, whether the fallback remains truthful, and which real-device test could disprove the choice.
