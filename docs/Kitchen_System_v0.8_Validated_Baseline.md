# Kitchen System v0.8 — Validated Baseline Addendum

**Status:** evidence-backed addendum; does not replace frozen v0.4 or formal v0.5 interface/schema draft  
**Product-bearing baseline:** `a0a8979e412ab254eb9095b9d5ccf21747bc8c63`

## 1. Purpose

This document records which architectural claims have been exercised by real regression/integration gates through v0.8.

It is not a new architecture rewrite. If this document conflicts with the frozen v0.4 architecture or the v0.5 interface/schema draft, treat the older formal documents as the contract and treat the conflict as a defect to resolve explicitly.

## 2. Validated interface boundaries

### RuntimeAdapter / StorageProvider separation

Validated evidence:

- Pure Web remains useful without durable storage.
- Web + Google Drive adds durability without changing Cooking domain rules.
- storage read/write failures degrade continuity rather than replacing the kitchen task.

Still unvalidated:

- Codex runtime composition.
- second shared provider.
- concurrent multi-client conflict handling.

### ContextRetriever

Validated:

- tiny META + current ActiveTask bootstrap.
- explicit routing before task-specific retrieval.
- normal Cooking/Shopping retrieval is bounded.
- normal candidate generation does not load Events by default.
- at most 1–2 relevant Experiences for Cooking and at most 1 for Shopping in the current Web slice.
- selected Experience evidence refs do not imply Event dereference.

### DomainModule

Validated product modules:

- Cooking.
- Shopping.

Their cross-domain handoff is canonical KitchenState rather than transcript replay.

Canonical schema support for Inventory, Planning, Recipe, and Equipment is not evidence that those independent DomainModules have been implemented.

### PersistenceCoordinator

Validated:

- semantic write gate before provider commit.
- current observation precedence.
- unknown preservation.
- precision degradation (`500 g exact - ~120 g` becomes approximately 380 g).
- revision-aware durable writes.
- failed durable write does not produce durable success.
- failed semantic change can remain session-pending and retry after provider recovery.
- Experience compaction merge preserves stable id/key, deduplicates evidence, caps representative evidence refs, and does not mutate supporting Events.

### HealthEngine

Validated:

- cheap state/retrieval re-anchoring behavior through Cooking regression.
- storage degradation signalling and recovery path.
- Event → Experience compaction maintenance path:
  `HealthEngine -> RepairPlan/ChangeSet -> PersistenceCoordinator -> StorageProvider`.

Web does not require a background scheduler; maintenance may be explicit or opportunistic.

## 3. Validated canonical-object behavior

### KitchenState

Validated for:

- inventory handoff from Shopping to Cooking.
- equipment lookup relevant to Cooking.
- current state outranking colder history.

### ActiveTask

Validated for:

- sparse operational Cooking state.
- sparse Shopping state.
- task clear before cross-domain handoff.
- fresh-session continuation.
- no proportional transcript growth.

### Experience

Validated for:

- compact reusable learned knowledge.
- stable semantic key/id on compatible evidence merge.
- scalar evidence_count growth without linear payload growth.
- bounded representative evidence refs (Web slice cap: 8).
- active/tentative retrieval with superseded/retired exclusion by default.

### Event

Validated for:

- compact immutable purchase/audit evidence.
- append-only cold history.
- zero normal Event reads in the tested Cooking/Shopping paths.
- surviving compaction unchanged at a 2000-row history scale.

### Meta

Validated for:

- store marker/schema compatibility.
- global revision continuity.
- active_task_id continuity.
- degraded health signalling.
- last_compaction_at advancing only after successful compaction commit.

### Recipe

Canonical object exists in v0.5 design, but no independent durable Recipe collection/provider mapping has yet been validated in the Google Drive five-tab slice.

## 4. Validated provider profile

Current durable provider profile:

`GoogleDriveProvider / kitchen-skill-google-sheets-v1`

Physical tabs remain exactly:

- META
- STATE
- ACTIVE_TASK
- EXPERIENCES
- EVENTS

STATE domains currently available in the physical slice:

- `_root`
- inventory
- equipment
- preferences
- plans

The absence of a Recipes tab is intentional in the current slice, not evidence that Recipe persistence is solved.

Sequential multi-client use only. Concurrent conflict resolution remains out of scope.

## 5. Validation evidence registry

Machine-readable evidence is authoritative for release inheritance:

`tests/VALIDATION_REGISTRY.yaml`

A historical gate may be inherited by a later release candidate only when the registry's guarded product files retain their expected Git blob identities.

This prevents documentation-only release commits from forcing unnecessary full reruns while preventing silent product changes from borrowing stale validation evidence.

## 6. Release-hardening rule

Milestone gates prove individual boundaries. A release baseline additionally requires:

1. synchronized README / deployment / validation metadata;
2. deterministic static repository validation;
3. current-HEAD composite regression for boundaries touched by later shared infrastructure changes;
4. durable result reporting and cleanup evidence;
5. a release/tag only after the current release issue is completed.

The v0.8.1 release gate is tracked in GitHub Issue #7.

## 7. Explicitly unvalidated boundaries

Do not claim the following merely because the canonical architecture permits them:

- Web ↔ Codex portability.
- local SQLite/file provider.
- Notion/Tencent Docs provider.
- concurrent writer merge/conflict resolution.
- independent Inventory DomainModule.
- independent Planning DomainModule.
- independent Equipment DomainModule.
- durable Recipe provider mapping/migration.
- automatic background compaction scheduling.

These are future experiments, not current guarantees.
