# Notion Plugin Capability Probe

This suite measures the actual capabilities exposed by two independently installed Notion integrations: one on Web and one in Codex.

It intentionally runs **before** any Notion StorageProvider implementation or Web/App/Codex synchronization test.

## Why

The Notion brand name is not a sufficient interface contract. Different plugin/app versions may expose different read/write actions, permissions, object models, and legacy sync/search-only behavior.

The provider design must therefore come from the intersection of operations proven on both target surfaces.

## Required order

1. Run `demo/NOTION_WEB_CAPABILITY_PROMPT.md` in the Web surface with the intended Web Notion integration explicitly selected.
2. Run `demo/NOTION_CODEX_CAPABILITY_PROMPT.md` in Codex with the intended Codex Notion plugin explicitly selected.
3. Record both reports in GitHub Issue #9 or return them to the development session unchanged.
4. Only after both reports exist, derive the Notion provider mapping and decide whether a pre-provisioned Notion template is required.
5. Only after provider-interface alignment, design the App/Web ↔ Codex shared-Notion synchronization gate.

## Important distinctions

- Read/search-only Notion access is insufficient for Kitchen durable state.
- Lack of autonomous database/data-source creation is not automatically fatal if all P0 record operations work against a pre-provisioned template; classify that as `template_bootstrap_required`.
- Lack of true transactions is allowed as `transactional_write=false`, but a future provider must then implement and test partial-write detection/recovery before production use.
- A local Codex file, SQLite database, exported Markdown, or copied JSON is never evidence of shared Notion durability.

The exact capability matrix and scratch payloads are in `tests/notion/capability_matrix.yaml`.
