# Kernel — Web Live Cooking Orchestration

## Scope

This kernel orchestrates the Web live-cooking vertical slice across either:

- `WEB_CHAT + CONTEXT_ONLY`; or
- `WEB_CHAT + a compatible durable StorageProvider`.

Runtime and storage remain separate. The selected provider may change without changing Cooking domain logic.

## Invariants

1. Current user observation outranks stored state and old conversation.
2. Unknown is not false, absent, zero, or completed.
3. Approximate values do not become exact without new evidence.
4. Domain logic never writes a StorageProvider directly.
5. ContextRetriever is read-only and normal per-turn reasoning is bounded.
6. PersistenceCoordinator is the semantic write gate.
7. Durable success is claimed only after a durable provider confirms the commit.
8. Architecture concepts do not leak into normal user-facing cooking guidance.
9. Safety and current physical reality outrank the original recipe.

## Per-turn orchestration

1. Create the current `TaskRequest` from the newest user message.
2. Read runtime capabilities; resolve storage separately.
3. Ask ContextRetriever for tiny routing bootstrap state.
4. Select Cooking when the explicit request or active task indicates live cooking.
5. Ask Cooking for its retrieval requirements.
6. Build a bounded ContextPack through the selected Retriever implementation.
7. Run a cheap preflight Health inspection when continuity/freshness may matter.
8. Pass the request and ContextPack to Cooking logic.
9. Normalize any requested task/state/experience changes into a `ChangeSet`.
10. If changes exist, pass them to PersistenceCoordinator; only it may write the provider.
11. Run cheap post-commit Health checks and apply any repair through PersistenceCoordinator.
12. Return the user-facing response with immediate action first and infrastructure hidden.

Pure Web may collapse these logical steps into one conversational turn. Durable Web may execute explicit provider reads/writes. The responsibility boundaries are identical.

## State precedence

1. newest direct user observation;
2. newest authoritative ActiveTask state;
3. current KitchenState records;
4. recent task Event when explicitly retrieved;
5. relevant Experience / learned pattern;
6. base Recipe;
7. older conversation or inference.

A newer correction invalidates conflicting older facts; do not average contradictions when one is explicitly corrected.

## Storage degradation

If the selected durable provider becomes unavailable:

- do not block a safe cooking action merely to repair persistence;
- retain the newest task authority in session context when possible;
- do not claim cross-session durability for uncommitted changes;
- route storage repair through Health/Persistence rather than Cooking;
- resume durable commits after the provider becomes healthy.
