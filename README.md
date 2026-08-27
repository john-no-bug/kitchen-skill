# Kitchen Skill — v0.8.1 Validated Release Baseline

Status: validated release baseline  
Frozen architecture baseline: `docs/Kitchen_System_v0.4_Frozen_Architecture.md` + `docs/Kitchen_System_v0.5_Interface_and_Schema_Draft.md`

## Project state

The product-bearing v0.8 baseline is commit `a0a8979e412ab254eb9095b9d5ccf21747bc8c63`.

The current-HEAD composite release gate was tested at `d3c1fac7ea4de7e3d83dd198ce9799d82ed7c81b` and passed GitHub Issue #7. Release-freeze commits after that tested commit are metadata/docs/CI-only and inherit product evidence only while the validation-registry blob guards remain exact and static validation stays green.

Validated gates:

- v0.5 Pure Web Live Cooking — Issue #1 — 3 × 36/36 PASS.
- v0.6 Web + Google Drive fresh-session persistence — Issue #2 — PASS.
- v0.7 Shopping → canonical KitchenState → fresh Cooking — Issue #3 — PASS.
- provider degradation / failed-write pending retry — Issue #5 — PASS with real Google Sheets 404 failures.
- v0.8 Event → Experience compaction + long-history bounded context — Issue #6 — PASS with 2000 Events + 122 Experiences.
- v0.8.1 current-HEAD composite release gate — Issue #7 — PASS with canonical ActiveTask shape validation, real failed-write 404, pending retry, cleanup verification, and zero normal Event-history reads.

Release evidence is recorded in `docs/RELEASE_v0.8.1.md` and `tests/VALIDATION_REGISTRY.yaml`.

## What is implemented

### Domain modules

- Cooking
- Shopping

### Runtime modes

- Web context-only / ephemeral
- Web + durable provider

### Durable provider

- Google Drive / native Google Sheets

### Stable durable store

Exactly five tabs remain authoritative:

- `META`
- `STATE`
- `ACTIVE_TASK`
- `EXPERIENCES`
- `EVENTS`

No vector database, retry table, Shopping table, archive table, or compaction table is required.

## Validated architecture claims

The following are evidence-backed rather than merely designed:

- Runtime and Storage are separate.
- DomainModules do not write providers directly.
- PersistenceCoordinator is the semantic write gate.
- persisted ActiveTask uses the canonical top-level shape; module-specific facts live under `state`, with canonical `completed` / `next` task-step lists.
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

See `docs/Kitchen_System_v0.8_Validated_Baseline.md`, `docs/RELEASE_v0.8.1.md`, and `tests/VALIDATION_REGISTRY.yaml`.

## Deployment entrypoints

Machine-readable deployment metadata lives in `dist/deployments.yaml`.

Validated entrypoints:

- Pure Web fallback: `SKILL.md` / `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`
- Web + Google Drive validated deployment: `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`

The root `SKILL.md` intentionally remains the validated Pure Web fallback rather than silently becoming a durable-provider bundle.

## Release discipline

v0.8.1 adds release discipline around the validated product:

- `tests/VALIDATION_REGISTRY.yaml` — machine-readable validation evidence and blob guards.
- `dist/deployments.yaml` — explicit deployment identities.
- `scripts/validate_repo.py` — deterministic repository invariant checks.
- `.github/workflows/static-validation.yml` — static validation on push/PR.
- `tests/release/*` — current-HEAD composite release gate, including canonical ActiveTask shape validation.
- `demo/RELEASE_SESSION_A_PROMPT.md` / `demo/RELEASE_SESSION_B_PROMPT.md` — real two-session release regression harness.

A historical result is inherited only when its declared Git blob guards still match. A product-bearing change to a guarded file invalidates that inherited evidence until the relevant gate is rerun.

## v0.8.1 release proof

Issue #7 composite path validated:

`Shopping purchase`
→ `canonical exact 500 g inventory`
→ fresh `Cooking` retrieval from STATE
→ canonical Cooking ActiveTask persistence
→ approximate consumption (`500 exact - ~120 = ~380 approximate`)
→ newest Cooking observation
→ real failed provider write against a deleted sacrificial Sheet
→ no false durable success + pending semantic state retained
→ no valid-store revision advance / partial mutation
→ bounded retry against restored valid store
→ revision `5 → 6` exactly once and newest canonical task state persists.

The successful composite run used tested commit `d3c1fac7ea4de7e3d83dd198ce9799d82ed7c81b`, frozen PASS result comment `5441221465`, cleanup comment `5441226472`, and static-validation run `33083694868`.

## Not implemented yet

Do not confuse canonical-schema coverage with implemented product modules.

Not yet implemented/validated as independent DomainModules:

- Inventory
- Planning
- Recipe
- Equipment

Not yet validated:

- Codex/local runtime composition
- Web ↔ Codex shared-store portability
- second shared remote provider
- concurrent multi-client write conflict resolution

Sequential clients remain the v1 assumption.

## Next after v0.8.1

Preferred next architecture/product experiment:

1. Web ↔ Codex sequential portability through the same shared Google Drive store;
2. then an Inventory DomainModule using the existing `STATE.inventory` contract;
3. then Planning using `STATE.plans`;
4. defer Recipe durable-schema expansion and second-provider work until the release baseline remains stable.

Do not add a vector database without a demonstrated retrieval failure.
