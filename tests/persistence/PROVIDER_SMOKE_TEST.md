# Google Drive Provider Smoke Test

Date: 2026-08-25 (America/Los_Angeles)  
Scope: physical Drive/Sheets primitives only; **not** the full Chat A -> Chat B persistence acceptance test.

## Purpose

Verify that the currently available Web-host Google Drive connector can execute the provider operations assumed by `providers/google_drive.md`.

## Test procedure

A temporary native Google Sheet named `Kitchen Skill Store - DEV PROVIDER SMOKE TEST` was created and deleted in the same development session.

The test used a minimal five-tab store:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

### 1. Initialization batch

One spreadsheet batch successfully:

- renamed the default sheet to `META`;
- created `STATE`, `ACTIVE_TASK`, `EXPERIENCES`, and `EVENTS`;
- wrote all five header rows;
- wrote a compatible META marker;
- wrote a root KitchenState row;
- wrote bounded test inventory/equipment rows;
- wrote one compact ActiveTask;
- wrote one compact Experience.

### 2. Bounded reads/search

Verified:

- `META!A1:H2` can be read directly without loading the rest of the store;
- a bounded `STATE!A1:F20` row search for `ground_beef` returned the single relevant inventory row.

This supports the intended bootstrap/retrieval strategy rather than whole-store reads.

### 3. Atomic per-turn style write

A second spreadsheet batch successfully performed all of the following together:

- updated ActiveTask revision `1 -> 2`;
- changed phase from `evaporate_water` to `brown_beef`;
- changed beef state from `water_level=high` to `water_level=none, sizzling=true`;
- advanced META global revision `1 -> 2`;
- appended one Event row.

### 4. Readback

Bounded reads confirmed:

- `ACTIVE_TASK!A1:I2` contained revision 2 and the corrected physical state;
- `EVENTS!A1:F3` contained the appended Event.

### 5. Cleanup

The temporary spreadsheet was deleted successfully. No test Kitchen store was intentionally retained.

A subsequent access attempt returned not-found, consistent with successful cleanup.

## Result

**PASS — provider primitive smoke test.**

The current connector can support the physical operations assumed by the first Google Sheets-backed StorageProvider slice:

- create store;
- initialize schema in batch;
- bounded projection read;
- bounded row search;
- update task/meta in one batch;
- append Event in that batch;
- bounded readback.

## Explicit non-claims

This smoke test does **not** prove:

- fresh Chat B can discover and resume Chat A automatically;
- the complete bundle routes/retrieves/commits correctly over multiple user turns;
- stale revision handling works across real competing clients;
- provider failure fallback has been exercised end-to-end;
- cross-platform clients can all access the same representation.

Those remain acceptance/integration tests, beginning with `01_google_drive_cross_session_resume.md`.
