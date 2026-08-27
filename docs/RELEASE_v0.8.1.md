# Kitchen Skill v0.8.1 — Validated Release Record

Status: validated release baseline

## Product baseline

- Product-bearing baseline: `a0a8979e412ab254eb9095b9d5ccf21747bc8c63`
- Current-HEAD composite tested commit: `d3c1fac7ea4de7e3d83dd198ce9799d82ed7c81b`
- Release gate: GitHub Issue #7
- Frozen PASS result comment: `5441221465`
- Cleanup receipt: `5441226472`
- Static validation run for tested commit: `33083694868` — success

The commits after the product-bearing v0.8 baseline and through the release freeze are release/docs/CI/harness-only. No Cooking, Shopping, runtime, provider, retrieval, persistence, health, canonical schema, Google Drive store schema, or v0.8 product bundle behavior was changed by release hardening.

## Validated release scope

This release carries forward the validated v0.5–v0.8 behavior and adds a current-HEAD composite release proof for:

- Shopping quantity-fit reasoning and canonical purchase capture;
- fresh-session Cooking retrieval from canonical STATE rather than transcript/Event replay;
- exact 500 g minus approximate 120 g becoming approximate ~380 g;
- canonical persisted Cooking ActiveTask shape (`state`, `completed`, `next` boundaries);
- real failed provider write against a deleted Google Sheet;
- no false durable-success claim;
- session-pending semantic change retention;
- no valid-store revision advance or partial mutation on failed write;
- bounded refresh and retry through PersistenceCoordinator → StorageProvider;
- revision advancing exactly once on successful retry;
- zero normal EVENTS/history reads during the composite candidate path.

Pure Web v0.5 and v0.8 long-history evidence are inherited only through the exact Git blob guards recorded in `tests/VALIDATION_REGISTRY.yaml`.

## Deployment identities

- Pure Web fallback: `SKILL.md` / `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`
- Validated Web + Google Drive deployment: `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`

The root `SKILL.md` intentionally remains the Pure Web fallback.

## Explicitly not included

- Codex runtime composition / Web ↔ Codex portability
- local SQLite/files provider
- second shared remote provider
- concurrent writer conflict resolution
- independent Inventory / Planning / Equipment / Recipe DomainModules
- durable Recipe provider mapping/schema migration
- background compaction scheduler

## Next recommended experiment

Validate Web ↔ Codex sequential portability against the same shared Google Drive Kitchen store without changing the StorageProvider contract or introducing concurrency semantics.
