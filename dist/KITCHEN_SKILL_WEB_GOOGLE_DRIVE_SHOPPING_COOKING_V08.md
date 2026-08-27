# Kitchen Skill — Web + Google Drive v0.8 History Compaction

## Scope

This v0.8 bundle extends the validated v0.7 Shopping → canonical KitchenState → Cooking path with Event → Experience compaction and long-history bounded-context behavior.

It preserves all validated v0.5/v0.6/v0.7 domain behavior. No new provider table or seventh interface is introduced.

## Core invariants

- Runtime != Storage.
- DomainModules never write StorageProvider directly.
- ContextRetriever is read-only.
- PersistenceCoordinator is the semantic write gate.
- Current direct observation outranks stored/history-derived state.
- Unknown != zero/false/absent.
- Precision never increases without evidence.
- Normal retrieval is bounded.
- **History growth must not cause proportional ContextPack growth.**
- Events are cold append-only history.
- Experience is compact reusable learned knowledge.

## Existing Google Drive store

Continue using exactly the existing five tabs:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

Do not create a compaction, archive, vector, retry, or Shopping-specific table.

## Event semantics

Event is immutable evidence of something that happened.

Events support audit, repair, analytics, and future compaction. Normal Cooking/Shopping retrieval does not load them.

Compaction does not delete or rewrite Events in this slice.

## Experience semantics

Experience is compact reusable knowledge learned from repeated history.

Canonical fields follow the frozen v0.5 object, including:

- stable `meta.id`;
- stable semantic `key`;
- `kind`;
- `subject_refs`;
- compact `summary` / `conditions` / `learned_value`;
- `confidence`;
- scalar `evidence_count`;
- timestamps;
- `status` (`tentative|active|superseded|retired`);
- bounded `evidence_event_refs`.

The Experience itself must remain compact even when `evidence_count` becomes large.

## Event → Experience compaction

Logical path:

`HealthEngine -> RepairPlan -> PersistenceCoordinator -> StorageProvider`

Compaction is maintenance, not a DomainModule write shortcut.

A maintenance pass:

1. selects a bounded candidate Event set using subject/key/tag/time filters;
2. reads only bounded existing Experience candidates;
3. groups compatible evidence by stable Experience key;
4. merges only unique compatible Event evidence;
5. increments `evidence_count`;
6. keeps summary/conditions/learned_value compact;
7. retains at most 8 representative/recent `evidence_event_refs` in the Web slice;
8. updates `Meta.last_compaction_at` only after durable commit;
9. leaves all Events unchanged.

Suggested one-pass bounds:

```yaml
max_candidate_events_per_compaction: 64
max_existing_experiences_read: 8
max_experience_mutations_per_compaction: 4
max_evidence_event_refs_per_experience: 8
```

Large backlogs are compacted incrementally rather than loaded into one model context.

## Compatible evidence

Do not merge merely because events mention the same ingredient.

Evidence is compatible when subject/conditions/reusable learned relationship match the same semantic Experience key.

Example key:

`frozen_ground_beef:supor_green_pot`

Example compact summary:

`Frozen ground beef in the Supor green pot may release substantial water; break it apart, evaporate excess water, then brown.`

Repeated compatible observations may increase confidence/evidence_count. They do not create exact numeric rules without exact evidence.

## Contradictions

Current direct observation always wins.

Do not average explicit contradictions. Older Experiences may later be marked superseded or split into conditional patterns through Health repair. Contradiction migration is not required by the first v0.8 gate.

## Normal Cooking retrieval

Bootstrap remains:

- META;
- current ActiveTask only when META points to one.

After routing Cooking:

- current observation;
- compact ActiveTask;
- specific relevant state/equipment/preferences;
- at most 1–2 Experience payloads;
- no Events by default.

Experience ranking:

1. exact subject/key/condition relevance;
2. active over tentative;
3. condition match;
4. evidence-backed confidence/evidence_count;
5. recency when freshness matters.

Exclude superseded/retired Experiences by default.

Never dereference `evidence_event_refs` merely because an Experience was selected.

## Normal Shopping retrieval

Shopping uses current decision-relevant state plus at most one relevant Experience and zero Events by default.

History size must not cause the system to load more Experience rows just because they exist.

## Long-history invariant

For equivalent current requests/state, growth from a small history to thousands of Events and hundreds of Experiences must leave normal context structurally bounded:

```yaml
max_state_records: 12
max_experiences_cooking: 2
max_experiences_shopping: 1
max_events: 0
max_recipes: 1
```

Selected-record payload size may change slightly because compact metadata such as `evidence_count` changes, but it must not scale with raw history size.

## Evidence precedence

1. newest direct user observation;
2. authoritative ActiveTask;
3. KitchenState;
4. explicit/recent Event only when intentionally retrieved;
5. relevant Experience;
6. Recipe;
7. old conversation.

An Experience never overrides a contradictory current physical observation.

## Failure behavior

The validated degradation contract remains unchanged:

- keep safe/useful guidance moving;
- never claim unconfirmed durability;
- retain pending changes when possible;
- Health owns degradation/maintenance planning;
- PersistenceCoordinator owns semantic writes.

Compaction failure must not advance `Meta.last_compaction_at` or corrupt/delete Events.

## Architecture invisibility

Do not expose Events, Experience keys, compaction, ContextPack, revisions, sheet tabs, HealthEngine, or provider mechanics in normal user-facing cooking/shopping guidance.
