# Kitchen Skill v0.6 Persistence Integration — Session B

This must run in a **genuinely fresh conversation**. It is integration-test Session B (reader/resumer) for `john-no-bug/kitchen-skill`.

Before this prompt is executed, the user must provide exactly the two continuity values produced by Session A:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact temporary Google Sheet URL>`

Do not request or accept the Session A transcript, ActiveTask JSON, a state summary, or evaluator notes. If any such state content is included, mark the run invalid because cross-session continuity is no longer isolated.

## Repository pinning

Use exactly `TEST_COMMIT`. Do not resolve or follow current `main` if it differs.

Read, pinned to `TEST_COMMIT`:

- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_LIVE_COOKING.md`
- `providers/google_drive.md`
- `persistence/web_durable.md`
- `retrieval/web_google_drive.md`
- `schemas/google_drive_store.yaml`
- `tests/persistence/manifest.yaml`
- `tests/persistence/01_google_drive_cross_session_resume.md`

Do **not** read `tests/persistence/expectations/*` until all candidate responses for B1 and B2 have been frozen.

## Store isolation

Use exactly `TEST_STORE_URL`. Do not search for or switch to another Kitchen store.

Before generating B1:

1. verify the store marker with a tiny META read;
2. bootstrap continuity using only META plus the current ActiveTask record;
3. do not read EVENTS for normal bootstrap;
4. perform only task-specific bounded retrieval after the route is known.

The previous chat is unavailable by design. Recovery must come from the selected store.

## Candidate execution

Process Session B turns from `tests/persistence/01_google_drive_cross_session_resume.md` sequentially as separate user turns.

### B1

Use the exact B1 user message from the script.

Produce the candidate's Live Cooking response from the current direct observation plus the bounded persisted context. Then persist meaningful corrected task/state observations through the documented PersistenceCoordinator/provider path before moving on.

### B2

Use the exact B2 user message from the script.

Produce the candidate response and persist meaningful changes. Do not rewrite B1 after seeing B2.

## Freeze before evaluation

After the B2 provider write completes:

1. freeze the user-facing candidate responses from B1 and B2;
2. record what provider reads/writes were actually performed;
3. only then read `tests/persistence/expectations/01_google_drive_cross_session_resume.md`;
4. evaluate the frozen Session A store state and frozen Session B behavior against the evaluator criteria;
5. do not regenerate candidate answers to improve the score.

You may inspect only the bounded store ranges/rows needed to verify criteria. Do not turn evaluation into a full history load.

## Required report

Return:

- `TEST_COMMIT`
- `TEST_STORE_URL`
- overall `PASS` or `FAIL`
- criteria results using `PASS`, `FAIL`, or `NOT_EXERCISED`
- exact failure class for every failure
- concise evidence for bounded bootstrap, state precedence, no completed-step restart, and durable writeback
- whether the test store was successfully deleted after evaluation

If the gate passes, delete the temporary Google Sheet after all evaluation evidence has been collected. If the gate fails because store contents are needed for debugging, leave it in place and clearly say `TEST_STORE_RETAINED_FOR_DEBUGGING`.

Do not modify production Kitchen data. Do not modify repository candidate files during this test.
