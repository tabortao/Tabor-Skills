# State, Memory & Recognition

**Stable ID:** `state-memory-and-recognition`  
**Class:** Core  
**Primary domain:** Information, Attention & Typography

## Observable trigger

Route here when users must remember hidden mode, prior input, query, transformation, code, exception, or step in order to continue or recover.

## Non-trigger and near miss

Do not route here when trained experts explicitly choose a pure command workflow, when security forbids exposing the information, or when available options are visible but semantically wrong.

## Decision question

Which system-known facts should be externalized as state or recognition cues, and how can the design preserve expert efficiency, privacy, and aesthetic coherence?

## Interpretation method

Treat working memory as the user's current focus, not persistent storage. Inventory information the system already knows and users will need next. Replace unsupported recall with visible state, history, recent items, examples, thumbnails, suggestions, position cues, searchable commands, or contextual instructions. Make common functions visible in proportion to audience and frequency while retaining shortcuts for trained experts.

## Executable design procedure

1. Walk the task and list every fact users must remember across screens, modes, interruptions, or time.
2. Mark what the system knows, what privacy permits, and what forgetting would cost.
3. Choose a persistent, contextual, historical, suggested, or searchable recognition cue.
4. Expose current mode, scope, query, filters, transformations, progress, and unsaved change where consequential.
5. Keep common paths recognizable and preserve optional expert shortcuts.
6. Test interruption, return after delay, multi-device or multi-window state, error recovery, privacy, and assistive access.

## Boundaries and failure modes

- Do not expose secrets or sensitive state; provide safe hints and recovery instead.
- Do not show stale or ambiguous history that users may mistake for current truth.
- Do not force common actions into hidden gestures, syntax, or undocumented commands.
- Avoid decorative icons whose metaphor does not match the target.
- Return `reframe` and signal Interaction, Agency & Wayfinding when users recognize options but interpret their objects or actions incorrectly.

## Attached Reference Knowledge

Recognition uses external cues; recall requires unsupported reconstruction. Recent items, examples, suggestions, and command search can bridge novice and expert use. Consistency is especially important because a small set of exceptions is harder to remember than an entirely explicit rule.

## Required Capability Contribution

Return exactly the canonical seven fields from `routing-and-reconciliation.md`: `decision`, `evidence`, `recommendation`, `consequence`, `boundary`, `validation`, and `onward`. Do not add a mini-report.

Populate those fields with the decision key; recall burden; system-known state; selected recognition cues; privacy boundary; expert path; interruption and recovery checks; validation obligation; and the onward state.

## Runtime Self-Critique

Ask what users still need to remember, whether displayed state is current and scoped, whether privacy is preserved, and whether expert efficiency survives without making common use depend on memory.
