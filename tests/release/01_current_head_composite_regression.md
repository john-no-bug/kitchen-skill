# Current-HEAD Composite Release Regression

This script defines the exact release candidate user turns and fault-injection phases.

## Session A — Shopping

### A1

`我接下来准备做两顿番茄牛肉意面，两顿合计大概需要350g牛肉。店里有500g一包和1kg一包，价格先不考虑，你觉得买哪个更合适？`

Expected candidate behavior is evaluated later, not during execution.

### A2

`好，我买500g这包了，包装标的是500g。`

After A2 semantic persistence succeeds, Session A ends after its non-evaluative evidence escrow and continuity handoff.

## Session B — genuinely fresh Cooking + reliability

Session B receives only:

- TEST_COMMIT
- TEST_STORE_URL
- DEAD_TARGET_URL
- the Session B runner prompt

No Session A transcript/state/Event/task/evaluator content is allowed in the handoff.

Before B1, Session B must load pinned `schemas/active_task.yaml` and `tests/release/active_task_shape.yaml`. Every persisted Cooking ActiveTask in B1-B4 must pass that candidate-visible canonical shape contract before provider commit. Module-specific operational facts belong under canonical `state`; `completed` / `next` are canonical task-step lists. A shape-invalid task mutation is `harness_defect` and must not be physically committed.

### B1

`我要开始做一人份番茄牛肉意面。这包牛肉现在是冷藏的。牛肉还够吗？如果够就从牛肉开始。`

B1 should route from the explicit current Cooking request and retrieve current beef inventory from STATE, not purchase Event history.

Before persisting the new Cooking task, freeze and validate the complete canonical task payload, record `ACTIVE_TASK_SHAPE_VALID: true`, then commit through PersistenceCoordinator/provider.

### B2

`我取了大概120g下锅了，剩下的先收起来。现在先怎么弄牛肉？`

The approximate current observation must update canonical inventory through the normal semantic persistence path. Exact 500 g minus approximate 120 g must become approximate remaining quantity around 380 g, never exact 380 g.

The B2 atomic semantic write must include a canonical ActiveTask update that independently passes `tests/release/active_task_shape.yaml`; a correct inventory mutation cannot compensate for an invalid task payload.

### B3 — failed durable write turn

`牛肉已经明显褐色，洋葱已经倒进去，还有一点粘锅。现在怎么办？`

Execution discipline:

1. bounded-read the valid store needed for current task state;
2. freeze the user-facing B3 response and semantic ChangeSet from the newest direct observation;
3. make the pending ActiveTask canonical: all module facts under `state`, with canonical task-step lists only in `completed` / `next`;
4. validate against `tests/release/active_task_shape.yaml` and record `ACTIVE_TASK_SHAPE_VALID: true`;
5. only after semantic shape validation, route the exact provider commit batch for that semantic change to DEAD_TARGET_URL;
6. the dead target must already have been permanently deleted in Session A;
7. record the real provider failure receipt/error;
8. do not mutate the valid store as a substitute for the failed attempt;
9. verify valid META revision and affected ActiveTask remain pre-B3;
10. retain the canonical B3 semantic change as session-pending.

### B4 — provider recovery

`继续。`

Before generating B4:

1. restore provider target to TEST_STORE_URL;
2. bounded-refresh META + only affected current records;
3. rebase/retry the retained B3 pending semantic change through PersistenceCoordinator -> StorageProvider;
4. revalidate the retained/rebased task with `tests/release/active_task_shape.yaml` and record `ACTIVE_TASK_SHAPE_VALID: true`;
5. verify the retry succeeds and advances global revision exactly once;
6. verify durable current task is canonical and now contains beef browned=true, onion added=true, pan sticking=slight (or semantically equivalent facts under `state`);
7. generate/freeze B4 from this recovered newest state without repeating beef browning or adding onion again.

## Candidate retrieval rules

Across B1-B4 candidate generation:

- normal bootstrap is META + current ActiveTask only when META points to one;
- task-specific STATE lookup remains bounded;
- normal candidate generation reads zero EVENTS;
- Experiences remain within current Web limits when relevant;
- no Issue #7 comment/evaluator content may enter candidate generation.

## Freeze boundary

Only after B1, B2, B3, B4 responses and all candidate/provider traces are frozen may evaluator-only material be loaded:

- `tests/release/expectations/01_current_head_composite_regression.md`
- matching Session A frozen evidence from Issue #7
- static-validation evidence comment for TEST_COMMIT from Issue #7
- purchase Event / final bounded store audit if required by evaluator

Evaluator must also audit the frozen/read-back ActiveTask payloads against `tests/release/active_task_shape.yaml`. Physical provider acceptance of a noncanonical task never counts as semantic persistence success.

Do not regenerate candidate responses after evaluator material is loaded.
