# Kitchen Skill — v0.5 Pure Web Live Cooking Vertical Slice

Status: regression-testable vertical slice  
Baseline: Kitchen System v0.4 frozen architecture + v0.5 interface/schema draft

## Goal

Validate one narrow hypothesis before durable storage is added:

> Live cooking can remain state-consistent through a long ordinary web-chat session without requiring a database, platform memory, hidden scratchpad, or user-managed checkpoint.

## Implemented

- Pure Web (`WEB_CHAT + CONTEXT_ONLY`)
- Live Cooking
- logical `ActiveTask`
- bounded context selection
- state precedence and correction rules
- lightweight Monitor/Doctor re-anchor
- adversarial regression suite with evaluator-only expectations

Not implemented yet: durable persistence, Google Drive/Tencent Docs/Notion providers, Codex persistence, full inventory, shopping, planning, scheduled checks, or cross-session continuity.

## Repository map

- `SKILL.md` — canonical Pure Web candidate used by tests.
- `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md` — distribution copy.
- `core/kernel.md` — orchestration/invariants.
- `modules/cooking/contract.md` and `logic.md` — domain contract and behavior.
- `runtime/web_ephemeral.md` — Pure Web runtime semantics.
- `retrieval/web_ephemeral.md` — bounded context selection.
- `health/web_ephemeral.md` — Monitor/Doctor re-anchor.
- `schemas/` — minimal schemas for this slice.
- `tests/manifest.yaml` — authoritative automated regression protocol.
- `tests/01_*` ... `tests/04_*` — candidate-visible scripts only.
- `tests/expectations/` — evaluator-only expectations loaded after transcript freeze.
- `tests/EVALUATION_RUBRIC.md` — 18 criteria / 36 points.
- `demo/DEMO_SESSION_PROMPT.md` — single prompt for a fresh session with GitHub access.
- `docs/` — v0.4 rollback baseline and v0.5 interface/schema draft.

## Automated demo

In a fresh session with GitHub access, paste `demo/DEMO_SESSION_PROMPT.md`. It will retrieve the repository and run three suite runs without requiring you to manually send every test turn.

The automated harness is useful for regression testing, but it is not identical to real host-level context truncation. Keep a small number of true multi-turn platform tests before declaring Pure Web production-ready.

## Pass gate

Each suite run evaluates all four scenarios together against the 18-criterion rubric:

- maximum 36;
- pass >= 32;
- no zero on criteria 1, 2, 4, 9, 12, 13, 15, or 16;
- current v0.5 gate requires all 3 suite runs to pass.

Patch failed interface boundaries, not wording differences. Prefer the smallest change that restores the invariant.
