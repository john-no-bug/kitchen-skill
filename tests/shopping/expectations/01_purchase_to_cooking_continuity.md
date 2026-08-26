# Evaluator Expectations — Shopping Purchase to Fresh Cooking

Evaluator-only. Load only after Session A execution and all Session B candidate responses are frozen.

## Session A — Shopping

1. A1 recommends the 500 g package by default because about 350 g is planned and 500 g covers it with less surplus/waste than 1 kg when price is explicitly excluded and no contrary storage/future-use evidence exists.
2. A1 does not fabricate price/unit-price/freshness facts and does not turn the decision into a questionnaire.
3. Shopping uses/creates `ActiveTask(type=shopping)` only as compact operational state.
4. A2 is treated as purchase confirmation without asking the user to enter inventory again.
5. The labelled 500 g package becomes canonical ground-beef inventory at evidence-backed precision; stable inventory ID is retained.
6. A compact append-only `purchase_inventory` Event records the purchase without storing the raw transcript.
7. The A2 semantic write flows through ChangeSet -> PersistenceCoordinator -> provider.
8. Shopping ActiveTask is completed/cleared after purchase and META has no current active task before Session B.
9. No Shopping-specific storage tab/table is created.

## Session B — Fresh Cooking

10. Session B receives no Session A transcript/state summary/purchase Event and does not request a recap.
11. Bootstrap reads only META plus current ActiveTask if one exists; because Shopping was cleared, no Shopping task should be revived.
12. The explicit B1 cooking request routes to Cooking.
13. B1 retrieves the beef inventory from STATE using bounded task-specific lookup; the purchase Event is not required or loaded for candidate generation.
14. B1 correctly recognizes that the recorded 500 g purchase is enough for a one-person dish and does not claim the purchase came from remembered Shopping chat.
15. B1 current observation `牛肉现在是冷藏的` is authoritative for current physical state.
16. A new `ActiveTask(type=cooking)` is created/persisted through the normal coordinator/provider path.
17. Cooking domain files contain no Google Drive/Sheets provider API dependency and were not rewritten for Shopping.
18. B2's `大概120g` consumption updates remaining inventory through semantic persistence.
19. Precision result is approximate: exact/labelled 500 g minus approximately 120 g may become approximately 380 g, never exact 380 g.
20. B2 gives useful current beef-cooking guidance and does not restart Shopping or require purchase history.
21. Normal candidate retrieval remains bounded and does not load full EVENTS/history/whole spreadsheet.
22. Unknown fields not established by the run remain unknown rather than fabricated.

## Harness completion

23. Before cleanup, the frozen evaluation result is written to `john-no-bug/kitchen-skill` Issue #3 and includes TEST_COMMIT, TEST_STORE_URL, criteria, failure classes, bounded-read/write evidence, and latest relevant revisions.
24. PASS path deletes the temporary test Sheet after result writeback, verifies it unavailable, records cleanup receipt, and closes Issue #3 completed.
25. FAIL path retains the test store for debugging and leaves Issue #3 open.
26. Failure to durably report the result to Issue #3 is `harness_defect` and forces overall FAIL.

## Pass decision

PASS only if all criteria above pass. Patch the smallest broken boundary; do not expand architecture for wording differences.

## Failure classification

- `shopping_logic`
- `purchase_capture`
- `cross_domain_state`
- `persistent_retrieval`
- `persistence_write`
- `precision_semantics`
- `cooking_regression`
- `instruction_leak`
- `harness_defect`
