# Kitchen Skill v0.7 Cross-Domain Integration — Session A (Shopping)

This is integration-test Session A for `john-no-bug/kitchen-skill`.

## Repository pinning

1. Inspect current `main` once at the start and set its exact 40-character HEAD as `TEST_COMMIT`.
2. From then on, read every repository file for this test pinned to `TEST_COMMIT`. Do not follow later main changes.
3. Read pinned:
   - `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING.md`
   - `modules/shopping/contract.md`
   - `modules/shopping/logic.md`
   - `persistence/web_durable.md`
   - `providers/google_drive.md`
   - `retrieval/web_google_drive.md`
   - `schemas/change_set.yaml`
   - `schemas/google_drive_store.yaml`
   - `tests/shopping/manifest.yaml`
   - `tests/shopping/01_purchase_to_cooking_continuity.md`
4. Do **not** read `tests/shopping/expectations/*` in Session A.

## Isolated test store

Create a new native Google Sheet used only for this run, titled like:

`Kitchen Skill Shopping Test - <short TEST_COMMIT>`

Initialize the existing `kitchen-skill-google-sheets-v1` physical layout only:

- META
- STATE
- ACTIVE_TASK
- EXPERIENCES
- EVENTS

Do not create a Shopping-specific tab. Do not touch production Kitchen stores.

Initialize META with compatible store marker/schema, global revision, null active_task_id, healthy status. STATE may begin with only its root metadata row; ground-beef inventory should not be pre-seeded for this test.

Canonical numeric inventory amounts written in this run must use v0.5 `Amount.mode` (`exact`/`approximate`) rather than an ad-hoc `precision` field.

## Candidate execution

Process exact Session A turns A1 and A2 from `tests/shopping/01_purchase_to_cooking_continuity.md` sequentially as separate user turns.

For each turn:

- apply the candidate bundle/domain behavior without exposing infrastructure;
- perform only bounded provider reads needed for validation/addressing;
- persist semantic changes through the documented ChangeSet -> PersistenceCoordinator -> provider path;
- do not read evaluator expectations.

A1 should establish compact Shopping operational state when meaningful.

A2 must complete the semantic purchase write before Session A ends. The purchase confirmation itself is the inventory capture; do not create a fake extra user turn for data entry.

For A2 labelled `500g`, canonical inventory should use `amount.mode=exact`, `value=500`, `unit=g` unless contradictory evidence appears.

## Handoff isolation

After A2 write success, verify only enough store state to ensure:

- purchased ground beef exists in canonical STATE;
- compact purchase Event exists;
- Shopping ActiveTask is cleared/completed from current continuity;
- META active_task_id is null.

Do not produce a state summary for Session B.

Return to the user exactly these two continuity values plus a one-line instruction to open a fresh conversation:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact temporary Sheet URL>`

Do not include Shopping transcript, inventory JSON, Event JSON, evaluator notes, or an ActiveTask summary in the handoff.
