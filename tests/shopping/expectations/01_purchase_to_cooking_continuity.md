# Evaluator Expectations — Shopping Purchase to Fresh Cooking

Evaluator-only. Load only after Session A execution and all Session B candidate responses are frozen.

Session A does not read this file. Session A instead writes a non-evaluative frozen evidence escrow comment to Issue #3 before handoff. Session B may read that evidence comment only after B1/B2 are frozen.

## Session A — Shopping

1. A1 recommends the 500 g package by default because about 350 g is planned and 500 g covers it with less surplus/waste than 1 kg when price is explicitly excluded and no contrary storage/future-use evidence exists.
2. A1 does not fabricate price/unit-price/freshness facts and does not turn the decision into a questionnaire.
3. Shopping uses/creates `ActiveTask(type=shopping)` only as compact operational state.
4. A2 is treated as purchase confirmation without asking the user to enter inventory again.
5. The labelled 500 g package becomes canonical ground-beef inventory using v0.5 Amount semantics: `amount.mode=exact`, `value=500`, `unit=g`; stable inventory ID is retained. An ad-hoc `precision` field must not replace canonical `Amount.mode`.
6. A compact append-only `purchase_inventory` Event records the purchase without storing the raw transcript.
7. The A2 semantic write flows through ChangeSet -> PersistenceCoordinator -> provider.
8. Shopping ActiveTask is completed/cleared after purchase and META has no current active task before Session B.
9. No Shopping-specific storage tab/table is created.

Criteria 1–7 must be judged from the matching frozen Session A evidence escrow comment plus bounded store readbacks. Do not infer unobserved A1/A2 user-facing behavior merely from the final store.

## Session B — Fresh Cooking

10. Session B receives no Session A transcript/state summary/purchase Event/evidence contents through the user handoff and does not request a recap.
11. Bootstrap reads only META plus current ActiveTask if one exists; because Shopping was cleared, no Shopping task should be revived.
12. The explicit B1 cooking request routes to Cooking.
13. B1 retrieves the beef inventory from STATE using bounded task-specific lookup; the purchase Event is not required or loaded for candidate generation.
14. B1 correctly recognizes that the recorded 500 g purchase is enough for a one-person dish and does not claim the purchase came from remembered Shopping chat.
15. B1 current observation `牛肉现在是冷藏的` is authoritative for current physical state.
16. A new `ActiveTask(type=cooking)` is created/persisted through the normal coordinator/provider path.
17. Cooking domain files contain no Google Drive/Sheets provider API dependency and were not rewritten for Shopping.
18. B2's `大概120g` consumption updates remaining inventory through semantic persistence.
19. Precision result uses canonical Amount semantics: exact 500 g minus approximately 120 g becomes `amount.mode=approximate` around 380 g, never `mode=exact` 380 g.
20. B2 gives useful current beef-cooking guidance and does not restart Shopping or require purchase history.
21. Normal candidate retrieval remains bounded and does not load full EVENTS/history/whole spreadsheet.
22. Unknown fields not established by the run remain unknown rather than fabricated.

## Evidence isolation and harness completion

23. Before user handoff, Session A durably writes exactly one matching frozen evidence escrow comment to Issue #3. It includes TEST_COMMIT, TEST_STORE_URL, frozen A1/A2 responses, bounded A1 Shopping ActiveTask readback, A1/A2 provider read/write trace, A2 ChangeSet/PersistenceCoordinator/provider-path evidence, canonical purchase/Event/task-clear readbacks, and `EVALUATOR_EXPECTATIONS_READ: false`. It contains no evaluator scores or expectations.
24. Session B does not read the Session A evidence escrow comment or evaluator expectations before B1/B2 are frozen. After freeze, it reads exactly the matching evidence comment for TEST_COMMIT + TEST_STORE_URL and uses it only for evaluation.
25. Before cleanup, the frozen final evaluation result is written to `john-no-bug/kitchen-skill` Issue #3 and includes TEST_COMMIT, TEST_STORE_URL, criteria, failure classes, bounded-read/write evidence, the Session A evidence comment ID/URL, evidence-isolation confirmation, and latest relevant revisions.
26. PASS path deletes the temporary test Sheet after result writeback, verifies it unavailable, records cleanup receipt, and closes Issue #3 completed.
27. FAIL path retains the test store for debugging and leaves Issue #3 open.
28. Missing/ambiguous Session A evidence escrow, pre-freeze reading of that evidence, or failure to durably report the final result to Issue #3 is `harness_defect` and forces overall FAIL.

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
