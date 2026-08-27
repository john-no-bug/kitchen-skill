# Evaluator Expectations — Event/Experience Compaction + Long-History Context

Evaluator-only. Load only after C0/S0, history growth, M1 compaction, C1/S1, selected-context measurements, and candidate/provider traces are frozen.

## Baseline

1. C0 normal Cooking retrieval contains zero Events and no more than 2 Experiences.
2. C0 selects the relevant active `frozen_ground_beef:supor_green_pot` Experience when useful.
3. C0 newest direct observation (`broken apart`, `water high`) remains authoritative; Experience is advisory technique history.
4. S0 normal Shopping retrieval contains zero Events and no more than 1 Experience.
5. S0 may select the relevant `shopping_beef:350g_plan` Experience; it must not fabricate price/storage/future-use facts.
6. Baseline selected-context measurements are deterministic and exclude provider search/debug output.

## History growth

7. Event data rows reach exactly 2000: 20 compatible total (3 old + 17 new) plus 1980 noise.
8. Experience data rows reach at least 122, including at least 120 irrelevant/superseded rows.
9. At least 8 superseded/noise Experiences are superficially similar enough to exercise status/relevance filtering but do not reuse the active Experience stable key.
10. Bulk history seeding does not alter the current physical facts used by C0/C1 or the Shopping request facts used by S0/S1.

## Compaction

11. M1 compaction runs through `HealthEngine -> RepairPlan/ChangeSet -> PersistenceCoordinator -> StorageProvider`; no DomainModule writes provider directly.
12. Compaction candidate reasoning is bounded to <=64 Event payloads and <=8 existing Experience payloads.
13. Exactly the 17 new compatible unique Events are accepted as new evidence; old already-accounted or noise Events do not inflate evidence_count.
14. Existing Experience `meta.id=exp-frozen-beef-supor-pot` and `key=frozen_ground_beef:supor_green_pot` remain stable.
15. `evidence_count` becomes exactly 20.
16. `evidence_event_refs` contains at most 8 refs and does not grow in proportion to evidence_count.
17. Experience summary/conditions/learned_value remain compact reusable knowledge and contain no raw transcript/history dump.
18. Status remains active and confidence is not used to invent exact numeric rules.
19. All 2000 Event rows remain append-only/present after compaction; no supporting Event is deleted or rewritten.
20. `Meta.last_compaction_at` advances only with the successful durable compaction commit.
21. Compaction does not create a new storage table/collection.

## Long-history normal retrieval

22. C1 candidate generation reads no EVENTS.
23. C1 selects no more than 2 Experiences and selects the relevant active Experience over irrelevant/superseded noise.
24. C1 does not dereference selected Experience `evidence_event_refs` into Events.
25. C1 current direct observation still outranks the Experience.
26. S1 candidate generation reads no EVENTS.
27. S1 selects no more than 1 Experience and excludes irrelevant/superseded noise.
28. C0 -> C1 selected persisted-record byte growth is bounded: post <= baseline + 2048 bytes and <=1.5x baseline when the ratio is meaningful.
29. S0 -> S1 selected persisted-record byte growth is bounded under the same rule.
30. Any small post-history growth is explainable by compact metadata such as evidence_count / capped refs rather than raw history rows.
31. ContextPack selected-record counts do not grow with 2000 Event rows or 122+ Experience rows.

## Architecture preservation

32. Cooking and Shopping domain files contain no Google Drive/Sheets API details and are not modified merely to compact history.
33. Event/Experience compaction uses existing canonical objects and the existing five Google Sheets tabs.
34. Provider-internal search/scan effort is not confused with ContextPack size; only bounded candidate outputs enter model reasoning.
35. Unknown/precision/evidence-precedence invariants remain intact.

## Harness completion

36. Evaluator expectations were not read until all candidate responses, context measurements, compaction decisions, and provider traces were frozen.
37. Before cleanup, the full frozen evaluation is written to `john-no-bug/kitchen-skill` Issue #6 with TEST_COMMIT, TEST_STORE_URL, history counts, baseline/post ContextPack measurements, compaction evidence, criteria, and failure classes.
38. PASS path deletes the temporary Sheet only after result writeback, verifies it unavailable, adds cleanup receipt, then closes Issue #6 completed.
39. FAIL path retains the temporary Sheet and leaves Issue #6 open.
40. Missing/ambiguous evidence that prevents judging a required criterion is `harness_defect`, not an automatic PASS.

## Pass decision

PASS only if all required exercised criteria pass and there is no architecture-boundary violation.

## Failure classes

- `compaction_selection`
- `experience_merge`
- `experience_payload_growth`
- `retrieval_boundedness`
- `event_leakage`
- `evidence_precedence`
- `persistence_write`
- `domain_coupling`
- `harness_defect`
