# Kitchen Skill v0.8.1 Release Gate — Session B (Fresh Cooking + Failed Write Recovery)

This must run in a **genuinely fresh conversation**.

Before execution, the user must provide exactly:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact valid temporary Google Sheet URL>`
- `DEAD_TARGET_URL: <exact deleted sacrificial Google Sheet URL>`

Do not request or accept Session A transcript, state/inventory summary, Event payload, ActiveTask payload, evaluator notes, or Session A escrow contents from the user. Extra state content invalidates the run with `harness_defect`.

## Repository pinning

Use exactly TEST_COMMIT for all repository reads.

Read pinned before candidate execution:

- `README.md`
- `tests/VALIDATION_REGISTRY.yaml`
- `dist/deployments.yaml`
- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`
- `modules/cooking/contract.md`
- `modules/cooking/logic.md`
- `modules/shopping/contract.md`
- `modules/shopping/logic.md`
- `persistence/web_durable.md`
- `providers/google_drive.md`
- `retrieval/web_google_drive.md`
- `runtime/web_persistent.md`
- `health/web_google_drive.md`
- `schemas/change_set.yaml`
- `schemas/google_drive_store.yaml`
- `tests/release/manifest.yaml`
- `tests/release/01_current_head_composite_regression.md`

Do **not** read:

- `tests/release/expectations/*`;
- Issue #7 comments;
- Session A escrow;

until B1-B4 responses and candidate/provider traces are frozen.

## Store isolation

Use exactly TEST_STORE_URL as the valid Kitchen store. Do not search for another Kitchen store.

Use exactly DEAD_TARGET_URL only for the one B3 failed provider commit. The dead target is harness transport only and must never enter canonical payloads or user-facing cooking guidance.

## B1 — fresh Cooking bootstrap

Process exact B1 message from the candidate script.

Before response:

1. bounded read `META` only for bootstrap;
2. because Shopping should have been cleared, no current Shopping ActiveTask should be revived;
3. route explicit current request to Cooking;
4. only then bounded-retrieve relevant STATE, including ground beef;
5. normal candidate generation reads zero EVENTS;
6. generate/freeze B1;
7. persist a compact new Cooking ActiveTask through PersistenceCoordinator/provider before B2.

Record actual provider reads/writes and revision evidence.

## B2 — approximate consumption

Process exact B2 message.

Use current direct observation as authoritative. Persist approximate consumption through semantic persistence.

If inventory before B2 is exact 500 g and the user reports approximately 120 g used, remaining inventory must be canonical `Amount.mode=approximate` around 380 g, never exact 380 g.

Generate/freeze B2 and complete its valid-store durable write/readback before B3. Record the resulting valid-store global revision; call it `PRE_B3_REVISION`.

## B3 — real failed durable write

Process exact B3 message.

Execution order is mandatory:

1. bounded-read valid META/current ActiveTask needed for current reasoning;
2. apply newest direct observation: beef browned, onion already added, slight sticking;
3. generate/freeze the user-facing B3 response;
4. freeze the semantic B3 ChangeSet / normalized provider mutation intent;
5. only then route the exact provider commit batch for that B3 semantic change to DEAD_TARGET_URL instead of TEST_STORE_URL;
6. record the real provider-boundary failure (unavailable/not-found such as 404);
7. do not issue a success receipt and do not perform a substitute B3 write to the valid store;
8. retain the B3 semantic change as session-pending;
9. bounded-read valid META and current ActiveTask after failure;
10. prove valid META revision remains PRE_B3_REVISION and current durable task remains pre-B3, with no partial B3 mutation.

The B3 user-facing response must remain useful cooking guidance and must not mention storage internals or claim a durable save.

## B4 — restore/retry

Process exact B4 message `继续。`.

Before generating B4:

1. restore provider target to TEST_STORE_URL;
2. bounded-refresh valid META + only affected current record(s);
3. re-evaluate/rebase the retained B3 pending semantic change against refreshed current state;
4. retry it through PersistenceCoordinator -> StorageProvider;
5. verify durable commit succeeds;
6. verify global revision advances exactly once from PRE_B3_REVISION;
7. verify durable current Cooking task now reflects the newest B3 facts (beef browned, onion already added, slight sticking, or semantically equivalent representation);
8. generate/freeze B4 from recovered newest state without repeating beef browning or adding onion again.

No candidate phase may load EVENTS/history.

## Freeze and evaluator-only phase

Only after B1-B4 responses and all candidate/provider traces are frozen:

1. read pinned `tests/release/expectations/01_current_head_composite_regression.md`;
2. fetch Issue #7 comments;
3. locate exactly one matching `Release Session A frozen evidence` comment for TEST_COMMIT + TEST_STORE_URL + DEAD_TARGET_URL;
4. locate static-validation evidence for TEST_COMMIT from the development session;
5. evaluate validation-registry blob guards at TEST_COMMIT;
6. if any required escrow/static evidence is missing or ambiguous, overall FAIL with `harness_defect`/`static_validation` as appropriate;
7. evaluator may now bounded-read purchase Event/final current records needed for audit;
8. do not regenerate any candidate response or provider trace.

## Durable result reporting — mandatory

Before deleting TEST_STORE_URL, add one complete frozen result comment to Issue #7 including:

- TEST_COMMIT;
- TEST_STORE_URL;
- DEAD_TARGET_URL;
- overall PASS/FAIL;
- every evaluator criterion result and failure class for failures;
- static-validation evidence comment id/reference;
- registry blob-guard results;
- frozen A1/A2 evidence comment id/reference;
- frozen B1/B2/B3/B4 responses;
- ordered candidate-phase provider reads/writes;
- B2 precision result and PRE_B3_REVISION;
- real B3 dead-target failure evidence;
- proof no B3 revision advance/partial valid-store state;
- session-pending B3 semantic state;
- bounded B4 retry/rebase evidence;
- final revision and recovered durable task state;
- confirmation candidate generation read zero EVENTS;
- confirmation Issue comments/expectations were unread until freeze.

If result writeback fails, overall FAIL with `harness_defect`; retain TEST_STORE_URL.

## Cleanup

If all criteria PASS and the frozen result comment exists:

1. permanently delete TEST_STORE_URL;
2. verify the original valid store is unavailable/not-found;
3. append a cleanup receipt to Issue #7;
4. **leave Issue #7 open** for the development session to perform the final metadata-only release freeze/update and release/tag.

If any criterion fails:

- retain TEST_STORE_URL for debugging;
- append explicit `TEST_STORE_RETAINED_FOR_DEBUGGING` evidence;
- keep Issue #7 open.

Do not modify repository candidate/release files or production Kitchen data during this test session.
