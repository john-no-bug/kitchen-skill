# Kitchen Skill — v0.6 Web + Google Drive Persistence Vertical Slice

Status: first durable Web persistence slice layered on the existing Pure Web Live Cooking candidate  
Architecture baseline: frozen v0.4 + v0.5 interface/schema draft

## Current milestone

The repository now contains two deliberately separate Web deployments:

1. **Pure Web** — `WEB_CHAT + CONTEXT_ONLY`, still used by the existing regression harness.
2. **Web + Google Drive** — `WEB_CHAT + GoogleDriveProvider`, using a bounded Google Sheets-backed Kitchen store.

The purpose of the new slice is to validate one architecture claim:

> Live Cooking domain behavior can survive a fresh chat through durable shared storage without rewriting Cooking logic or loading full history.

## Preserved Pure Web baseline

The following remain unchanged by the persistence slice:

- `SKILL.md`
- `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`
- `modules/cooking/contract.md`
- `modules/cooking/logic.md`
- the four-scenario default regression harness in `tests/manifest.yaml`

The v0.5 Pure Web regression baseline passed all three required suite runs at 36/36 and is tracked separately from persistence validation.

## Added durable Web slice

- `runtime/web_persistent.md` — Web runtime semantics when an external persistent provider is available.
- `providers/google_drive.md` — Google Drive `StorageProvider` implementation profile using one native Google Sheet.
- `retrieval/web_google_drive.md` — bounded persistent Context Retriever.
- `persistence/web_durable.md` — durable PersistenceCoordinator and compatibility normalization from the existing Cooking result shape.
- `health/web_google_drive.md` — persistent-storage health/re-anchor behavior.
- `schemas/change_set.yaml` — semantic write intent.
- `schemas/storage_provider.yaml` — provider contract used by the slice.
- `schemas/google_drive_store.yaml` — provider-specific physical mapping; not a canonical domain schema.
- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_LIVE_COOKING.md` — deployable Web + Drive bundle.
- `tests/persistence/manifest.yaml` — persistence integration gate definition.
- `tests/persistence/01_google_drive_cross_session_resume.md` — candidate-visible cross-session scenario.
- `tests/persistence/expectations/01_google_drive_cross_session_resume.md` — evaluator-only expectations loaded after candidate transcript freeze.
- `tests/persistence/PROVIDER_SMOKE_TEST.md` — record of the real Drive/Sheets primitive smoke test performed during implementation.
- `demo/PERSISTENCE_SESSION_A_PROMPT.md` — writer/session-A integration prompt.
- `demo/PERSISTENCE_SESSION_B_PROMPT.md` — genuinely fresh reader/session-B integration prompt.

## Google Drive v1 store

The first provider uses **one native Google Sheet** as the Kitchen store. It keeps only the minimum persistence domains required by the vertical slice:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

Canonical objects remain provider-neutral. The Sheet is only a physical mapping. `payload_json` stores canonical records; small projection columns exist only to support bounded bootstrap/search and are updated in the same provider commit.

Normal Live Cooking retrieval does **not** read the whole Sheet. It normally loads:

- the tiny `META` projection;
- the one current `ACTIVE_TASK` row;
- only task-relevant `STATE` rows;
- at most 1–2 relevant `EXPERIENCE` rows;
- no `EVENTS` unless explicitly required.

## Write path

The write invariant remains:

`Cooking / Health -> ChangeSet -> PersistenceCoordinator -> GoogleDriveProvider`

The current Cooking module still emits its existing logical task/state/experience observations. `PersistenceCoordinator` contains a compatibility normalization step that turns that shape into a canonical `ChangeSet` before durable write. Provider APIs never enter Cooking logic.

## Failure behavior

If Drive is unavailable or a durable commit fails:

- current cooking assistance continues when safe;
- the response must not claim a durable save;
- pending changes remain session-level when possible;
- Health receives a storage-degraded signal;
- the system can temporarily behave like Pure Web rather than blocking the user.

## Validation status

A real Web-host Drive/Sheets smoke test has passed for the provider primitives used by this slice:

- native spreadsheet creation;
- one-batch tab/header initialization;
- bounded `META` range read;
- bounded STATE row search;
- one-batch `ACTIVE_TASK` + `META` revision update plus Event append;
- bounded readback of the updated ActiveTask and appended Event;
- cleanup of the temporary test spreadsheet.

This validates the physical provider operations, not the complete product behavior.

The v0.6 integration harness now separates candidate-visible scripts from evaluator-only expectations and requires two real conversations:

1. run `demo/PERSISTENCE_SESSION_A_PROMPT.md` in Session A;
2. carry only `TEST_COMMIT` and `TEST_STORE_URL` into a genuinely fresh conversation;
3. run `demo/PERSISTENCE_SESSION_B_PROMPT.md` in Session B;
4. Session B freezes B1/B2 candidate responses before loading evaluator expectations;
5. the temporary test store is deleted on a clean PASS or retained explicitly for debugging on failure.

**Chat A -> fresh Chat B recovery has not yet been executed and must not be reported as passed.** It is the current development gate before Shopping work begins.

## Architecture docs

- `docs/Kitchen_System_v0.4_Frozen_Architecture.md` remains the untouched rollback baseline.
- `docs/Kitchen_System_v0.5_Interface_and_Schema_Draft.md` remains the current formal interface/schema architecture.

The v0.6 label is an implementation milestone, not a replacement architecture document.
