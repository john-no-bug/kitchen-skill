# Health Engine — Event → Experience Compaction

## Scope

This v0.8 maintenance profile turns repeated compatible Event evidence into compact reusable Experience records without making normal Cooking/Shopping retrieval depend on raw history.

It does **not** introduce a seventh interface or a new storage collection.

Logical path:

`HealthEngine -> RepairPlan -> PersistenceCoordinator -> StorageProvider`

Events remain append-only cold data. Compaction means **logical knowledge compaction into Experience**, not destructive Event rewriting/deletion.

## Why this exists

The system invariant is:

> history growth must not cause proportional ContextPack growth.

Raw Events provide auditability, but repeated compatible evidence should become one compact Experience. Future domain turns retrieve that Experience directly and normally retrieve zero Events.

## Triggering

Web has no required background scheduler. Compaction may run:

- explicitly in a maintenance/test operation;
- opportunistically after an operational task completes when the user is not waiting on an immediate action;
- during a low-friction Health maintenance pass when enough uncompacted evidence exists.

Do not interrupt active cooking merely to compact history.

`Meta.last_compaction_at` is the canonical maintenance watermark available in the v0.5 schema. Advance it only after a durable compaction commit succeeds.

## Bounded maintenance input

A single compaction pass must remain bounded in model context even if physical history is large.

Suggested Web defaults:

```yaml
max_candidate_events_per_compaction: 64
max_existing_experiences_read: 8
max_experience_mutations_per_compaction: 4
max_evidence_event_refs_per_experience: 8
```

A provider may scan/filter a larger cold table internally to select candidates, but only the bounded candidate set enters reasoning context. Large backlogs are processed incrementally over multiple passes rather than loaded wholesale.

Prefer candidate selection by:

1. subject/entity refs;
2. stable compaction key/tag;
3. `occurred_at > Meta.last_compaction_at` when available;
4. finite provider scan bounds.

## Experience key and compatible evidence

Each compactable pattern uses a stable semantic `Experience.key`, for example:

`frozen_ground_beef:supor_green_pot`

Compatible evidence must describe the same reusable relationship/condition. Do not merge events merely because they share one ingredient name.

For one compatible cluster:

- preserve the stable Experience `meta.id` and `key` when updating an existing record;
- increment `evidence_count` only for newly accepted unique Event evidence;
- update `first_observed_at` / `last_observed_at` when supported;
- keep `summary`, `conditions`, and `learned_value` compact and reusable;
- retain at most the configured number of representative/recent `evidence_event_refs`;
- never copy raw transcripts into Experience.

`evidence_count` may grow without causing Experience payload size to grow proportionally.

## Confidence/status

For the first Web slice:

- one isolated observation may remain `tentative`;
- repeated compatible direct observations may raise confidence;
- three or more consistent observations may support `status=active` when there is no material contradiction;
- do not promote exact numeric/personal rules merely because evidence_count increased.

Compaction aggregates evidence; it does not manufacture precision.

## Contradictions

Do not average explicit contradictions.

If newer high-priority evidence materially conflicts with an existing Experience:

- keep the newest direct observation authoritative for the current task;
- exclude the contradicted Experience from current guidance when appropriate;
- Health may mark an older Experience `superseded` or keep both as separate conditional patterns through a later RepairPlan;
- do not destroy the supporting Events.

The first v0.8 gate validates compatible merging and bounded retrieval; contradiction migration is not required for that gate.

## Commit semantics

One compaction RepairPlan/ChangeSet may:

- upsert/merge one or more Experience records;
- update `Meta.last_compaction_at`;
- advance global revision.

It must **not** rewrite/delete the supporting Event rows.

PersistenceCoordinator validates stable IDs, evidence uniqueness, status/confidence semantics, and the evidence-ref cap before provider commit.

## Retrieval boundary after compaction

Normal Cooking/Shopping retrieval:

- reads no Events by default;
- retrieves only top relevant active/tentative Experiences within domain limits;
- never dereferences `evidence_event_refs` merely because they are present;
- excludes `superseded` and `retired` Experience records by default.

A mature Experience is the reusable context object. Events remain cold audit history.
