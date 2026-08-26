# Context Retriever — Web + Google Drive

## Goal

Produce the smallest useful persistent ContextPack for the current task without loading full Drive state/history.

This implementation is read-only.

## Bootstrap

For every new turn, bootstrap only enough continuity to route:

1. read the one `META` row;
2. if `active_task_id` exists, read the one `ACTIVE_TASK` row;
3. return only the routing projection: task id/type/goal/phase + last activity/health status + continuity confidence.

Do not read STATE, EXPERIENCES, or EVENTS during bootstrap merely because they exist.

A fresh Chat B should therefore be able to discover an active cooking task without replaying Chat A.

## Cooking retrieval

After Cooking is selected, retrieve only what the current decision needs.

Default slots:

- current direct user observation from the newest message;
- full compact ActiveTask;
- specific inventory rows named by ActiveTask/current request;
- specific equipment rows referenced by ActiveTask;
- relevant preference rows only when they change the current action;
- at most 1–2 relevant Experience rows;
- due checks that materially affect the action;
- no Events by default.

## Suggested hard limits for this slice

```yaml
max_state_records: 12
max_experiences: 2
max_events: 0
max_recipes: 1
```

These are implementation defaults, not canonical schema limits.

## Lookup strategy

Prefer, in order:

1. direct `(domain, id)` lookup from ActiveTask/entity refs;
2. bounded exact/name/key row search;
3. provider text search over small projection/search fields;
4. mark unknown when no reliable record is found.

Do not scan old Events or whole history to avoid one necessary decision-changing question.

## Evidence precedence

When retrieved storage conflicts with the newest message:

1. newest direct observation wins;
2. ActiveTask is next;
3. KitchenState rows follow;
4. recent Event only if explicitly retrieved;
5. Experience;
6. old conversation.

Example:

Stored ActiveTask says beef water level is high. In fresh Chat B the user says the pot has no visible pooled water and is sizzling. Build the ContextPack from `no pooled water + sizzling`; do not continue acting as if water is high.

## Freshness

For volatile inventory, old timestamps lower confidence; they do not turn quantity into zero or absent.

Generate a DueCheck only when the stale fact materially affects current cooking/safety. Stable equipment capability may remain trusted much longer.

## Provider degradation

If the Drive provider cannot be read:

- use the visible conversation as best-effort continuity;
- do not claim persistent state was recovered;
- keep current cooking useful;
- surface a storage degradation signal to Health;
- avoid a full-history reconstruction attempt.
