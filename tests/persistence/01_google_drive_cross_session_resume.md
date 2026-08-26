# Persistence Scenario 01 — Google Drive Cross-Session Resume

Status: candidate-visible integration script; **not** part of the Pure Web regression manifest.

## Purpose

Exercise the Web + Google Drive Live Cooking deployment across two genuinely separate conversations.

Do not read `tests/persistence/expectations/*` while generating candidate responses.

## Preconditions

- both sessions pin the same repository commit;
- both sessions load `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_LIVE_COOKING.md` from that commit;
- both sessions can access the same isolated temporary Google Drive Kitchen test store;
- Session A finishes all writes before Session B starts;
- Session B must not receive the Session A transcript, an ActiveTask dump, a state summary, or evaluator notes.

## Session A — establish persistent live task

Process these user turns sequentially. Do not batch-answer them.

### Turn A1

User:

> 我想做一人份番茄牛肉意面。牛肉是冷冻肉末，大概还有500g；有洋葱、意面、橄榄油、盐。番茄酱我不确定是哪种。锅还是那个苏泊尔小绿锅，可以开盖加热和炒。

### Turn A2

User:

> 我先弄牛肉。现在已经能铲散了，但锅里水很多，洋葱还没加。

### Turn A3

User:

> 这次牛肉大概用了120g。现在我先停一下，晚点继续。

After A3, finish all intended durable writes before ending Session A.

The only continuity data that may be handed manually to Session B is:

- exact tested repository commit SHA;
- exact temporary Kitchen test-store URL or file ID.

Do not hand Session B any task-state content.

## Session B — fresh-session resume

Start a completely fresh conversation. Use the exact commit and exact test store from Session A. Do not paste or summarize Session A.

Process these turns sequentially.

### Turn B1

User:

> 继续。锅里已经没明显积水，开始滋滋响了，洋葱还没加。

### Turn B2

User:

> 洋葱我已经倒进去了，现在有点粘锅，下一步呢？

After B2, finish all intended durable writes.

## Candidate transcript freeze

Freeze all candidate-visible Session A and Session B responses before reading evaluator-only files.

Evaluator-only material begins at:

`tests/persistence/expectations/01_google_drive_cross_session_resume.md`

Do not revise candidate responses after evaluator material is loaded.
