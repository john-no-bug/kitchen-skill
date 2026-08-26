# Kernel — Web Kitchen Orchestration

## Scope

This kernel orchestrates the current Web vertical slices across either:

- `WEB_CHAT + CONTEXT_ONLY`; or
- `WEB_CHAT + a compatible durable StorageProvider`.

Current domain modules exercised by the implementation are:

- Cooking;
- Shopping.

Runtime and storage remain separate. The selected provider may change without changing domain logic.

## Invariants

1. Current user observation outranks stored state and old conversation.
2. Unknown is not false, absent, zero, or completed.
3. Approximate values do not become exact without new evidence.
4. Domain logic never writes a StorageProvider directly.
5. ContextRetriever is read-only and normal per-turn reasoning is bounded.
6. PersistenceCoordinator is the semantic write gate.
7. Durable success is claimed only after a durable provider confirms the commit.
8. Architecture concepts do not leak into normal user-facing kitchen guidance.
9. Safety and current physical reality outrank recipe/task plans.
10. Domain modules communicate through canonical state/contracts, not hidden transcript coupling.

## Per-turn orchestration

1. Create the current `TaskRequest` from the newest user message.
2. Read runtime capabilities; resolve storage separately.
3. Ask ContextRetriever for tiny routing bootstrap state.
4. Select the DomainModule using explicit current intent first, then current ActiveTask type/phase.
5. Ask the selected module for its retrieval requirements.
6. Build a bounded ContextPack through the selected Retriever implementation.
7. Run a cheap preflight Health inspection when continuity/freshness may matter.
8. Pass the request and ContextPack to the selected domain logic.
9. Normalize any requested changes into a `ChangeSet` when compatibility shorthand is used.
10. If changes exist, pass them to PersistenceCoordinator; only it may write the provider.
11. Run cheap post-commit Health checks and apply any repair through PersistenceCoordinator.
12. Return the user-facing response with the immediate decision/action first and infrastructure hidden.

Pure Web may collapse these logical steps into one conversational turn. Durable Web may execute explicit provider reads/writes. The responsibility boundaries are identical.

## Routing

Use, in order:

1. explicit current user request;
2. current ActiveTask type/phase from bootstrap;
3. newest direct observation;
4. fallback intent classification.

Examples:

- during an active Shopping task, `我买500g这包了` remains Shopping and should become a purchase observation/state update;
- in a fresh conversation after Shopping has completed and `META.active_task_id` is null, `我要开始做番茄牛肉意面` routes to Cooking and retrieves relevant inventory from KitchenState;
- Cooking must not need the Shopping transcript or purchase Event to see current purchased inventory.

A short subquestion may be handled without changing the current ActiveTask type when appropriate.

## State precedence

1. newest direct user observation;
2. newest authoritative ActiveTask state;
3. current KitchenState records;
4. recent task Event when explicitly retrieved;
5. relevant Experience / learned pattern;
6. base Recipe/plan;
7. older conversation or inference.

A newer correction invalidates conflicting older facts; do not average contradictions when one is explicitly corrected.

## Cross-domain continuity

The normal handoff between modules is canonical state, not transcript replay.

Example:

`Shopping confirms 500 g beef purchase`
-> `PersistenceCoordinator commits inventory + purchase Event and clears Shopping ActiveTask`
-> fresh Cooking request
-> `Retriever reads current beef inventory from STATE`
-> `Cooking starts a new ActiveTask`.

Events remain cold history and are not required for this handoff.

## Storage degradation

If the selected durable provider becomes unavailable:

- do not block safe/useful cooking or shopping guidance merely to repair persistence;
- retain the newest task authority/pending changes in session context when possible;
- do not claim cross-session durability for uncommitted changes;
- route storage repair through Health/Persistence rather than DomainModule;
- resume durable commits after the provider becomes healthy.
