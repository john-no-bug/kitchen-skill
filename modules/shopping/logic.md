# Shopping Logic — Quantity Fit and Purchase Capture

## Minimal state model

Maintain only sparse task state relevant to the current shopping decision:

- shopping goal/planned dish;
- target item;
- required/planned quantity when known;
- current relevant inventory when known;
- current candidates/package sizes;
- decision-changing storage/waste constraints;
- selected/purchased candidate;
- unresolved issues.

Do not preserve catalog browsing transcript as ActiveTask state.

## Package comparison

For package-size choice:

1. establish the planned required quantity if already supplied;
2. subtract reliable current inventory only when relevant;
3. compare candidate sizes against remaining need;
4. prefer lower likely waste when price/storage/future-use evidence does not favor the larger option;
5. state what missing fact would change the recommendation only if that fact is decision-changing.

Example:

- planned beef need: about 350 g;
- options: labelled 500 g or 1 kg;
- price is explicitly out of scope/unknown;
- no batch-cooking/freezing plan supplied.

Default recommendation: 500 g because it covers the need with substantially less surplus. Do not invent a unit-price argument.

## Purchase confirmation

When the user confirms a purchase:

```text
observe purchase
-> produce one ChangeSet
-> upsert inventory
-> append compact purchase Event
-> complete/clear Shopping ActiveTask
-> PersistenceCoordinator commits
```

Do not require a second inventory-entry interaction.

Suggested purchase Event payload fields for this slice:

- item ref/name;
- package Amount/label evidence;
- shopping task ref when available;
- optional planned-use note.

Do not store the full conversation.

## Canonical Amount semantics

Use the v0.5 Amount shape rather than an ad-hoc precision flag.

Examples:

```yaml
# package label/direct evidence
amount:
  mode: exact
  value: 500
  unit: g
```

```yaml
# approximate statement
amount:
  mode: approximate
  value: 500
  unit: g
```

Rules:

- `包装标的是500g` can support `mode: exact` for the labelled package quantity;
- `大概500g` remains `mode: approximate`;
- later Cooking use such as `大概用了120g` degrades the remaining arithmetic result to `mode: approximate` even if the purchased package quantity was exact;
- do not promote approximate information to exact without new evidence.

## Task completion

After confirmed purchase and successful semantic commit:

- Shopping ActiveTask no longer needs to remain current;
- clear `Meta.active_task_id`;
- retain current inventory as canonical state;
- retain the compact Event as history/cold data.

A future Cooking request should retrieve inventory from KitchenState, not revive the completed Shopping task.

## Response style

Give the recommendation/decision first, then the short reason. Do not expose ChangeSet, ActiveTask, tables, revisions, or provider mechanics unless the user explicitly asks about implementation.
