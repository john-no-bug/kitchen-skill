# Kitchen Skill — Codex Notion Capability Probe

Run this in the **Codex surface** where the Notion plugin/app version you actually intend to use is installed. In Sources / Use plugins (or the equivalent control), explicitly select that intended Notion integration.

This is a Notion-plugin capability test, not a local-storage or coding test.

## Ground rules

1. Read `tests/notion/capability_matrix.yaml` from `john-no-bug/kitchen-skill` at current `main`.
2. Test only the selected Codex Notion plugin/app and its actual exposed actions.
3. Codex filesystem, worktree, shell, Python, SQLite, local JSON/YAML/Markdown, repository files, direct Notion REST calls/curl, browser automation, or another MCP/app are **not substitutes** for a missing Notion plugin action.
4. You may use local/code capabilities only to inspect the Kitchen test specification or format the final report; they must not serve as persistence evidence.
5. Do not infer support from the public Notion API or plugin label.
6. Do not expose OAuth tokens, workspace secrets, account IDs, or credentials.
7. Use scratch Notion content only.

## Step C0 — identify the actual integration and runtime

Before mutation, record:

- surface/runtime = Codex;
- evidence that this is a Codex task/conversation surface, not ordinary Web Chat;
- selected plugin/app display name;
- visible version/build/manifest/developer identity if exposed;
- connection/auth state;
- actual real-time Notion actions exposed;
- whether access is read/search-only or includes mutation actions.

If the intended Notion integration is not exposed here, stop with `plugin_not_exposed`.

## Step C1 — create isolated scratch structured collection

Attempt to create:

`Kitchen Skill Notion Capability Probe CODEX <short-random-suffix>`

with minimum logical properties:

- `Name` — title
- `ks_key` — text
- `collection` — text or select
- `revision` — number
- `payload_json` — text/rich text

Optional: `lookup_keys`, `status`.

Record returned database/data-source/page/container IDs and inspect property schema if possible.

If the selected Codex plugin cannot create/configure a structured collection, report that accurately. Continue P0 only if an explicitly disposable, writable structured probe target is already available; otherwise stop after the bootstrap finding.

## Step C2 — create/read META-style row

Create the matrix `meta` row via the selected Notion integration and read it back. Record stable object/page ID plus last-edited/version metadata if exposed.

## Step C3 — create/read STATE-style row

Create the matrix `state_initial` row with exact 500 g payload and read it back.

## Step C4 — exact bounded structured query

Use the Notion plugin's structured property query/filter to request:

`ks_key == inventory/ground_beef`

with finite result limit/page size, preferably `1`.

Record exact filter capability, limit/page-size capability, pagination/sort controls, and returned stable record ID.

Full-text/file search is not equivalent to `structured_query`.

## Step C5 — partial update with stable identity

Update the existing STATE row in place:

- revision `1 -> 2`;
- exact 500 g payload -> approximate 380 g payload.

Read it back and verify the object/page ID did not change. Record any new last-edited/version metadata.

## Step C6 — append Event-style row

Create the matrix `event_append` as a new independent row. Verify the STATE row remains at revision 2 and unchanged.

## Step C7 — optional/maintenance operations

Attempt only if exposed by this exact plugin:

- exact title/container resolution;
- text search;
- sort + finite pagination;
- bulk/batch writes;
- conditional/version-aware update;
- transactional multi-record write.

Record unsupported operations without trying to recreate them through shell/API code.

## Step C8 — cleanup

Archive/trash/delete only the scratch objects created by this run, then verify they disappear from normal active exact query/search if possible.

If cleanup is unavailable, report `cleanup_gap` and preserve exact scratch title/object IDs for manual removal.

## Required report

Return:

```yaml
surface: codex
codex_runtime_evidence:
integration_display_name:
visible_version_or_manifest_identity:
connection_auth_result:
actions_observed: []
p0:
  durable_read: supported|unsupported|ambiguous
  durable_write: supported|unsupported|ambiguous
  stable_identity: supported|unsupported|ambiguous
  partial_update: supported|unsupported|ambiguous
  append: supported|unsupported|ambiguous
  structured_query: supported|unsupported|ambiguous
  bounded_query: supported|unsupported|ambiguous
  shared_remote: supported|unsupported|ambiguous
  revision_observability: supported|unsupported|ambiguous
p1:
  bootstrap_collection_create:
  schema_inspection:
  exact_resolution:
  sort_pagination:
  cleanup:
p2:
  text_search:
  bulk_or_batch_write:
  conditional_write:
  transactional_write:
created_ids: []
stable_id_preserved_on_update:
last_edited_or_version_metadata:
local_storage_used_as_evidence: false
exact_errors: []
cleanup_result:
overall_classification: p0_pass|template_bootstrap_required|unusable_as_kitchen_provider|plugin_not_exposed|connection_auth
```

Every `supported` result must be backed by a real action through the selected Codex Notion plugin in this run.

If GitHub Issue #9 commenting is available, append this report there under heading `Codex Notion capability result`; otherwise return it verbatim to the user.
