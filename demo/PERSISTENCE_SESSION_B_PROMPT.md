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

## Mandatory GitHub result sink

The durable test result belongs on existing tracking issue:

- repository: `john-no-bug/kitchen-skill`
- issue: `#2` — `v0.6 persistence gate: real Chat A → fresh Chat B resume`

Do **not** create a separate regression issue for this gate.

Before deleting or otherwise cleaning up the temporary store, add a comment to Issue #2 containing:

- `TEST_COMMIT`
- `TEST_STORE_URL`
- overall `PASS` or `FAIL`
- every criterion as `PASS`, `FAIL`, or `NOT_EXERCISED`
- exact failure class for every failure
- concise evidence for bounded bootstrap, state precedence, completed-step handling, and durable B1/B2 writeback
- the latest observed META/ActiveTask revisions after B2
- `TEST_STORE_CLEANUP: pending`

This GitHub writeback is part of the harness, not an optional convenience.

If the Issue #2 comment cannot be written:

1. force the overall test result to `FAIL`;
2. classify `harness_defect`;
3. retain the temporary store;
4. do not close Issue #2;
5. return `TEST_STORE_RETAINED_FOR_DEBUGGING` to the user.

## Cleanup and gate closure

After a successful Issue #2 result comment:

### If the evaluated gate is FAIL

- retain the temporary store for debugging;
- add a short follow-up comment to Issue #2 stating `TEST_STORE_RETAINED_FOR_DEBUGGING`;
- leave Issue #2 open.

### If the evaluated gate is PASS

1. delete the temporary Google Sheet only after all evaluation evidence and the first Issue #2 result comment are safely recorded;
2. verify the store is no longer accessible;
3. add a follow-up comment to Issue #2 stating `TEST_STORE_CLEANUP: deleted`;
4. close Issue #2 with state reason `completed`.

If cleanup fails, do not silently close the issue. Add the cleanup failure to Issue #2 and leave it open until the test artifact is resolved.

## Required user-facing report

Return:

- `TEST_COMMIT`
- `TEST_STORE_URL`
- overall `PASS` or `FAIL`
- criteria results using `PASS`, `FAIL`, or `NOT_EXERCISED`
- exact failure class for every failure
- concise evidence for bounded bootstrap, state precedence, no completed-step restart, and durable writeback
- Issue #2 writeback status
- whether the test store was deleted or retained

Do not modify production Kitchen data. Do not modify repository candidate files during this test.