# Kitchen Skill v0.7 Cross-Domain Integration — Session B (Fresh Cooking)

This must run in a **genuinely fresh conversation**.

Before this prompt is executed, the user must provide exactly:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact temporary Google Sheet URL>`

Do not request or accept Session A transcript, inventory/state summary, purchase Event, ActiveTask JSON, evaluator notes, or Session A evidence comment contents from the user. If such state content is provided in the handoff, mark the run invalid with `harness_defect`.

## Repository pinning

Use exactly `TEST_COMMIT`. Do not follow current main if it differs.

Read pinned:

- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING.md`
- `modules/cooking/contract.md`
- `modules/cooking/logic.md`
- `modules/shopping/contract.md`
- `modules/shopping/logic.md`
- `persistence/web_durable.md`
- `providers/google_drive.md`
- `retrieval/web_google_drive.md`
- `schemas/change_set.yaml`
- `tests/shopping/manifest.yaml`
- `tests/shopping/01_purchase_to_cooking_continuity.md`

Do **not** read `tests/shopping/expectations/*` until B1 and B2 responses are frozen.

Critically, do **not** read Issue #3 comments before B1/B2 are frozen. Session A writes an evaluator-only frozen evidence comment there, and reading it during candidate generation would invalidate fresh-session isolation.

## Store isolation and bootstrap

Use exactly `TEST_STORE_URL`. Do not search for/switch to another store.

Before B1:

1. verify the store marker with a tiny META read;
2. bootstrap only META plus current ActiveTask if META points to one;
3. do not read EVENTS during normal bootstrap;
4. route B1 from the explicit Cooking request;
5. only then retrieve task-specific relevant STATE rows, including ground beef.

The previous Shopping conversation is unavailable by design.

## Candidate execution

Process B1 and B2 exact user messages sequentially.

### B1

Generate the Cooking response from the current B1 observation plus bounded persisted state. Do not retrieve purchase EVENTS or Issue #3 evidence for normal candidate generation. Persist a new Cooking ActiveTask when meaningful through PersistenceCoordinator/provider before B2.

### B2

Use the exact B2 message. Apply the approximate consumption observation through semantic persistence, preserving canonical Amount uncertainty: if the store has `amount.mode=exact, value=500 g` and the user says approximately 120 g was used, remaining inventory must become `amount.mode=approximate` around 380 g, never exact 380 g.

Produce current Live Cooking guidance. Persist B2 changes before evaluation.

Do not rewrite B1 after seeing B2.

## Freeze and evaluator-only evidence phase

After the B2 provider write:

1. freeze B1/B2 user-facing responses;
2. record actual provider reads/writes;
3. only now read `tests/shopping/expectations/01_purchase_to_cooking_continuity.md` pinned to TEST_COMMIT;
4. only now fetch Issue #3 comments and locate exactly one `Session A frozen evidence` comment matching both TEST_COMMIT and TEST_STORE_URL;
5. if the matching Session A evidence comment is missing or ambiguous, overall result is `FAIL`, class `harness_defect`, and the store must be retained;
6. evaluate Session A criteria from the frozen Session A evidence comment plus bounded durable store evidence;
7. evaluate Session B criteria from frozen B1/B2 responses plus bounded durable store evidence;
8. do not regenerate any candidate response to improve the score.

The Session A evidence comment is evaluator-only evidence. Its contents must never influence B1/B2 candidate generation.

## Durable test reporting — mandatory

Before deleting or modifying the test store for cleanup, write one complete frozen evaluation as a comment to:

`john-no-bug/kitchen-skill` Issue #3

The comment must include:

- TEST_COMMIT;
- TEST_STORE_URL;
- overall PASS/FAIL;
- every criterion result;
- failure class for every failure;
- frozen B1/B2 responses;
- candidate-phase bounded reads;
- the Session A evidence comment URL/ID used during evaluator phase;
- explicit confirmation that the Session A evidence comment and evaluator expectations were not read before B1/B2 freeze;
- A2 purchase write evidence, including canonical `Amount.mode`;
- B1/B2 durable write evidence;
- proof Shopping task was cleared before Session B;
- latest ground-beef `Amount.mode`/value after B2.

If GitHub result writeback fails, overall result is `FAIL`, class `harness_defect`; retain the store and do not close Issue #3.

## Cleanup

If evaluation PASS and Issue #3 result comment exists:

1. delete the temporary Sheet;
2. verify it is unavailable;
3. append a cleanup receipt to Issue #3;
4. close Issue #3 as completed.

If any required criterion fails, retain the Sheet for debugging, explicitly report `TEST_STORE_RETAINED_FOR_DEBUGGING`, and keep Issue #3 open.

Do not modify production Kitchen data or candidate repository files during the test.
