# Kitchen Skill Provider Degradation / Failure Injection Gate

Run this as one dedicated integration-test conversation for `john-no-bug/kitchen-skill`.

## Repository pinning

1. Inspect current `main` once at start and set exact HEAD as `TEST_COMMIT`.
2. Pin every repository read for this run to TEST_COMMIT.
3. Read pinned, before candidate execution:
   - `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING.md`
   - `core/kernel.md`
   - `runtime/web_persistent.md`
   - `retrieval/web_google_drive.md`
   - `persistence/web_durable.md`
   - `health/web_google_drive.md`
   - `providers/google_drive.md`
   - `modules/cooking/contract.md`
   - `modules/cooking/logic.md`
   - `tests/degradation/manifest.yaml`
   - `tests/degradation/01_provider_failure_and_recovery.md`
4. Do **not** read `tests/degradation/expectations/*` until all D0-D3 candidate responses and provider traces are frozen.

## Isolated provider setup

Create two native Google Sheets used only by this test:

1. valid store: `Kitchen Skill Degradation Test - <short TEST_COMMIT>`
2. sacrificial store: `Kitchen Skill Degradation Dead Target - <short TEST_COMMIT>`

Initialize the valid store with the existing five-tab `kitchen-skill-google-sheets-v1` layout only:

- META
- STATE
- ACTIVE_TASK
- EXPERIENCES
- EVENTS

Do not create any degradation-specific tab and do not touch production Kitchen stores.

Immediately delete the sacrificial Sheet and retain only its now-dead spreadsheet URL/ID as `DEAD_TARGET`. Verify at least one bounded read against it returns a real not-found/provider failure. This ID is harness-only fault-injection state and must never be written into canonical Kitchen data.

## Execute candidate scenario sequentially

Use the exact D0-D3 user messages from `tests/degradation/01_provider_failure_and_recovery.md`. Process them as separate turns. Do not batch-answer or rewrite earlier responses later.

### D0 — healthy baseline

Use the valid store normally.

Generate/freeze D0 response, commit its semantic ActiveTask through PersistenceCoordinator/provider, and record bounded read/write operations plus the post-D0 valid-store `META.global_revision` as `BASELINE_REVISION`.

### D1 — read failure

For the normal persistent bootstrap attempt only, route the provider read to `DEAD_TARGET` so the real connector call fails. Do not query the valid store to replace that failed bootstrap before generating D1.

Generate/freeze D1 using visible conversation/session working state under the documented degraded-runtime behavior.

Record:

- the actual failed read;
- the session-only/degraded continuity decision or Health signal;
- whether any user-facing durable/recovery claim was made.

After D1 response is frozen, restore the valid store as provider target. No D1 write is required if the turn produced no meaningful semantic change.

### D2 — write failure

Use the valid store for normal bounded bootstrap/retrieval.

Generate the D2 user-facing response and semantic ChangeSet from the newest direct physical observation. Freeze the domain response/change intent before fault injection.

Immediately before PersistenceCoordinator delegates the provider commit, route exactly that commit call to `DEAD_TARGET`. The connector call must fail.

Do not alter the valid store.

Record:

- the failed provider receipt/error;
- `durable_committed=false` or equivalent;
- storage-degraded Health state;
- the exact pending semantic change retained in session working state;
- whether any false durable-success claim was made.

Then read only bounded META/current ActiveTask from the valid store and verify:

- its revision is still `BASELINE_REVISION` (unless D1 legitimately made a successful semantic commit, in which case use the latest healthy pre-D2 revision as the comparison baseline);
- the failed D2 state is not partially durable there.

### D3 — recovery

Restore the valid test store as the provider target.

Without inventing a new physical observation, retry the retained D2 pending semantic change through normal PersistenceCoordinator/provider flow. Refresh only META plus affected current records needed for validation/rebase.

After successful retry, bounded-read the valid META/current ActiveTask and verify the newest D2 observation is now durable and the revision advanced normally.

Then process/freeze exact D3 `继续。` candidate response from that recovered state.

## Freeze and evaluate

After D3 response and recovery evidence are frozen:

1. record the complete ordered provider-operation trace for D0-D3;
2. only now read `tests/degradation/expectations/01_provider_failure_and_recovery.md` pinned to TEST_COMMIT;
3. evaluate the frozen run criterion-by-criterion;
4. do not regenerate candidate answers or provider traces to improve the score.

## Durable result reporting — mandatory

Before cleanup, add one complete frozen result comment to `john-no-bug/kitchen-skill` Issue #5 containing:

- TEST_COMMIT;
- valid TEST_STORE_URL;
- DEAD_TARGET id/url and proof it was deleted before injection;
- overall PASS/FAIL;
- all criterion results and failure classes;
- frozen D0-D3 user-facing responses;
- candidate-phase bounded read/write trace;
- D1 failed-read evidence and fallback behavior;
- D2 failed-write evidence, no-success receipt, pending ChangeSet evidence, and valid-store revision check;
- D3 retry/recovery evidence and post-retry state/revision;
- explicit confirmation expectations were unread until candidate/trace freeze;
- confirmation fault-injection details never entered canonical Kitchen payloads.

If GitHub result writeback fails, overall result is FAIL with `harness_defect`; retain the valid store and keep Issue #5 open.

## Cleanup

If overall PASS and the result comment exists:

1. delete the valid temporary Kitchen store;
2. verify it is unavailable;
3. append a cleanup receipt to Issue #5;
4. close Issue #5 as completed.

If FAIL, retain the valid store for debugging and keep Issue #5 open. The sacrificial Sheet should already be deleted by design.

Do not modify production Kitchen data or repository candidate files during this test.
