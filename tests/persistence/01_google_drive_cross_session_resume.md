# Persistence Acceptance Test 01 — Google Drive Cross-Session Resume

Status: separate persistence test; **not** part of the existing Pure Web regression manifest.

## Purpose

Validate the first durable vertical slice:

> The same Cooking domain behavior continues across a fresh chat through Google Drive without full-history replay or provider-specific Cooking logic.

This scenario is intended for a real Web host with the Google Drive/Sheets provider available.

## Preconditions

- load `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_LIVE_COOKING.md` in both chats;
- both chats can access the same Google Drive account/store;
- use one compatible `Kitchen Skill Store`;
- sequential use only: finish Chat A writes before starting Chat B;
- do not read evaluator notes while generating candidate responses.

## Chat A — establish persistent live task

### Turn A1

User:

> 我想做一人份番茄牛肉意面。牛肉是冷冻肉末，大概还有500g；有洋葱、意面、橄榄油、盐。番茄酱我不确定是哪种。锅还是那个苏泊尔小绿锅，可以开盖加热和炒。

Expected structural behavior:

- initialize/resolve Drive store without making the user maintain tables;
- ask about tomato product only if/when it changes the next decision;
- persist relevant equipment/inventory observations at their actual precision;
- create/update `ActiveTask(type=cooking)` through PersistenceCoordinator.

### Turn A2

User:

> 我先弄牛肉。现在已经能铲散了，但锅里水很多，洋葱还没加。

Expected structural behavior:

- current state becomes `beef broken apart + water high + onion not added`;
- do not keep treating beef as a frozen block;
- guidance should focus on evaporating water before real browning;
- durable ActiveTask update occurs through the coordinator/provider path.

### Turn A3

User:

> 这次牛肉大概用了120g。现在我先停一下，晚点继续。

Expected structural behavior:

- inventory math preserves approximation (`~500 g - ~120 g` is still approximate);
- task may become paused but remains resumable;
- META points to the current task;
- relevant state/task write is durably committed before Chat A ends.

## Store inspection between chats

Verify without loading full history into a candidate response:

- META has compatible store marker and non-null active_task_id;
- ACTIVE_TASK contains one compact current task, not the transcript;
- STATE contains only canonical current records/metadata needed for continuity;
- EVENTS, if present, are append-only and are not needed for normal resume;
- no provider credentials or raw chat transcript were stored.

## Chat B — fresh session resume

Start a completely fresh chat with the same bundle/store. Do not paste Chat A transcript.

### Turn B1

User:

> 继续。锅里已经没明显积水，开始滋滋响了，洋葱还没加。

Pass behavior:

- bootstrap from Drive META + ACTIVE_TASK rather than asking for a full recap;
- newest B1 observation overrides stored `water high` state;
- do not repeat soften/break-apart steps;
- advise current browning/add-onion dependency from the new physical state;
- retrieve only directly relevant state/equipment and at most a tiny Experience set;
- persist the corrected ActiveTask after reasoning.

### Turn B2

User:

> 洋葱我已经倒进去了，现在有点粘锅，下一步呢？

Pass behavior:

- `onion added` invalidates any pending add-onion instruction;
- adapt locally to the current sticking state rather than restarting the recipe;
- persist the new task state through the same coordinator/provider path.

## Acceptance criteria

All must pass:

1. `modules/cooking/contract.md` and `modules/cooking/logic.md` required no provider-specific rewrite.
2. Chat B resumes without the user replaying Chat A.
3. Bootstrap reads are bounded to META/current ActiveTask.
4. Normal Cooking retrieval excludes full EVENTS/history.
5. Current B1 observation outranks stored A2 physical state.
6. Completed major steps are not repeated.
7. Approximate inventory remains approximate.
8. Domain logic does not call Drive/Sheets directly.
9. All semantic writes pass through PersistenceCoordinator.
10. Failed durable writes, if simulated, do not block safe cooking and do not produce false save claims.
11. The provider store contains canonical Kitchen data only, not raw transcript/general assistant memory.
12. ContextPack size does not grow with Event history.

## Failure diagnostics

When this test fails, classify the smallest broken boundary:

- store discovery/provider;
- bounded Retriever;
- evidence precedence;
- ChangeSet normalization;
- PersistenceCoordinator validation;
- provider commit;
- Health/re-anchor;
- user-facing Cooking behavior.

Patch the boundary, not wording differences.
