# Storage Provider — Google Drive v1

## Scope

This is the first durable `StorageProvider` implementation profile for Kitchen Skill.

Physical representation: **one native Google Sheet stored in Google Drive**.

This file is provider-specific by design. Domain modules must never depend on its Sheet names, columns, API operations, or file IDs.

## Capabilities

```yaml
durable_read: true
durable_write: true
partial_update: true
append: true
structured_query: true      # limited to provider row/range filtering
text_search: true           # limited provider search, not semantic retrieval
shared_remote: true
transactional_write: true   # one spreadsheet batch; no multi-client CAS guarantee
```

`shared_remote=true` means sequential cross-client continuity is possible when each client can access the same Drive file.

Concurrent conflicting writes remain out of v1 scope.

## Store identity and discovery

Preferred file title:

`Kitchen Skill Store`

The title is not the canonical identity. A compatible store must also contain the `META` marker:

`store_format = kitchen-skill-google-sheets-v1`

Resolution order:

1. use an explicitly configured/pinned Drive file ID or URL when available;
2. otherwise search Drive for the preferred title;
3. verify candidates by reading only the small `META` projection;
4. if exactly one compatible store exists, use it;
5. if several compatible stores exist, do not guess from recency alone; keep the current task usable in session context and ask for one disambiguation only when persistence continuity materially depends on it.

If the user explicitly selected/enabled the Google Drive deployment and no compatible store exists, initialize one store without asking them to design tables or schemas. Do not interrupt an urgent live-cooking action merely to finish setup.

## Physical layout

Canonical records are stored as JSON payloads. Small projection columns support bounded reads/search and are provider implementation details.

### `META`

Exactly one data row.

Columns:

```text
store_format | store_id | schema_version | global_revision | active_task_id |
last_activity_at | health_status | payload_json
```

`payload_json` contains the canonical `Meta` object. Projection cells are updated in the same commit.

### `STATE`

One row per KitchenState child record plus one root metadata row.

Columns:

```text
domain | id | revision | updated_at | lookup_keys | payload_json
```

Allowed `domain` values in this slice:

- `_root` — `id=kitchen_state`; payload contains KitchenState `RecordMeta` only;
- `inventory`;
- `equipment`;
- `preferences`;
- `plans` (supported physically but not required by the cooking slice).

`lookup_keys` is derived/rebuildable and never canonical truth.

### `ACTIVE_TASK`

At most one current task data row.

Columns:

```text
id | type | status | revision | updated_at | goal | phase | lookup_keys | payload_json
```

`payload_json` contains the canonical `ActiveTask`. Projection cells are updated atomically with it.

Completed/cancelled operational task history belongs in Events/Experience where useful; this tab is not a task-history log.

### `EXPERIENCES`

One row per compact reusable Experience.

Columns:

```text
id | key | kind | status | confidence | evidence_count |
last_observed_at | tags | lookup_keys | payload_json
```

Experience retrieval must be limited. Normal Live Cooking uses at most 1–2 relevant rows.

### `EVENTS`

Append-only rows.

Columns:

```text
id | type | occurred_at | task_id | entity_keys | payload_json
```

Events are cold data. Normal Live Cooking does not scan this tab.

## Initialization

Create one native spreadsheet and ensure the five tabs above exist with header rows.

Initialize `META` with:

```yaml
store_format: kitchen-skill-google-sheets-v1
schema_version: 0.6-drive-slice-1
global_revision: 1
active_task_id: null
health_status: healthy
```

Generate a stable `store_id`. Never store OAuth tokens, passwords, connector credentials, or unrelated assistant memory in the Kitchen store.

## Read mapping

### Meta

Read only `META` header + single data row.

### ActiveTask

Read only the one `ACTIVE_TASK` data row when `META.active_task_id` is present.

### State

Resolve by `(domain, id)` whenever IDs are known.

When the current message provides only a name, a bounded row search over `STATE.lookup_keys`/payload may be used. Do not read all state into model context.

### Experience

Search by `key`, tags, entity/name terms, or `lookup_keys`, then return only the requested limit.

### Events

Only read for explicit debugging/repair/audit policies. Default retrieval policy is none.

## Search mapping

Provider search is a candidate-selection mechanism, not semantic truth.

Search results must retain stable canonical IDs. When a candidate will affect the decision, read its full `payload_json` before reasoning from it.

## Commit mapping

PersistenceCoordinator supplies a normalized `StorageMutationBatch`.

Provider commit should:

1. resolve target row numbers from stable IDs/keys;
2. build one spreadsheet batch when practical;
3. upsert affected STATE/EXPERIENCE rows;
4. replace or clear the single ACTIVE_TASK row as requested;
5. append Event rows rather than rewriting old Events;
6. update root KitchenState metadata when KitchenState changes;
7. update canonical Meta payload + projections, including `global_revision = previous + 1` and `last_activity_at`;
8. return a write receipt only after the provider reports batch success.

A provider must not reinterpret semantic operations such as `subtract` in a way that upgrades uncertainty. PersistenceCoordinator resolves amount semantics before physical write.

## Sequential revision discipline

v1 assumes sequential clients, but revisions still protect against stale overwrites.

Before commit, PersistenceCoordinator should compare its expected/global revision with current `META.global_revision` when available.

If a mismatch is detected:

- do not force-write stale state;
- refresh the minimum affected records;
- re-evaluate the semantic change or defer it;
- preserve the current user observation as highest-priority evidence.

This is stale-write protection, not full concurrent conflict resolution.

## Health

Provider health should detect at least:

- file inaccessible;
- missing required tab/header;
- invalid `store_format`;
- unsupported schema version;
- unreadable META row;
- ACTIVE_TASK id mismatch between META and the task row;
- failed write batch.

Health does not repair semantic records directly. Repairs flow through `HealthEngine -> RepairPlan -> PersistenceCoordinator`.

## Current Web-host primitive mapping

The current ChatGPT Drive connector exposes the primitives needed by this profile:

- Drive metadata search for store discovery;
- native spreadsheet creation;
- spreadsheet metadata reads;
- bounded range/cell reads;
- bounded row search;
- spreadsheet batch updates for cell updates, sheet creation, and append-style row operations.

These connector action names are runtime/provider implementation details. Other hosts may map the same logical provider contract to different APIs.
