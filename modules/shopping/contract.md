# Shopping Module Contract

## Responsibility

Help the user plan purchases and choose between concrete ingredient/product options using current kitchen state, planned use, storage/waste constraints, and relevant preferences/experience.

The v0.7 vertical slice exercises one narrow path:

`quantity need -> package comparison -> user confirms purchase -> canonical inventory update`.

Shopping does not implement provider APIs and does not maintain a separate inventory database.

## Input

- current TaskRequest/user shopping message;
- bounded ContextPack;
- optional `ActiveTask(type=shopping)`;
- only the current inventory/plans/preferences needed for the decision.

## Context requirements

Default retrieval for package selection:

- current Shopping ActiveTask when present;
- current quantity/availability of the item being considered;
- planned required quantity when known;
- storage/waste constraint only when material;
- at most one relevant prior Shopping/ingredient Experience;
- no Event history by default.

Do not load the whole pantry or shopping history for a two-package comparison.

## Output

Shopping should prefer the canonical durable shape:

```text
ModuleResult
  response
  changes: ChangeSet?
  completion
  health_signals?
```

On confirmed purchase, the ChangeSet may include:

- KitchenState inventory upsert/update;
- compact purchase Event append;
- Shopping ActiveTask completion/clear;
- Meta continuity update.

All writes flow through PersistenceCoordinator.

## Rules

- Ask only decision-changing questions.
- Consider quantity fit, planned dish fit, existing inventory, package size, storage capacity, freshness, price/value when actually known, waste risk, preferences, and relevant experience.
- Do not fabricate price, unit price, freshness, package contents, or storage constraints that were not observed/provided.
- Prefer the smallest practical purchase when extra quantity would mainly create waste and no contrary evidence exists.
- A user statement such as `买500g这包了` is already a purchase observation; do not ask them to enter it again into inventory.
- Package-label quantity may be stored at the precision supported by that label/direct observation.
- Purchase completion should leave canonical KitchenState usable by another module in a fresh conversation.
- Domain logic must not call Drive/Sheets directly.
