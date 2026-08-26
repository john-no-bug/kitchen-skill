# Kitchen Skill v0.6 Persistence Integration — Session A

This is **integration-test Session A (writer)** for `john-no-bug/kitchen-skill`. It is not a development session and not the v0.5 Pure Web regression suite.

Your job is to establish a durable Live Cooking task in an **isolated temporary Google Sheets Kitchen test store** so that a completely fresh Session B can resume using Drive only.

## Non-negotiable isolation rules

- Do not use or modify a production/personal Kitchen store if one exists.
- Create a new temporary native Google Sheet dedicated to this run.
- Preferred title: `Kitchen Skill Persistence Test - <short commit SHA>`; if that exact title already exists, add a unique suffix rather than reusing it.
- Do not paste task state into a handoff for Session B.
- The only manual continuity values Session B may receive are the exact tested commit SHA and the exact temporary store URL/file ID.

## Repository pinning

1. Inspect `john-no-bug/kitchen-skill` and resolve the current `main` HEAD once at the beginning.
2. Record it as `TEST_COMMIT`.
3. Every repository read for this run must be pinned to `TEST_COMMIT`.
4. Do not follow later changes to `main` during the run.

Read, from `TEST_COMMIT`:

- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_LIVE_COOKING.md`
- `providers/google_drive.md`
- `persistence/web_durable.md`
- `retrieval/web_google_drive.md`
- `schemas/google_drive_store.yaml`
- `tests/persistence/manifest.yaml`
- `tests/persistence/01_google_drive_cross_session_resume.md`

Do **not** read `tests/persistence/expectations/*` in Session A.

## Store setup

Create one isolated native Google Sheet and initialize the minimum v0.6 store layout exactly as the pinned provider/store mapping requires. Use that Sheet as the selected `GoogleDriveProvider` for this run.

Do not create a spreadsheet architecture that differs from the pinned provider merely for convenience.

## Candidate execution

Treat the pinned Web + Google Drive bundle as the candidate behavior. Process Session A turns from `tests/persistence/01_google_drive_cross_session_resume.md` sequentially as separate user turns:

- A1
- A2
- A3

For each turn:

1. perform only bounded reads needed by the candidate;
2. produce the candidate's user-facing Live Cooking response;
3. normalize meaningful changes through the documented PersistenceCoordinator path;
4. perform the provider write before advancing to the next scripted turn;
5. do not batch-answer future turns.

After A3, verify durable continuity using bounded store reads. Do not load evaluator expectations and do not rewrite candidate responses after the fact.

## Required final output

Return a concise Session A test handoff containing exactly these items plus a one-line status:

- `TEST_COMMIT: <40-char SHA>`
- `TEST_STORE_URL: <exact Google Sheet URL>`
- `SESSION_A_STATUS: READY_FOR_FRESH_SESSION_B` or `SESSION_A_STATUS: FAILED`

If FAILED, add a compact failure reason after the status, but still do not expose an ActiveTask dump or task-state summary for Session B.

Do not delete the temporary store yet. Session B owns final inspection/cleanup after evaluation.
