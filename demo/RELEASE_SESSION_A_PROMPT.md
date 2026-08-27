# Kitchen Skill v0.8.1 Release Gate — Session A (Shopping + Test Setup)

This is Session A of the current-HEAD composite release regression for `john-no-bug/kitchen-skill`.

## Repository pinning

1. Inspect current `main` exactly once and set its 40-character HEAD as `TEST_COMMIT`.
2. From then on, read every repository file pinned to TEST_COMMIT. Do not follow later changes to main.
3. Read pinned:
   - `README.md`
   - `tests/VALIDATION_REGISTRY.yaml`
   - `dist/deployments.yaml`
   - `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`
   - `modules/shopping/contract.md`
   - `modules/shopping/logic.md`
   - `persistence/web_durable.md`
   - `providers/google_drive.md`
   - `retrieval/web_google_drive.md`
   - `schemas/change_set.yaml`
   - `schemas/google_drive_store.yaml`
   - `tests/release/manifest.yaml`
   - `tests/release/01_current_head_composite_regression.md`
4. Do **not** read `tests/release/expectations/*`.
5. Do not read Issue #7 comments before Session A candidate responses are frozen; previous release-development comments are not candidate input.

## Valid isolated Kitchen store

Create a new native Google Sheet used only for this run, titled like:

`Kitchen Skill Release Test - <short TEST_COMMIT>`

Initialize exactly the existing `kitchen-skill-google-sheets-v1` physical profile:

- META
- STATE
- ACTIVE_TASK
- EXPERIENCES
- EVENTS

No extra provider table is allowed.

Initialize META with compatible marker/schema, `global_revision=1`, `active_task_id=null`, healthy status. STATE may start with only its root record. Do not pre-seed ground beef.

Call this URL `TEST_STORE_URL`.

## Sacrificial dead target

Create a second native Google Sheet titled like:

`Kitchen Skill Release Dead Target - <short TEST_COMMIT>`

Record its exact URL as `DEAD_TARGET_URL`, then permanently delete it before A1 candidate execution.

Perform one bounded read/probe against DEAD_TARGET_URL after deletion and record the real provider-boundary unavailable/not-found evidence. Never reuse the valid Kitchen store as the dead target.

The dead-target URL/error is harness-only and must never enter canonical Kitchen payloads.

## Candidate execution

Process exact A1 and A2 messages from `tests/release/01_current_head_composite_regression.md` sequentially.

For both turns:

- use the v0.8 candidate bundle/domain behavior;
- expose no infrastructure in user-facing responses;
- perform only bounded provider reads needed for the current turn;
- persist semantic changes through ChangeSet -> PersistenceCoordinator -> StorageProvider;
- do not read evaluator expectations.

### A1

Generate/freeze the exact A1 user-facing response before A2.

When meaningful, persist a compact `ActiveTask(type=shopping)` through the normal semantic path. Record actual reads/writes and one bounded readback of current META/Shopping task for later evaluator evidence.

### A2

Generate/freeze the exact A2 user-facing response before evidence reporting.

Treat purchase confirmation itself as the inventory observation; do not fabricate another user turn for inventory entry.

For the labelled package, canonical ground-beef inventory must use v0.5 Amount semantics:

`amount.mode=exact`, `value=500`, `unit=g`

unless contradictory evidence appears.

Complete one semantic purchase commit that, as applicable:

- upserts the stable inventory record;
- appends one compact `purchase_inventory` Event;
- clears/completes Shopping ActiveTask;
- sets `META.active_task_id=null`;
- advances global revision.

Record the normalized A2 ChangeSet intent, PersistenceCoordinator validation/normalization, provider mutation batch summary, provider success, and bounded readback evidence.

## Session A frozen evidence escrow — mandatory

After A2 durable write/readback succeeds and before returning continuity values, add exactly one non-evaluative comment to GitHub Issue #7 with a heading like:

`## Release Session A frozen evidence — <short TEST_COMMIT>`

It must include:

- TEST_COMMIT;
- TEST_STORE_URL;
- DEAD_TARGET_URL;
- dead-target deletion + bounded unavailable/not-found probe evidence;
- exact frozen A1 response;
- exact frozen A2 response;
- candidate-phase bounded reads/writes;
- compact A1 Shopping ActiveTask readback sufficient to audit no transcript dump;
- A2 semantic ChangeSet/coordinator/provider write-path evidence;
- canonical ground-beef exact 500 g readback;
- compact purchase Event evidence;
- proof Shopping ActiveTask cleared and `META.active_task_id=null` before handoff;
- `EVALUATOR_EXPECTATIONS_READ: false`.

This escrow must contain no evaluator expectations, scores, PASS/FAIL judgments, or Session B instructions beyond identifiers.

If the evidence comment cannot be durably written, mark the run invalid/FAIL with `harness_defect`, retain TEST_STORE_URL, and do not proceed to normal handoff.

## Handoff isolation

After the escrow comment exists, return to the user exactly:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact valid Sheet URL>`
- `DEAD_TARGET_URL: <exact deleted sacrificial Sheet URL>`

plus one short instruction to open a genuinely fresh conversation and run `demo/RELEASE_SESSION_B_PROMPT.md`.

Do not include Session A transcript, inventory JSON, Event JSON, ActiveTask JSON, escrow contents, evaluator notes, or state summary in the handoff.
