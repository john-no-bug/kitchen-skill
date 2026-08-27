# Persistence Coordinator — Web Durable Slice

## Responsibility

This is the single semantic write path for Web + durable provider deployments.

It converts DomainModule/Health write intent into validated canonical mutations, then delegates physical writes to the selected StorageProvider.

Cooking, Shopping, and Health never write Google Drive directly.

## Input compatibility

The existing Pure Web Cooking implementation predates the durable `ChangeSet` field and conceptually emits:

- `active_task_patch`;
- `state_observations`;
- `experience_observations`;
- health signals.

To avoid rewriting Cooking logic, this coordinator accepts that shape as compatibility shorthand and normalizes it into one canonical `ChangeSet` before validation.

New durable modules, including Shopping, should prefer emitting `ChangeSet` directly.

Normalization is an implementation detail, not a second write interface.

## Compatibility normalization

Conceptual mapping:

```text
active_task_patch
  -> ChangeSet.active_task_ops

state_observations
  -> ChangeSet.state_ops

experience_observations
  -> ChangeSet.experience_ops

end-of-task meaningful facts
  -> optional ChangeSet.event_appends + state/experience updates + ActiveTask completion/clear
```

The provider must not care which ModuleResult syntax produced the ChangeSet.

## Validation

Before provider commit, enforce:

1. schema/path validity;
2. current user observation is not overwritten by older lower-priority evidence;
3. unknown is not converted to zero/false/absent;
4. approximate amounts remain approximate after arithmetic;
5. exactness can degrade but cannot increase without evidence;
6. Event records are append-only;
7. canonical IDs remain stable;
8. secrets/credentials are not written to Kitchen data;
9. expected/global revision is not stale when revision information is available;
10. Experience evidence aggregation does not grow canonical payloads proportionally to raw Event count.

## Amount subtraction rule

Example:

```text
inventory says exact 500 g beef from a labelled purchased package
cooking observation says approximately 120 g used
```

The result may be represented as approximately 380 g or an uncertainty range, but **not** exact 380 g because the subtraction includes approximate evidence.

Likewise, `~500 g - ~120 g` remains approximate.

If unit conversion or source precision is unclear, preserve uncertainty or mark the result unknown rather than fabricate precision.

## Commit flow

1. Read current `META.global_revision` and only the affected records needed for validation/row addressing.
2. Normalize and validate the ChangeSet.
3. Resolve semantic operations into canonical post-write records.
4. Build one `StorageMutationBatch` containing all related state/task/experience/event/meta mutations.
5. Ask the StorageProvider to commit the batch.
6. Return `durable_committed` only when durable provider write succeeds.
7. On success, use the new revision as the session continuity authority.

For the Google Sheets provider, related task/state/experience/event/meta changes for one user turn should be sent in one spreadsheet batch when practical.

## Shopping purchase commit

A confirmed purchase is a normal semantic commit, not a special provider path.

One Shopping ChangeSet may:

- upsert the purchased inventory item in KitchenState at the precision supported by the observation/package label;
- append a compact `purchase_inventory` Event;
- complete/clear the Shopping ActiveTask;
- set `Meta.active_task_id = null`;
- advance global revision.

Do not ask the user to re-enter the purchase into inventory after they already confirmed it.

The next Cooking task reads the resulting KitchenState; it does not need to retrieve the purchase Event.

## Event → Experience compaction commits

Compaction is a Health maintenance write, not a provider feature and not a DomainModule shortcut.

Logical path:

`HealthEngine -> RepairPlan/ChangeSet -> PersistenceCoordinator -> StorageProvider`

For a compatible Event evidence cluster, one compaction ChangeSet may:

- upsert/merge one or more existing Experience records by stable `meta.id` + semantic `key`;
- increment `evidence_count` only for newly accepted unique Event refs;
- update compact confidence/status/timestamps;
- retain only a bounded representative set of `evidence_event_refs` (Web default: maximum 8);
- update `Meta.last_compaction_at` after successful durable commit;
- advance global revision.

It must **not** delete, rewrite, or mark the supporting Events as consumed. Event history remains append-only cold audit data.

### Experience merge validation

Before commit:

1. confirm candidate events are semantically compatible with the target Experience key/conditions;
2. deduplicate evidence refs before incrementing `evidence_count`;
3. preserve the stable Experience record ID/key for compatible merges;
4. do not copy raw transcript text into Experience;
5. do not let `evidence_event_refs` grow beyond the configured cap;
6. do not upgrade numeric exactness merely because repeated evidence exists;
7. do not average explicit contradictory user observations;
8. exclude `superseded`/`retired` records from automatic merge targets unless a repair explicitly addresses them.

A large raw evidence count may increase the scalar `evidence_count`; it must not cause Experience payload size to grow linearly.

If the provider write fails, `Meta.last_compaction_at` must not advance and the compaction ChangeSet may remain pending/deferred like other semantic writes.

## ActiveTask completion

When an operational task ends, one semantic commit may:

- apply known KitchenState deltas;
- append a compact Event if useful;
- upsert/merge tentative Experience evidence when warranted;
- mark/clear the ActiveTask;
- set `Meta.active_task_id = null`;
- advance global revision.

Do not preserve the entire task transcript as task history.

## Stale revision

If the current store revision differs from `ChangeSet.base_global_revision`:

- do not blindly overwrite;
- refresh only Meta + affected records;
- re-evaluate the semantic change against current evidence;
- if the change cannot be safely rebased, return deferred/rejected and retain it as a session-level pending change.

v1 does not attempt concurrent multi-client merge.

## Provider failure

If commit fails:

- current cooking/shopping guidance continues when safe/useful;
- do not tell the user the change was durably saved;
- retain the newest logical ActiveTask/pending changes in session context when possible;
- emit a storage-degraded Health signal;
- retry only when relevant/provider becomes available.

Storage housekeeping must not displace the user's immediate kitchen task.
