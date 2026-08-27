# Kitchen Skill — v0.8 Event/Experience Compaction + Long-History Bounded Context

Status: v0.8 implementation/harness ready for real integration gate  
Architecture baseline: frozen v0.4 + v0.5 interface/schema draft

## Validated baselines

### v0.5 — Pure Web Live Cooking ✅

The frozen Pure Web candidate passed the required 3 × 36/36 regression runs.

### v0.6 — Web + Google Drive persistence ✅

Real Chat A -> fresh Chat B continuity passed in GitHub Issue #2:

- bounded META + ActiveTask bootstrap;
- newest direct observation overrides persisted stale physical state;
- durable writeback works across fresh chats;
- normal Cooking retrieval does not load Event history.

### v0.7 — Shopping -> canonical KitchenState -> fresh Cooking ✅

Real cross-domain gate passed in GitHub Issue #3:

- Shopping purchase becomes canonical inventory + compact purchase Event;
- Shopping ActiveTask clears;
- fresh Cooking reads STATE rather than Shopping transcript/Event history;
- exact 500 g minus approximately 120 g becomes approximately 380 g.

### Reliability — provider degradation/retry ✅

Real failure injection passed in GitHub Issue #5:

- provider read and write failures were real Google Sheets 404s;
- safe Cooking guidance continued;
- no false durable-success claim;
- failed semantic change remained session-pending;
- valid-store revision did not advance on failed write;
- recovery retried the pending ChangeSet and advanced revision exactly once.

## v0.8 architecture claim

The next frozen invariant to validate is:

> History growth must not cause proportional ContextPack growth.

The v0.8 slice formalizes the relationship:

`raw append-only Events -> Health compaction -> compact Experience -> bounded normal retrieval`

Events remain cold audit history. Compaction does **not** delete/rewrite them in this slice.

## v0.8 implementation additions

- `health/event_experience_compaction.md` — bounded Health maintenance profile for Event -> Experience aggregation.
- `retrieval/web_google_drive.md` — Experience ranking/status filtering, evidence-ref non-dereference, explicit long-history invariant.
- `persistence/web_durable.md` — Experience merge/evidence-count/ref-cap validation and compaction commit semantics.
- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md` — v0.8 deployable behavior bundle.

No new canonical object, interface, provider, or Google Sheets tab is introduced.

The durable store remains exactly:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

## Compaction semantics

Repeated compatible Event evidence merges into one stable Experience.

Example:

`frozen_ground_beef:supor_green_pot`

A compaction pass may:

- select a bounded set of matching Event evidence;
- merge unique compatible refs into the existing Experience;
- increment scalar `evidence_count`;
- keep summary/conditions/learned_value compact;
- retain at most 8 representative/recent `evidence_event_refs` in the Web slice;
- update `Meta.last_compaction_at` only after successful durable commit.

Supporting Events remain append-only.

Compaction runs through:

`HealthEngine -> RepairPlan/ChangeSet -> PersistenceCoordinator -> StorageProvider`

DomainModules do not write providers directly.

## Normal retrieval after large history

Normal Cooking:

- META + ActiveTask tiny bootstrap;
- relevant current STATE;
- at most 1–2 Experience rows;
- 0 Events by default.

Normal Shopping:

- relevant current STATE/plans;
- at most 1 Experience row;
- 0 Events by default.

Selected Experience `evidence_event_refs` do not trigger Event reads merely because they exist.

Superseded/retired Experiences are excluded by default.

## v0.8 real integration gate

Tracking issue: GitHub Issue #6.

Harness:

- `tests/history/manifest.yaml`
- `tests/history/01_long_history_compaction_and_bounded_context.md`
- `tests/history/expectations/01_long_history_compaction_and_bounded_context.md`
- `tests/history/README.md`
- `demo/HISTORY_COMPACTION_LONG_CONTEXT_PROMPT.md`

The gate uses one isolated native Google Sheet and one dedicated test conversation.

It compares identical Cooking/Shopping retrieval probes under:

1. tiny history;
2. 2000 Event rows + 122+ Experience rows after bounded compaction.

The gate verifies:

- normal retrieval still reads zero Events;
- Experience counts remain within fixed domain limits;
- relevant active Experience beats irrelevant/superseded noise;
- selected persisted-record context size stays near the tiny-history baseline instead of scaling with history;
- 17 new compatible Event observations merge into the existing Experience (`evidence_count 3 -> 20`);
- Experience evidence refs remain <=8;
- all 2000 Events remain present;
- current user observation still outranks Experience.

**This v0.8 real long-history gate has not yet been executed and must not be reported as passed.**

## Next after v0.8 gate

If the real compaction/long-history gate passes:

1. freeze the v0.8 history behavior as a validated baseline;
2. then decide whether the next highest-value expansion is another shared provider (Notion/Tencent Docs), Codex/local storage, or broader domain coverage;
3. do not add a vector database unless a demonstrated retrieval failure requires one.

## Architecture docs

- `docs/Kitchen_System_v0.4_Frozen_Architecture.md` — rollback baseline.
- `docs/Kitchen_System_v0.5_Interface_and_Schema_Draft.md` — formal interface/canonical schema baseline.

The v0.8 label is an implementation milestone, not a replacement architecture document.
