# Evaluator Expectations — Google Drive Cross-Session Resume

Evaluator-only. Load this file only after all Session A and Session B candidate responses are frozen.

## Gate

All criteria below are required. A failure should be assigned to the smallest broken boundary rather than to wording differences.

## Session A expectations

1. The temporary store is resolved/created without requiring the user to design or maintain tables.
2. Relevant observations are persisted at their actual precision.
3. By A2, current task state reflects beef broken apart, high water, and onion not added; the candidate does not keep reasoning from a frozen-block state.
4. A3 preserves approximate arithmetic: approximately 500 g minus approximately 120 g remains approximate rather than becoming an exact 380 g fact.
5. The task remains resumable after the user pauses; META points to the current active/paused task as appropriate.
6. Durable writes follow the documented semantic path through PersistenceCoordinator rather than a Cooking-to-Drive direct write.
7. No raw chat transcript, provider credential, or unrelated general memory is written to the Kitchen store.

## Between-session store expectations

8. META contains the compatible store marker and the continuity pointer needed for bootstrap.
9. ACTIVE_TASK contains one compact operational task rather than the conversation transcript.
10. STATE contains canonical current records needed for continuity.
11. EVENTS, if present, are append-only/cold data and are not required for normal Session B bootstrap.

## Session B expectations

12. Session B resumes the cooking task without receiving or requesting a full recap of Session A.
13. Bootstrap is bounded to tiny continuity data: META plus current ActiveTask before task-specific retrieval.
14. Normal cooking retrieval does not load the full EVENTS history or whole spreadsheet merely because it exists.
15. B1's newest direct observation (`no obvious pooled water`, `sizzling`, `onion not added`) overrides any older persisted wet-beef state.
16. The candidate does not repeat already-completed soften/break-apart work.
17. Guidance continues from the current browning/add-onion dependency and remains concise Live Cooking guidance.
18. B1's corrected physical/task state is durably persisted after reasoning.
19. At B2, `onion already added` invalidates any pending add-onion instruction.
20. The candidate adapts locally to sticking rather than restarting the recipe.
21. B2 task-state changes again use the same PersistenceCoordinator/provider path.

## Architecture preservation expectations

22. `modules/cooking/contract.md` and `modules/cooking/logic.md` do not contain Google Drive/Sheets provider API dependencies.
23. Current direct observation outranks persisted state.
24. Unknown remains unknown; approximate information is not upgraded to exact without evidence.
25. Context size is structurally bounded and does not grow in proportion to Event history.
26. If a durable write failure is actually encountered during the run, safe cooking guidance continues and the candidate does not falsely claim durable success.

## Pass decision

PASS only if all required criteria that are exercised by the run pass and there is no architecture-boundary violation.

If a criterion requiring an injected failure was not exercised (for example durable-write failure), mark it `NOT_EXERCISED`, not PASS. Such a result does not block the cross-session-resume gate but must be covered by the later failure/degradation suite.

## Failure classification

Use one primary class per concrete failure:

- `provider_resolution`
- `persistent_retrieval`
- `persistence_write`
- `state_precedence`
- `cooking_regression`
- `instruction_leak`
- `harness_defect`

For every failure, report:

- session and turn;
- observed behavior;
- violated criterion number;
- smallest likely boundary to patch;
- whether the failure is deterministic or uncertain.
