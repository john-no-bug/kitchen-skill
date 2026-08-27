# Kitchen Skill v0.8 — Event/Experience Compaction + Long-History Gate Runner

Run this in one **dedicated fresh test conversation** for `john-no-bug/kitchen-skill`.

The goal is to execute the real Google Sheets integration gate, not to review the test statically.

## 1. Pin repository revision

At the start:

1. inspect current `main` once;
2. set the exact 40-character HEAD as `TEST_COMMIT`;
3. from then on read all candidate/test files pinned to TEST_COMMIT;
4. do not follow later main changes.

Read pinned before candidate execution:

- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`
- `health/event_experience_compaction.md`
- `retrieval/web_google_drive.md`
- `persistence/web_durable.md`
- `providers/google_drive.md`
- `health/web_google_drive.md`
- `modules/cooking/contract.md`
- `modules/cooking/logic.md`
- `modules/shopping/contract.md`
- `modules/shopping/logic.md`
- `schemas/google_drive_store.yaml`
- `tests/history/manifest.yaml`
- `tests/history/01_long_history_compaction_and_bounded_context.md`

Do **not** read `tests/history/expectations/*` yet.

## 2. Create isolated test store

Create one native Google Sheet titled:

`Kitchen Skill History Test - <short TEST_COMMIT>`

Use only the existing v1 tabs:

- META
- STATE
- ACTIVE_TASK
- EXPERIENCES
- EVENTS

Do not touch production Kitchen stores and do not create archive/compaction/vector/index tables.

Initialize the existing headers/marker/schema. Create stable test current state/equipment required by the scenario.

## 3. Seed the small-history baseline

Follow `tests/history/01_long_history_compaction_and_bounded_context.md` exactly.

Relevant canonical records and all 20 compactable Events must be real static canonical payloads with stable IDs.

Seed:

- 3 initial compatible Events for `frozen_ground_beef:supor_green_pot`;
- relevant Cooking Experience `exp-frozen-beef-supor-pot`, evidence_count 3, evidence refs to those 3 Events;
- relevant Shopping Experience `exp-shopping-beef-350g`;
- META `last_compaction_at` after the third initial Event but before the future 17 matching Events.

Do not seed the bulk noise history yet.

## 4. Baseline probes C0 / S0

Process the exact C0 and S0 messages from the candidate script as normal retrieval probes.

For each probe:

1. perform normal tiny bootstrap/routing;
2. perform normal task-specific bounded retrieval;
3. generate/freeze the user-facing response;
4. record the exact provider read trace;
5. record selected canonical persisted record IDs/types;
6. record counts of selected STATE / Experience / Event records;
7. serialize only selected persisted canonical records deterministically as compact JSON (sorted keys, stable separators) and compute exact UTF-8 byte length.

Use local code execution for the deterministic serialization/byte count if available. Do not estimate byte length. If exact measurement cannot be produced, classify the run `harness_defect` rather than inventing a number.

Do not mutate Kitchen state merely to measure context.

Freeze C0/S0 responses, selections, traces, and measurements.

## 5. Grow cold history

Append the required 17 new compatible canonical Events as static rows after `last_compaction_at`.

Then grow the physical cold-history fixture to the manifest targets:

- total Event data rows = 2000;
- total Experience data rows >= 122;
- at least 120 irrelevant/superseded Experience rows;
- at least 8 superficially similar superseded/noise Experiences.

### Efficient fixture rule

To avoid thousands of connector calls, the **irrelevant bulk fixture rows only** may be generated with Google Sheets `ARRAYFORMULA` / `SEQUENCE` or chunked `pasteData`/batch operations, provided their visible values form valid compact Event/Experience-like rows and do not contain the exact compactable key.

This formula/paste fixture is harness-only scale data. It must not be cited as proof of production Event append semantics.

The 20 compactable Events and the two relevant Experiences must remain real static canonical rows.

Freeze the bulk-write trace and verify sentinels/bounds showing 2000 Event data rows and >=122 Experience data rows exist.

## 6. Run explicit M1 compaction

Use the v0.8 Health compaction profile.

Required behavior:

1. read META / `last_compaction_at`;
2. select matching Event candidates with exact marker `frozen_ground_beef:supor_green_pot` after the watermark;
3. only bounded candidate outputs enter reasoning: <=64 Event payloads and <=8 existing Experience payloads;
4. identify exactly 17 new compatible unique Event refs;
5. read current `exp-frozen-beef-supor-pot` canonical payload;
6. build a Health RepairPlan / semantic ChangeSet;
7. commit only through PersistenceCoordinator -> GoogleDriveProvider;
8. preserve Experience id/key;
9. change evidence_count 3 -> 20;
10. keep `evidence_event_refs` <=8;
11. update `Meta.last_compaction_at` in the successful commit;
12. do not delete/rewrite EVENTS.

Freeze the candidate-selection evidence, RepairPlan/ChangeSet summary, provider write trace, revision movement, and bounded readback.

## 7. Long-history probes C1 / S1

Repeat the exact C0 and S0 user messages.

For each:

- run normal bootstrap/retrieval only;
- do not read EVENTS for candidate generation;
- freeze response/provider trace/selected records;
- compute the same deterministic selected persisted-record UTF-8 byte measurement.

Explicitly record whether any `evidence_event_refs` were dereferenced. Expected: no.

## 8. Freeze before evaluator

At this point freeze all of the following:

- C0/S0/C1/S1 user-facing responses;
- all four normal-retrieval provider traces;
- baseline/post selected-record IDs/counts/byte measurements;
- bulk-history write/sentinel evidence;
- M1 compaction candidate set and bounded-input counts;
- M1 RepairPlan/ChangeSet/provider write trace;
- post-compaction Experience/META evidence;
- proof supporting Events remain present.

Only now read:

`tests/history/expectations/01_long_history_compaction_and_bounded_context.md`

Do not regenerate any candidate response, selection, compaction decision, or measurement after reading evaluator expectations.

## 9. Evaluator-only audits

Perform only bounded audits needed to judge criteria, including:

- Event row 2001 sentinel (header + 2000 data rows);
- one initial and one late compatible Event sentinel;
- target Experience canonical payload;
- representative noise/superseded Experience evidence;
- META watermark/revision;
- sheet metadata proving only five existing tabs;
- pinned domain source/provider-separation checks.

Do not load the entire 2000-row Event history into model context during evaluation.

## 10. Durable result reporting — mandatory

Before cleanup, post one complete frozen result to:

`john-no-bug/kitchen-skill` Issue #6

The comment must include:

- TEST_COMMIT;
- TEST_STORE_URL;
- overall PASS/FAIL;
- every criterion result + failure class;
- C0/S0/C1/S1 frozen responses;
- baseline/post ContextPack selected-record counts + exact byte measurements;
- history row counts;
- M1 bounded candidate counts;
- target Experience before/after evidence_count and evidence-ref count;
- proof Events remained present;
- normal-retrieval provider traces showing zero Event reads;
- M1 write path/revision/watermark evidence;
- explicit confirmation expectations were unread until freeze.

If Issue #6 reporting fails: overall FAIL, class `harness_defect`, retain the store, keep Issue #6 open.

## 11. Cleanup

If all required criteria PASS and the frozen result comment exists:

1. delete the temporary test Sheet;
2. verify it is unavailable/not-found;
3. append cleanup receipt to Issue #6;
4. close Issue #6 as completed.

If any required criterion FAILS:

- retain the Sheet for debugging;
- report `TEST_STORE_RETAINED_FOR_DEBUGGING`;
- leave Issue #6 open.

Do not modify production Kitchen data or candidate repository files during the test.
