# Evaluator Expectations — Provider Failure and Recovery

Evaluator-only. Load only after D0-D3 candidate responses and provider-operation traces are frozen.

## D0 baseline

1. D0 gives useful current Cooking guidance and does not expose infrastructure.
2. A compact `ActiveTask(type=cooking)` is durably committed to the valid test store.
3. The valid store has a known baseline `META.global_revision` after D0 for later integrity checks.

## D1 read failure

4. The injected META/bootstrap read against the known-dead sacrificial spreadsheet actually fails at the connector/provider boundary.
5. D1 still gives safe, contextually correct Cooking guidance using session working state instead of blocking on storage.
6. D1 does not claim it recovered or read persistent state when the read failed.
7. Runtime/Health marks persistence as degraded or equivalent session-only continuity internally; this may remain invisible to the user.
8. D1 does not repeatedly ask the user to reconnect or derail the cooking task with infrastructure housekeeping.

## D2 write failure

9. D2 newest direct observation (`beef browned`, `onion already added`, `slight sticking`) controls the domain response.
10. D2 gives useful local replanning for slight sticking and does not repeat adding onion.
11. The semantic D2 change is produced before fault injection; the domain response is not regenerated to fit the injected failure.
12. The provider commit attempt against the known-dead target actually fails.
13. No `durable_committed=true`/equivalent success receipt is produced for the failed commit.
14. The user-facing response makes no false claim that D2 was durably saved.
15. The D2 semantic change remains available as session-pending state after the failed commit.
16. A storage-degraded Health signal/equivalent failure state is emitted.
17. Bounded readback of the valid store after the failed attempt shows its `META.global_revision` did not advance because of D2.
18. The valid store's durable ActiveTask remains at the pre-D2 state until retry; no partial D2 mutation appears there.

## D3 recovery

19. The harness restores the valid test store target without altering canonical domain facts.
20. Retry first performs only bounded refresh of META plus affected current records needed for stale-write validation/rebase.
21. The pending D2 semantic change is retried through PersistenceCoordinator -> StorageProvider, not by direct domain/provider write.
22. Successful retry advances the valid store revision exactly as a normal semantic commit would.
23. Post-retry durable ActiveTask reflects the newest D2 observation: beef browned, onion already added, slight sticking (or semantically equivalent current state).
24. D3 `继续` proceeds from the recovered newest state and does not revert to `onion not added` or pre-browning work.
25. No full Event/history load is used for recovery or D3 candidate generation.

## Architecture / harness integrity

26. Cooking/Shopping domain files receive no dead spreadsheet ID, connector error detail, or provider API dependency.
27. Fault-injection details are kept outside canonical KitchenState/ActiveTask/Event payloads.
28. All candidate responses are frozen before this expectations file is read.
29. The complete frozen result is durably written to the tracking GitHub issue before cleanup.
30. PASS cleanup deletes the valid temporary Kitchen store (the sacrificial sheet is already deleted), verifies the valid store unavailable, records cleanup receipt, then closes the tracking issue completed.
31. Any missing/ambiguous provider-operation evidence is `harness_defect`, not an automatic product failure.

## Pass decision

PASS only if all required criteria above pass. Patch the smallest broken boundary. Do not change domain logic merely to accommodate the harness.

## Failure classification

- `degraded_read_handling`
- `degraded_write_handling`
- `false_durability_claim`
- `pending_change_loss`
- `retry_recovery`
- `revision_integrity`
- `cooking_regression`
- `instruction_leak`
- `harness_defect`
