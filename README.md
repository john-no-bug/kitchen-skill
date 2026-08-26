# Kitchen Skill — v0.7 Shopping → Canonical State → Cooking

Status: first cross-domain vertical slice layered on the validated v0.6 Web + Google Drive persistence path  
Architecture baseline: frozen v0.4 + v0.5 interface/schema draft

## Validated baselines

### v0.5 — Pure Web Live Cooking

The frozen Pure Web candidate remains unchanged and passed all three required regression suite runs at 36/36.

Preserved files include:

- `SKILL.md`
- `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`
- `modules/cooking/contract.md`
- `modules/cooking/logic.md`
- `tests/manifest.yaml`

### v0.6 — Web + Google Drive persistence

The real two-conversation persistence gate passed at commit `354ba039d8ce56edec7789f01541d3899481c576` and is recorded in GitHub Issue #2.

Validated behavior includes:

- fresh Chat B recovery from Drive without Chat A transcript;
- bounded META + ActiveTask bootstrap;
- current observation overriding persisted stale physical state;
- B1/B2 durable ActiveTask writeback;
- no full Event/history loading for normal Cooking;
- approximate arithmetic remaining approximate;
- result writeback/cleanup harness behavior.

The provider-failure injection criterion was intentionally not exercised by that normal continuity gate and remains a later degradation-test item.

## v0.7 current milestone

The next architecture claim is cross-domain continuity:

> Shopping and Cooking can cooperate through canonical KitchenState rather than shared chat history or provider-specific coupling.

The minimal path is:

`Shopping quantity need`
-> `package choice`
-> `purchase confirmation`
-> `KitchenState inventory + purchase Event`
-> `Shopping ActiveTask cleared`
-> fresh `Cooking` request
-> bounded inventory retrieval from STATE
-> new Cooking ActiveTask.

## New Shopping slice

- `modules/shopping/contract.md`
- `modules/shopping/logic.md`
- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING.md`

Shopping uses the existing canonical contracts. It emits `ChangeSet` directly and never calls Google Drive/Sheets.

No new provider table was added. The same Google Drive store remains:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

Confirmed purchases update `STATE.inventory`; compact purchase history is appended to `EVENTS`.

## Cross-domain write/read path

Write:

`Shopping -> ChangeSet -> PersistenceCoordinator -> GoogleDriveProvider`

Read in a fresh Cooking conversation:

`TaskRequest -> bounded Retriever -> KitchenState inventory -> Cooking`

The purchase Event is not required for normal Cooking continuity.

## Precision test

The v0.7 gate deliberately spans modules:

- Shopping records a labelled 500 g beef package;
- fresh Cooking later receives the direct observation `大概用了120g`;
- PersistenceCoordinator must produce approximately 380 g remaining, not exact 380 g.

This proves new evidence may support precision while later uncertain arithmetic correctly degrades it.

## v0.7 integration harness

- `tests/shopping/manifest.yaml`
- `tests/shopping/01_purchase_to_cooking_continuity.md`
- `tests/shopping/expectations/01_purchase_to_cooking_continuity.md`
- `demo/SHOPPING_SESSION_A_PROMPT.md`
- `demo/SHOPPING_SESSION_B_PROMPT.md`

Tracking gate: GitHub Issue #3.

The harness uses a real temporary Google Sheet and two genuinely separate conversations. Session B receives only `TEST_COMMIT` and `TEST_STORE_URL`; it must not receive Shopping transcript/state/Event content.

## Persistence/provider notes

The v0.7 Shopping slice does not expand the Drive physical schema. `providers/google_drive.md`, the canonical v0.5 architecture draft, and the existing provider-neutral contracts remain authoritative.

PersistenceCoordinator now documents Shopping purchase commit semantics, but there is still one semantic write gate.

## Next after v0.7 gate

If the real Shopping -> fresh Cooking gate passes:

1. add a focused provider-degradation/failure-injection suite covering the v0.6 `NOT_EXERCISED` durability-failure behavior;
2. then proceed to durable Event/Experience compaction/long-history validation before widening provider support.

Do not expand Drive schema, add a vector database, or implement another provider merely because Shopping exists.

## Architecture docs

- `docs/Kitchen_System_v0.4_Frozen_Architecture.md` — untouched rollback baseline.
- `docs/Kitchen_System_v0.5_Interface_and_Schema_Draft.md` — current formal interface/schema architecture.

The v0.7 label is an implementation milestone, not a replacement architecture document.
