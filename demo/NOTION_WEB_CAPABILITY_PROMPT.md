# Kitchen Skill — Web Notion Capability Probe

Run this in the **Web Chat surface** where the Notion integration you actually intend to use is installed/connected. Explicitly select or @mention that Notion integration before running the probe.

This is a capability test only. Do not use or modify production Kitchen data.

## Ground rules

1. Read `tests/notion/capability_matrix.yaml` from `john-no-bug/kitchen-skill` at current `main`.
2. Test only the selected Web Notion plugin/app and its actual exposed actions.
3. Do not infer support from general Notion API knowledge or documentation.
4. Do not use browser automation, direct HTTP/curl, local files, copied JSON, another Notion integration, or manual UI edits to make a missing plugin action look supported.
5. Do not expose OAuth tokens, workspace secrets, account IDs, or credentials in the report.
6. Scratch object/page IDs are acceptable evidence because the probe will clean them up.

## Step W0 — identify the actual integration

Before mutating anything, record what the current surface can actually observe:

- surface = Web Chat;
- plugin/app display name;
- visible version/build/manifest/developer identity if exposed;
- whether the app is connected/authenticated;
- whether real-time Notion actions are exposed;
- whether access appears search/read-only or includes mutation actions;
- actual available Notion action names or clear operation descriptions when tool names are not visible.

If the intended Notion integration is not exposed to this conversation, stop with `plugin_not_exposed`.

## Step W1 — create isolated scratch collection

Attempt to create one structured Notion collection/database/data source named:

`Kitchen Skill Notion Capability Probe WEB <short-random-suffix>`

Use the minimum logical properties from the matrix:

- `Name` — title
- `ks_key` — text
- `collection` — text or select
- `revision` — number
- `payload_json` — text/rich text

Optional: `lookup_keys`, `status`.

Record the returned database/data-source/page/container ID(s) and inspect/read back the property schema if possible.

If collection creation/schema configuration is not exposed, do **not** fabricate success. Record `bootstrap_collection_create=unsupported`.

If the plugin can still perform P0 record CRUD/query against an already available scratch structured collection, it may continue using that only if the collection is explicitly a disposable probe target. Classify eventual success as `template_bootstrap_required`.

If no safe writable structured target exists, stop after reporting the bootstrap gap.

## Step W2 — create and read META-style row

Create the matrix `meta` row. Read it back through Notion and record:

- stable page/object ID;
- `ks_key`, `collection`, `revision`, `payload_json`;
- `last_edited_time`, version, or equivalent metadata if exposed.

## Step W3 — create STATE-style row

Create the matrix `state_initial` row with exact 500 g payload. Read it back.

## Step W4 — exact bounded query

Use a structured Notion query/filter—not free-text semantic search—to request:

`ks_key == inventory/ground_beef`

with a finite result limit/page size, preferably `1`.

Record whether the action exposes:

- exact property filter;
- limit/page size;
- sort/pagination controls;
- returned stable record ID.

If only full-text/file search is available, `structured_query` is unsupported even if it happens to find the row.

## Step W5 — partial update, same ID

Update the existing state row **in place** to the matrix `state_updated` representation:

- revision `1 -> 2`;
- payload exact 500 g -> approximate 380 g.

Do not create a replacement row.

Read back the row and verify the Notion object/page ID is unchanged. Record updated last-edited/version metadata if exposed.

## Step W6 — append Event-style row

Create the matrix `event_append` row as a separate new record. Verify the state row still exists unchanged at revision 2.

This proves append can coexist with current-state update.

## Step W7 — search/resolution and optional controls

Attempt, when the selected plugin exposes them:

- exact title/container lookup;
- text search;
- finite sorted query;
- pagination/cursor retrieval;
- bulk/batch write;
- conditional/version-aware update;
- transactional multi-record write.

Unsupported P2 operations are not failures. Report them accurately.

## Step W8 — cleanup

Archive/trash/delete only the scratch records/container created by this probe. Verify they are no longer returned by the normal active exact query/search path when the plugin allows verification.

If cleanup action is missing, report `cleanup_gap` and leave the exact scratch object title/ID so the user can remove it manually later; do not delete unrelated content.

## Required report

Produce one compact report with:

```yaml
surface: web
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
exact_errors: []
cleanup_result:
overall_classification: p0_pass|template_bootstrap_required|unusable_as_kitchen_provider|plugin_not_exposed|connection_auth
```

Base every `supported` value on an actual successful Notion action in this run.

If GitHub Issue #9 commenting is available, append this report there under heading `Web Notion capability result`; otherwise return it verbatim to the user for the development session.
