# Kitchen Skill — v0.7 Validated Cross-Domain Slice + Reliability Gate

Status: v0.7 Shopping -> canonical KitchenState -> fresh Cooking has passed; provider degradation/failure injection is the current reliability gate  
Architecture baseline: frozen v0.4 + v0.5 interface/schema draft

## Validated baselines

### v0.5 — Pure Web Live Cooking

The frozen Pure Web candidate remains unchanged and passed all three required regression suite runs at 36/36.

Preserved files include:

- `SKILL.md`
- `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`
- `modules/cooking/contract.md`
- `modules/cooking/logic.md`
- `tests/manifest.yaml`

### v0.6 — Web + Google Drive persistence

The real two-conversation persistence gate passed at commit `354ba039d8ce56edec7789f01541d3899481c576` and is recorded in GitHub Issue #2.

Validated behavior includes:

- fresh Chat B recovery from Drive without Chat A transcript;
- bounded META + ActiveTask bootstrap;
- current observation overriding persisted stale physical state;
- B1/B2 durable ActiveTask writeback;
- no full Event/history loading for normal Cooking;
- approximate arithmetic remaining approximate;
- result writeback/cleanup harness behavior.

That normal continuity gate intentionally did not inject a provider failure.

### v0.7 — Shopping -> canonical state -> fresh Cooking

The repaired-harness integration gate passed at commit `375a8f61a40409e93c757d6c6f93117e4c31cb86` and is recorded in GitHub Issue #3.

Validated behavior includes:

- Shopping choosing a 500 g package for about 350 g planned use without fabricating price/freshness facts;
- purchase confirmation becoming canonical inventory without duplicate data entry;
- compact append-only `purchase_inventory` Event;
- Shopping ActiveTask cleared before handoff;
- genuinely fresh Cooking session receiving no Shopping transcript/state summary;
- Cooking retrieving purchased beef from bounded STATE rather than Event history;
- new Cooking ActiveTask using the shared canonical state;
- exact 500 g minus approximately 120 g becoming `Amount.mode=approximate` around 380 g;
- no Shopping-specific provider table and no provider API dependency in DomainModules;
- evaluator evidence escrow preserving fresh-session isolation while still making Session A behavior auditable;
- PASS result writeback followed by verified temporary-store cleanup.

This proves Shopping and Cooking can cooperate through canonical KitchenState rather than shared chat history or provider-specific coupling.

## Current reliability gate — provider degradation / failure injection

The next task is to exercise failure behavior already documented by the durable Web runtime, PersistenceCoordinator, and HealthEngine. This is a reliability test, not a new domain feature.

Relevant existing contracts already say that provider failure must:

- keep safe live guidance moving using session working state when possible;
- avoid claiming persistent recovery/read success when a read failed;
- avoid claiming durable save when a write failed;
- retain failed semantic changes as session-pending state;
- preserve valid-store revision integrity on failed commit;
- retry/rebase the pending semantic change after provider recovery;
- keep provider error mechanics outside Cooking/Shopping logic.

The degradation suite uses one dedicated conversation and two isolated test Sheets:

1. one valid Kitchen test store;
2. one sacrificial Sheet deleted immediately so its dead ID can deterministically force real provider read/write failures without corrupting the valid store.

Test artifacts:

- `tests/degradation/manifest.yaml`
- `tests/degradation/01_provider_failure_and_recovery.md`
- `tests/degradation/expectations/01_provider_failure_and_recovery.md`
- `tests/degradation/README.md`
- `demo/DEGRADATION_FAILURE_INJECTION_PROMPT.md`

The fault injection happens outside DomainModules and must not enter canonical Kitchen data.

## Provider/store shape remains unchanged

No new physical storage schema has been added. Google Drive still uses exactly:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

Do not add a degradation table, retry table, vector database, or another provider just to satisfy the reliability test.

## Next after reliability gate

If degradation/failure injection passes, proceed to durable Event/Experience compaction and long-history validation:

- increase cold Event history substantially;
- keep normal ContextPack bounded;
- derive/retrieve only compact reusable Experience evidence;
- verify history growth does not cause proportional model-context growth.

Only after that should provider breadth (Notion, Tencent Docs, Codex/local storage, etc.) become a major implementation target.

## Architecture docs

- `docs/Kitchen_System_v0.4_Frozen_Architecture.md` — untouched rollback baseline.
- `docs/Kitchen_System_v0.5_Interface_and_Schema_Draft.md` — current formal interface/schema architecture.

The v0.7 label remains an implementation milestone, not a replacement architecture document.
