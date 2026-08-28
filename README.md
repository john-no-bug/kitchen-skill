# Kitchen Skill — v0.8.1 Validated Release + Public Bootstrap

Status: validated v0.8.1 product baseline; public-web bootstrap active; Notion Web/Codex capability probe in progress.

Frozen architecture baseline: `docs/Kitchen_System_v0.4_Frozen_Architecture.md` + `docs/Kitchen_System_v0.5_Interface_and_Schema_Draft.md`

## Start without installing a skill or connecting GitHub

Normal users do **not** need a GitHub connector and do not need repository write access.

Use this public bootstrap:

- rendered: `https://github.com/john-no-bug/kitchen-skill/blob/main/SKILL.md`
- raw: `https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/SKILL.md`

A generic startup instruction is:

> Read and follow the public Kitchen Skill bootstrap at https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/SKILL.md using ordinary web/HTTP access. Do not require a GitHub connector. Load only a validated deployment compatible with the capabilities available in this runtime.

Root `SKILL.md` is now intentionally a **small capability/distribution bootstrap**, not a full product bundle. It reads `dist/deployments.yaml`, selects a validated deployment compatible with the current runtime/provider, then loads that public `dist/` artifact.

If public web access is disabled by workspace policy, the final fallback is for the user to paste/upload the selected public bundle. GitHub connection is never required for runtime use.

## Validated product state

The product-bearing v0.8 baseline is commit `a0a8979e412ab254eb9095b9d5ccf21747bc8c63`.

The current-HEAD composite release gate was tested at `d3c1fac7ea4de7e3d83dd198ce9799d82ed7c81b` and passed GitHub Issue #7. Release/distribution commits after that tested commit inherit product evidence only while validation-registry blob guards remain exact and static validation stays green.

Validated gates:

- v0.5 Pure Web Live Cooking — Issue #1 — 3 × 36/36 PASS.
- v0.6 Web + Google Drive fresh-session persistence — Issue #2 — PASS.
- v0.7 Shopping → canonical KitchenState → fresh Cooking — Issue #3 — PASS.
- provider degradation / failed-write pending retry — Issue #5 — PASS with real Google Sheets 404 failures.
- v0.8 Event → Experience compaction + long-history bounded context — Issue #6 — PASS with 2000 Events + 122 Experiences.
- v0.8.1 current-HEAD composite release gate — Issue #7 — PASS with canonical ActiveTask shape validation, real failed-write 404, pending retry, cleanup verification, and zero normal Event-history reads.

Release evidence is recorded in `docs/RELEASE_v0.8.1.md` and `tests/VALIDATION_REGISTRY.yaml`.

## Validated deployment artifacts

Machine-readable deployment metadata lives in `dist/deployments.yaml`.

Current validated artifacts:

- Pure Web fallback: `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`
- Web + Google Drive: `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`

The Pure Web artifact retains validated Git blob `37a8d15bb376579a9a33ede514b121dff04c249d`. Root `SKILL.md` no longer has to equal that blob because it serves the public bootstrap role.

## Implemented product modules

### Domain modules

- Cooking
- Shopping

### Runtime modes already validated

- Web context-only / ephemeral
- Web + durable provider

### Durable provider already validated

- Google Drive / native Google Sheets

### Stable durable Google Drive store

Exactly five tabs remain authoritative:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

No vector database, retry table, Shopping table, archive table, or compaction table is required.

## Validated architecture claims

Evidence-backed claims include:

- Runtime and Storage are separate.
- DomainModules do not write providers directly.
- PersistenceCoordinator is the semantic write gate.
- persisted ActiveTask uses the canonical top-level shape; module-specific facts live under `state`.
- ContextRetriever is read-only and bounded.
- newest direct observation outranks stored/history-derived state.
- unknown is not zero/false/absent.
- approximate evidence does not become exact through arithmetic.
- fresh conversations can resume from shared durable state without transcript replay.
- Shopping and Cooking hand off through canonical KitchenState.
- provider failure does not justify a false durable-success claim; pending semantic change can survive in session and retry after recovery.
- failed writes do not advance the valid-store revision or partially mutate valid state.
- Events remain append-only cold history while reusable knowledge compacts into bounded Experience records.
- history growth does not cause proportional normal ContextPack growth.

## Distribution discipline

GitHub has two distinct roles:

1. **public read transport** — any runtime with ordinary web/HTTP access may read the public bootstrap and bundle files;
2. **development connector** — optional repository mutation, Issue evidence, CI, and release maintenance.

The second role is never an end-user dependency.

Formal test prompts must therefore treat GitHub Issue writeback as optional. If GitHub write access is unavailable, the full test/probe report must be returned in the conversation for later inspection.

## Current experiment — Notion capability/conformance

The former Google Drive Web↔Codex portability experiment was superseded before execution.

Current tracking issue: #9 — `Notion capability gate: Web vs Codex plugin conformance`.

Before implementing a Notion StorageProvider, we separately test the actual Notion plugin/app exposed in Web and the actual Notion plugin/app exposed in Codex. We compare proven operations rather than assuming that two Notion-branded integrations expose the same API.

Probe assets:

- `tests/notion/capability_matrix.yaml`
- `demo/NOTION_WEB_CAPABILITY_PROMPT.md`
- `demo/NOTION_CODEX_CAPABILITY_PROMPT.md`

The probes use public raw GitHub URLs for specification loading and do not require a GitHub connector. Notion provider mapping will be designed only after both capability reports exist.

## Not implemented / not yet validated

Do not confuse canonical-schema coverage with implemented product modules.

Not yet implemented/validated as independent DomainModules:

- Inventory
- Planning
- Recipe
- Equipment

Not yet validated:

- Notion StorageProvider mapping
- Web/App ↔ Codex shared-Notion synchronization
- second shared remote provider in production
- concurrent multi-client write conflict resolution

Sequential clients remain the v1 assumption.

Do not add a vector database without demonstrated retrieval failure evidence.
