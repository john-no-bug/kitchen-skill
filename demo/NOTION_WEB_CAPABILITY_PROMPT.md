# Kitchen Skill — Web Notion Capability Probe

Run this in the **Web Chat surface** where the Notion integration you actually intend to use is installed/connected. Explicitly select or @mention that Notion integration before running the probe.

This is a capability test only. Do not use or modify production Kitchen data.

## Public specification loading

A GitHub connector is **not required**.

Read the probe matrix using ordinary public web/HTTP access from:

`https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/tests/notion/capability_matrix.yaml`

Rendered fallback:

`https://github.com/john-no-bug/kitchen-skill/blob/main/tests/notion/capability_matrix.yaml`

If this runtime cannot read the public specification through ordinary web access, ask the user to paste/upload the matrix. Do not ask them to connect GitHub.

## Ground rules

1. Test only the selected Web Notion plugin/app and its actual exposed actions.
2. Do not infer support from general Notion API knowledge or documentation.
3. Do not use browser automation, direct HTTP/curl, local files, copied JSON, another Notion integration, or manual UI edits to make a missing plugin action look supported.
4. Public GitHub reading is allowed only for loading the test specification; GitHub is not persistence evidence.
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

Record returned database/data-source/page/container IDs and inspect/read back the property schema if possible.

If collection creation/schema configuration is not exposed, record `bootstrap_collection_create=unsupported`. Continue P0 only if an explicitly disposable, writable structured probe target is already available; classify success as `template_bootstrap_required`.

If no safe writable structured target exists, stop after reporting the bootstrap gap.

## Step W2 — create and read META-style row

Create the matrix `meta` row. Read it back through Notion and record stable page/object ID, logical properties, and last-edited/version metadata if exposed.

## Step W3 — create STATE-style row

Create the matrix `state_initial` row with exact 500 g payload. Read it back.

## Step W4 — exact bounded query

Use a structured Notion query/filter—not free-text semantic search—to request:

`ks_key == inventory/ground_beef`

with a finite result limit/page size, preferably `1`.

Record exact property filter, limit/page-size, sort/pagination controls, and returned stable record ID.

If only full-text/file search is available, `structured_query` is unsupported even if it happens to find the row.

## Step W5 — partial update, same ID

Update the existing STATE row **in place** to the matrix `state_updated` representation:

- revision `1 -> 2`;
- payload exact 500 g -> approximate 380 g.

Do not create a replacement row. Read back and verify the Notion object/page ID is unchanged. Record updated last-edited/version metadata if exposed.

## Step W6 — append Event-style row

Create the matrix `event_append` row as a separate new record. Verify the STATE row still exists unchanged at revision 2.

## Step W7 — optional controls

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

Archive/trash/delete only the scratch records/container created by this probe. Verify they are no longer returned by the normal active exact query/search path when possible.

If cleanup action is missing, report `cleanup_gap` and leave the exact scratch object title/ID for manual removal; do not delete unrelated content.

## Required report

Always return one complete report in the conversation:

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

If GitHub Issue #9 commenting happens to be available in this development/test environment, it may additionally append the report there under `Web Notion capability result`. That writeback is optional and must never be required from normal users.
