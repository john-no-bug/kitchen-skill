# Shopping Acceptance 01 — Purchase to Fresh Cooking Continuity

Candidate-visible script. Do not read `tests/shopping/expectations/*` until all Session B candidate responses are frozen.

## Session A — Shopping

### A1

User:

> 我接下来准备做两顿番茄牛肉意面，两顿合计大概需要350g牛肉。店里有500g一包和1kg一包，价格先不考虑，你觉得买哪个更合适？

### A2

User:

> 好，我买500g这包了，包装标的是500g。

End Session A after all semantic writes for A2 have completed.

## Session B — genuinely fresh Cooking conversation

Do not provide Session A transcript, state summary, purchase Event, or ActiveTask JSON.

### B1

User:

> 我要开始做一人份番茄牛肉意面。这包牛肉现在是冷藏的。牛肉还够吗？如果够就从牛肉开始。

### B2

User:

> 我取了大概120g下锅了，剩下的先收起来。现在先怎么弄牛肉？

Freeze B1 and B2 candidate responses before loading evaluator-only expectations.
