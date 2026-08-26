# Kitchen Skill — Web + Google Drive Shopping → Cooking

## Scope

This v0.7 bundle layers the first Shopping vertical slice on the already-validated Web + Google Drive Live Cooking persistence path.

Supported behavior in this bundle:

- shopping quantity/package comparison;
- low-friction purchase confirmation;
- canonical KitchenState inventory update;
- compact purchase Event append;
- Shopping ActiveTask completion;
- fresh-session Cooking retrieval of purchased inventory;
- existing Live Cooking behavior.

Do not add provider-specific logic to Cooking or Shopping. Google Drive is only the selected StorageProvider.

## Core invariants

- runtime is separate from storage;
- DomainModules never write StorageProvider directly;
- ContextRetriever is read-only;
- PersistenceCoordinator is the only semantic write gate;
- current direct observation outranks stored state;
- unknown is not absent/zero/false;
- precision never increases without evidence;
- normal context is bounded and does not scale with Event history;
- cross-domain handoff uses canonical state, not transcript replay.

## Store

Use the existing compatible Google Sheet store format:

`store_format = kitchen-skill-google-sheets-v1`

No new Shopping-specific table is introduced. Reuse:

- `META`;
- `STATE`;
- `ACTIVE_TASK`;
- `EXPERIENCES`;
- `EVENTS`.

Shopping purchase state belongs in `STATE.inventory`; a compact purchase observation may be appended to `EVENTS`.

## Routing and bootstrap

Every turn:

1. read only tiny META continuity data;
2. if an active task exists, read only the current ActiveTask row;
3. route from explicit current user intent first, then ActiveTask type/phase;
4. only after routing perform task-specific bounded retrieval.

Do not read STATE/EVENTS during bootstrap merely because they exist.

## Shopping

When the user asks which package to buy:

- consider planned required quantity;
- consider relevant current inventory;
- compare package fit and likely surplus/waste;
- consider price/value only when actually known;
- consider storage/freezing/future-use only when known or decision-changing;
- avoid unnecessary questions when a safe/useful default exists.

If planned beef need is about 350 g and the only known difference is 500 g vs 1 kg package size, prefer 500 g because it covers the need with less surplus. Do not invent price information.

### Purchase confirmation

If the user says they bought the package, treat that statement as the purchase observation.

Produce one semantic ChangeSet that may:

- upsert the inventory item at evidence-backed precision;
- append a compact `purchase_inventory` Event;
- clear/complete the Shopping ActiveTask;
- clear `META.active_task_id`;
- advance revision.

Only PersistenceCoordinator may commit it. Do not ask the user to enter the purchase again.

## Fresh Cooking after Shopping

A fresh conversation must not require the Shopping transcript.

If Shopping already completed:

1. bootstrap META; normally there is no current Shopping ActiveTask;
2. route the new explicit cooking request to Cooking;
3. retrieve only the inventory/equipment records relevant to that request;
4. do not load the purchase Event for normal cooking;
5. start a new Cooking ActiveTask through the normal PersistenceCoordinator path.

The purchased inventory record is the handoff.

## Live Cooking

Preserve existing behavior:

`safety > newest direct physical observation > current ActiveTask > current KitchenState > next 1–2 actions > relevant Experience > base Recipe > old conversation`.

Answer the immediate physical problem first, give sensory completion cues, locally re-plan deviations, and never repeat completed major steps as pending.

## Precision across modules

Example:

- Shopping purchase label says exactly 500 g beef;
- later Cooking user says approximately 120 g was used.

The remaining amount may be represented as approximately 380 g, but not exact 380 g, because the subtraction includes approximate evidence.

## Bounded retrieval

Normal Shopping/Cooking must not load full history.

Suggested limits:

- max state records: 12;
- max experiences: 2;
- max events: 0 by default;
- max recipes: 1.

Purchase Event history is not required for fresh Cooking continuity because current inventory is canonical state.

## Failure behavior

If durable storage fails:

- continue safe/useful shopping/cooking guidance when possible;
- never claim an unconfirmed durable save;
- retain pending logical changes in session context when possible;
- surface storage degradation to Health;
- do not make infrastructure repair more important than the current kitchen task.

## Architecture invisibility

Do not expose ActiveTask, ContextPack, ChangeSet, PersistenceCoordinator, revisions, sheet tabs, Monitor, Doctor, or provider mechanics in normal user-facing responses.
