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

## Candidate execution and freeze discipline

Process exact Session A turns A1 and A2 from `tests/shopping/01_purchase_to_cooking_continuity.md` sequentially as separate user turns.

For each turn:

- apply the candidate bundle/domain behavior without exposing infrastructure;
- perform only bounded provider reads needed for validation/addressing;
- persist semantic changes through the documented ChangeSet -> PersistenceCoordinator -> provider path;
- do not read evaluator expectations.

### A1

Generate the Shopping response and freeze it before A2. Do not rewrite it later.

After the A1 semantic write succeeds:

1. record the candidate-phase provider reads/writes actually performed;
2. do a bounded readback of META plus the one current ACTIVE_TASK row;
3. retain the compact A1 Shopping ActiveTask payload/projection as test evidence so its operational compactness can be evaluated later;
4. do not evaluate or score A1.

A1 should establish compact Shopping operational state when meaningful.

### A2

Generate the A2 Shopping response and freeze it before any handoff/evidence reporting.

A2 must complete the semantic purchase write before Session A ends. The purchase confirmation itself is the inventory capture; do not create a fake extra user turn for data entry.

For A2 labelled `500g`, canonical inventory should use `amount.mode=exact`, `value=500`, `unit=g` unless contradictory evidence appears.

Record, without evaluator judgment:

- the semantic ChangeSet intent emitted for A2;
- the fact that PersistenceCoordinator validated/normalized it before provider commit;
- the actual provider mutation batch targets/operation summary;
- provider success/readback evidence for the purchased inventory, purchase Event, task clear, and META revision.

## Durable Session A evidence escrow — mandatory

After A2 write/readback succeeds and **before** returning the handoff values, add one comment to `john-no-bug/kitchen-skill` Issue #3 titled like:

`## Session A frozen evidence — <short TEST_COMMIT>`

The comment must include:

- `TEST_COMMIT`;
- `TEST_STORE_URL`;
- the exact frozen A1 candidate response;
- the exact frozen A2 candidate response;
- candidate-phase bounded provider reads/writes for A1/A2;
- the bounded A1 compact Shopping ActiveTask readback (enough to audit compactness; not a chat transcript);
- A2 semantic ChangeSet summary and PersistenceCoordinator/provider write-path evidence;
- A2 canonical inventory readback including `Amount.mode`;
- compact purchase Event readback/evidence;
- proof the Shopping ActiveTask was cleared and `META.active_task_id=null` before handoff;
- the explicit statement `EVALUATOR_EXPECTATIONS_READ: false`.

This evidence comment is evaluator escrow only. It must contain **no evaluator expectations, no scores, and no PASS/FAIL judgments**.

If the Session A evidence comment cannot be durably written to Issue #3:

- mark Session A `FAIL` with class `harness_defect`;
- retain the temporary store;
- do not proceed to the normal Session B handoff.

## Handoff isolation

After the evidence comment is durably written, return to the user exactly these two continuity values plus a one-line instruction to open a fresh conversation:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact temporary Sheet URL>`

Do not include Shopping transcript, inventory JSON, Event JSON, evaluator notes, ActiveTask summary, or the Issue #3 evidence comment contents in the user handoff.

The fresh Session B must remain unable to use Session A evidence for candidate generation; the Session B prompt forbids reading Issue #3 comments until B1/B2 are frozen.
