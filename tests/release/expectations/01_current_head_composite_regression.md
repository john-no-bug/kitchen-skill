# Evaluator Expectations — v0.8.1 Current-HEAD Composite Release Gate

Evaluator-only. Load only after Session A candidate evidence and all Session B B1-B4 responses/provider traces are frozen.

## Release metadata / inherited evidence

1. TEST_COMMIT is the exact release-candidate HEAD used for all candidate/repository reads.
2. `tests/VALIDATION_REGISTRY.yaml` parses and all declared blob guards match TEST_COMMIT.
3. A durable Issue #7 static-validation evidence comment exists for TEST_COMMIT and reports the deterministic repository validator PASS.
4. Pure Web inheritance is valid only if `SKILL.md` and `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md` both retain validated blob `37a8d15bb376579a9a33ede514b121dff04c249d` and remain identical.
5. v0.8 history inheritance is valid only if the guarded health/retrieval/persistence/v0.8 dist blobs match the registry.
6. Deployment metadata identifies Pure Web fallback separately from Web + Google Drive v0.8 release candidate; root `SKILL.md` is not silently repurposed.

## Session A — Shopping

7. A1 recommends 500 g because ~350 g planned need is covered with less surplus than 1 kg when price is explicitly excluded.
8. A1 invents no price/unit-price/freshness/storage fact and does not turn the choice into a questionnaire.
9. A2 treats the purchase statement itself as inventory capture and does not request duplicate manual inventory entry.
10. The labelled package becomes one stable canonical ground-beef inventory record with `Amount.mode=exact,value=500,unit=g`.
11. A compact append-only purchase Event exists without raw transcript content.
12. Shopping ActiveTask is cleared/completed and `META.active_task_id=null` before the handoff.
13. Session A evidence escrow is non-evaluative, frozen before handoff, includes A1/A2 responses and actual write-path evidence, and confirms evaluator expectations were unread.
14. The sacrificial DEAD_TARGET was really created then permanently deleted before Session B; a provider probe proves it unavailable/not-found.

## Session B — fresh Cooking

15. Session B receives only TEST_COMMIT, TEST_STORE_URL, DEAD_TARGET_URL and the runner prompt; no Session A transcript/state summary/Event/task/evaluator content.
16. Before B1, bootstrap reads META only because Shopping was cleared; no Shopping task is revived.
17. B1 routes from explicit current Cooking intent.
18. B1 retrieves beef from bounded STATE rather than purchase Event/history and recognizes recorded 500 g is enough for one person.
19. B1 honors the current direct observation that the beef is refrigerated.
20. A new Cooking ActiveTask is persisted through the normal semantic coordinator/provider path and its canonical payload passes `tests/release/active_task_shape.yaml` before provider commit.
21. B2 approximate 120 g consumption updates inventory through semantic persistence, and the same atomic semantic write carries a canonical shape-valid ActiveTask update.
22. Exact 500 g minus approximate 120 g becomes `Amount.mode=approximate` around 380 g, never exact 380 g.
23. B1/B2 user-facing guidance remains useful Live Cooking and exposes no storage architecture.

## B3 — real failed durable write

24. B3 newest direct observation controls reasoning: beef is already browned, onion is already added, pan sticking is slight.
25. B3 does not repeat beef browning as pending work or instruct the user to add onion again.
26. The B3 response and semantic ChangeSet are frozen before the provider failure is injected; the pending ActiveTask is canonical shape-valid before provider normalization/commit routing.
27. The exact B3 provider commit attempt is routed to the already-deleted DEAD_TARGET and fails at the real provider boundary (e.g. 404/not-found), not by a fabricated logical error.
28. No durable-success receipt/status is produced for B3 and the user-facing response does not claim the state was durably saved.
29. The newest B3 canonical semantic change remains session-pending after the failed provider commit.
30. Valid TEST_STORE META.global_revision does not advance as a result of the failed B3 write.
31. The valid current ActiveTask remains pre-B3 immediately after failure; no partial B3 state appears in the valid store.

## B4 — recovery retry

32. Provider target is restored to the exact TEST_STORE_URL without changing domain facts.
33. Recovery refresh is bounded to META + affected current records; it does not load Events/history.
34. The retained B3 pending change is shape-revalidated and retried/rebased through PersistenceCoordinator -> StorageProvider, not by DomainModule/provider coupling.
35. Successful retry advances global revision exactly once relative to the post-B2 pre-B3 baseline.
36. Durable current task after retry is a canonical ActiveTask and contains the newest B3 facts under canonical state: beef browned, onion already added, slight sticking (semantically equivalent representation allowed).
37. B4 continues from the recovered newest state and does not regress to pre-browning or re-add onion.

## Boundedness / architecture

38. No B1-B4 candidate trace loads EVENTS/history.
39. Experience retrieval, if any, stays within current Web limits and does not dereference evidence Event refs.
40. Current direct observations outrank any stored Experience/history-derived pattern.
41. Cooking/Shopping domain files contain no Google Drive/Sheets provider API dependency.
42. Google Drive physical store remains the existing five-tab profile; release hardening adds no provider table/schema migration.

## Harness / cleanup

43. Issue #7 comments and evaluator expectations remain unread by Session B until B1-B4 and provider traces are frozen.
44. One complete frozen result is durably posted to Issue #7 before cleanup and includes TEST_COMMIT/store/dead target, all criterion results, failure classes, frozen responses, provider trace, revision evidence, registry/blob inheritance evidence, static-validation evidence reference, and canonical ActiveTask shape-validation evidence.
45. PASS path deletes the valid temporary Kitchen Sheet after frozen result writeback, verifies unavailable/not-found, and appends a cleanup receipt.
46. FAIL path retains the valid store for debugging and keeps Issue #7 open.
47. The test runner does not modify production Kitchen data or candidate product/release files while evaluating the candidate.
48. Missing/ambiguous escrow, static evidence, provider trace, shape-validation trace, or durable result reporting is `harness_defect` and forces overall FAIL.
49. Candidate-visible `tests/release/active_task_shape.yaml` is loaded before B1 and matches the release harness canonical top-level contract; every B1/B2/B3/B4 ActiveTask semantic payload records `ACTIVE_TASK_SHAPE_VALID: true` before any physical provider commit.
50. Provider acceptance alone never satisfies semantic persistence: evaluator audits frozen/read-back ActiveTask payloads and rejects any module-specific top-level state such as `ingredient_states`, `equipment_state`, `completed_milestones`, `next_actions`, `pan_state`, or `inventory_refs`.

## Pass decision

PASS only if all applicable criteria above pass. Do not patch candidate behavior after evaluator material is loaded.

The runner must leave Issue #7 open after a successful test cleanup. The development session performs the final metadata-only registry/docs freeze commit, verifies static CI for that freeze commit, then closes Issue #7 and may create the validated release/tag.

## Failure classes

- `release_registry`
- `static_validation`
- `shopping_regression`
- `persistent_retrieval`
- `precision_semantics`
- `degraded_write_handling`
- `false_durability_claim`
- `pending_change_loss`
- `retry_recovery`
- `revision_integrity`
- `event_leakage`
- `domain_coupling`
- `harness_defect`
