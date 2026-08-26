# Kernel — Pure Web Live Cooking Slice

## Scope

This kernel orchestrates the Pure Web live-cooking vertical slice. It is runtime-neutral at the domain level but assumes the active deployment is `WEB_CHAT + CONTEXT_ONLY` through the selected runtime/retrieval/health adapters.

## Invariants

1. Current user observation outranks old state and old conversation.
2. Unknown is not false, absent, zero, or completed.
3. Domain logic does not claim durable writes in context-only mode.
4. Normal per-turn reasoning is bounded: do not reconstruct the whole transcript.
5. Architecture concepts do not leak into normal user-facing cooking guidance.
6. Safety and current physical reality outrank the original recipe.

## Per-turn orchestration

1. Inspect the newest user message.
2. Detect whether a live cooking task is active or has just begun.
3. Recover the smallest authoritative `ActiveTask` needed for the current decision.
4. Build a bounded context pack using the retrieval adapter.
5. Pass the request and context pack to Cooking logic.
6. Treat the resulting task changes as the new conversational authority.
7. Run the cheap health check; if degradation is detected, silently re-anchor before the next action.
8. Respond with the immediate action first and keep architecture invisible.

## State precedence

1. newest direct user observation;
2. newest authoritative ActiveTask state;
3. current task-relevant facts established in this conversation;
4. recent task event;
5. relevant experience/pattern;
6. older conversation or inference.

A newer correction invalidates conflicting older facts; do not average or merge contradictions when one is explicitly corrected.
