# Kitchen System v0.5 — Interface & Canonical Schema Draft

**Status:** Draft built on frozen v0.4 baseline  
**Date:** 2026-08-25  
**Parent rollback point:** `Kitchen_System_v0.4_Frozen_Architecture.md`

This document begins the formal definition stage requested by v0.4. It does **not** modify v0.4. If v0.5 proves inconsistent or over-complex, roll back to v0.4.

---

# 0. Scope

v0.5 formally defines:

## Six stable interfaces

1. `RuntimeAdapter`
2. `StorageProvider`
3. `ContextRetriever`
4. `DomainModule`
5. `PersistenceCoordinator`
6. `HealthEngine`

## Six core data objects

1. `KitchenState`
2. `ActiveTask`
3. `Recipe`
4. `Experience`
5. `Event`
6. `Meta`

It also defines a small set of shared value types needed to keep those interfaces consistent.

These are **logical contracts**. They do not require JSON, SQL, Google Sheets, Notion, or any particular language. Providers map the logical schema to their physical representation.

---

# 1. System invariants

These invariants apply to every runtime and provider.

## I-01 — Runtime is separate from storage

Execution runtime answers **how the agent can execute**.

Storage provider answers **where/how state is persisted**.

Examples:

- Web + Context only
- Web + Google Drive
- Web + Tencent Docs
- Web + Notion
- Codex + SQLite
- Codex + local files
- Codex + Google Drive

All are valid compositions.

## I-02 — Domain logic never writes a provider directly

All semantic writes flow through:

`DomainModule / HealthEngine -> ChangeSet -> PersistenceCoordinator -> StorageProvider`

## I-03 — ContextRetriever is read-only

Retriever may select, rank, summarize, and filter records. It must not mutate canonical state.

## I-04 — Indexes/caches are derived

Indexes may be deleted and rebuilt without losing canonical state.

## I-05 — Current user observation outranks stored state

Evidence order:

1. current user observation;
2. current authoritative ActiveTask state;
3. KitchenState;
4. recent Event;
5. Experience / learned pattern;
6. old conversation.

## I-06 — Unknown is not zero/none

Missing information must not be silently converted to zero, false, empty, expired, or absent.

## I-07 — Precision must not increase without evidence

Approximate inventory cannot become exact merely because arithmetic was performed on it.

Example:

`~500 g - ~120 g` must remain approximate, not `380 g exact`.

## I-08 — Normal retrieval is bounded

History growth must not cause proportional Context Pack growth.

## I-09 — Pure Web remains valid

The system must function when durability is unavailable.

## I-10 — Shared remote providers enable portability

Cross-platform continuity is considered available only when all participating clients can access a compatible shared third-party provider.

Concurrent conflicting writes are out of v1 scope.

---

# 2. Shared types

The six core objects reuse the following small types. These are value types, not new first-class storage collections.

---

## 2.1 `RecordMeta`

Common metadata for persisted records.

```yaml
RecordMeta:
  id: string                 # stable within one Kitchen store
  revision: integer          # monotonically increasing per record when supported
  created_at: timestamp?
  updated_at: timestamp?
  provenance: Provenance?
```

Rules:

- `id` should remain stable even if display names change.
- `revision` supports freshness/debugging and future synchronization; v1 does not require multi-client conflict resolution.
- timestamps use an unambiguous ISO-8601 representation when the physical backend supports it.

---

## 2.2 `Provenance`

```yaml
Provenance:
  source_type: enum
    - user_observation
    - user_statement
    - photo_inference
    - shopping_observation
    - cooking_observation
    - imported_record
    - model_inference
    - system_maintenance
  source_ref: string?        # turn/event/import reference when available
  runtime: string?           # host/runtime identifier, optional
```

Provider credentials or secrets must never be stored here.

---

## 2.3 `Confidence`

```yaml
Confidence:
  level: enum
    - unknown
    - low
    - medium
    - high
    - confirmed
  reason: string?            # short explanation when materially useful
```

`confirmed` means directly confirmed/observed recently; it is not permanent truth.

Confidence and freshness are separate concepts.

---

## 2.4 `Amount`

Supports low-friction inventory precision.

```yaml
Amount:
  mode: enum
    - unknown
    - presence
    - level
    - approximate
    - exact

  present: boolean?          # for presence mode

  level: enum?               # for level mode
    - trace
    - low
    - quarter
    - half
    - high
    - full

  value: number?             # approximate/exact
  unit: string?              # g, kg, ml, item, pack, bottle, tbsp, etc.

  lower_bound: number?       # optional uncertainty range
  upper_bound: number?
```

Rules:

- exactness may degrade but must not be upgraded without evidence;
- arithmetic over approximate values remains approximate;
- presence mode is valid for staples such as salt;
- level mode is valid for oil/sauces when exact measurement is unnecessary.

---

## 2.5 `FreshnessEvidence`

Only facts, not a final safety verdict.

```yaml
FreshnessEvidence:
  purchased_at: timestamp?
  opened_at: timestamp?
  frozen_at: timestamp?
  thawed_at: timestamp?
  use_by: timestamp?
  best_before: timestamp?
  storage_condition: string?
  last_verified_at: timestamp?
```

The system should derive attention/check priority from evidence. It should not infer “safe to eat” from dates alone.

---

## 2.6 `EntityRef`

```yaml
EntityRef:
  kind: enum
    - inventory
    - equipment
    - recipe
    - experience
    - event
    - active_task
    - preference
    - plan
    - generic
  id: string
  label: string?
```

---

## 2.7 `TaskRequest`

Represents one user interaction entering the Kernel.

```yaml
TaskRequest:
  request_id: string
  user_text: string
  received_at: timestamp?
  attachments: list<AttachmentRef>?
  intent_hint: string?
  explicit_mode: string?          # e.g. expert/simple when user explicitly asks
```

`AttachmentRef` is runtime-specific and opaque to domain schemas.

---

# 3. Core object 1 — `KitchenState`

## 3.1 Purpose

Represents the best current understanding of the user's kitchen world.

It contains current operational state, not raw history.

Canonical top-level shape:

```yaml
KitchenState:
  meta: RecordMeta
  inventory: map<string, InventoryItem>
  equipment: map<string, EquipmentItem>
  preferences: map<string, PreferenceRecord>
  plans: map<string, PlanEntry>?
```

`KitchenState` may be physically stored as multiple tables/sheets/pages. The logical object remains one state domain.

---

## 3.2 `InventoryItem`

Minimum valid record:

```yaml
InventoryItem:
  id: string
  name: string
  amount: Amount
```

Extended form:

```yaml
InventoryItem:
  id: string
  name: string
  category: string?
  subtype: string?                 # e.g. ketchup / pasta sauce / tomato paste
  amount: Amount
  location: string?                # fridge/freezer/pantry/etc.
  physical_state: string?          # frozen/chilled/raw/cooked/opened/etc.
  freshness: FreshnessEvidence?
  confidence: Confidence?
  attributes: map<string, scalar>?
  notes: string?
  updated_at: timestamp?
  provenance: Provenance?
```

Rules:

- do not require all optional fields from the user;
- `subtype` should be captured when it materially changes cooking behavior;
- low-confidence photo inference is allowed if marked accordingly;
- volatile items may become stale/uncertain without being deleted.

---

## 3.3 `EquipmentItem`

```yaml
EquipmentItem:
  id: string
  name: string
  type: string?
  capabilities: list<EquipmentCapability>
  constraints: list<string>?
  attributes: map<string, scalar>?
  confidence: Confidence?
  updated_at: timestamp?
  provenance: Provenance?
```

Capability:

```yaml
EquipmentCapability:
  capability: string              # boil, saute, pressure_cook, bake, etc.
  evidence: enum
    - declared
    - inferred
    - observed
  confidence: Confidence?
  notes: string?
```

Observed capabilities outrank inferred capabilities.

---

## 3.4 `PreferenceRecord`

```yaml
PreferenceRecord:
  key: string
  value: scalar | object
  stage: enum
    - observation
    - tentative
    - learned
    - stable
  confidence: Confidence
  evidence_count: integer?
  last_observed_at: timestamp?
  last_verified_at: timestamp?
  scope: string?                  # e.g. pasta_portion, cooking_style, shopping
```

Rules:

- stable preferences require repeated evidence or explicit user statement;
- preferences may decay or be superseded;
- one-time situational facts should not become preferences.

---

## 3.5 `PlanEntry`

Used only for future intent that must survive beyond an ActiveTask.

```yaml
PlanEntry:
  id: string
  kind: string                   # meal, batch_cook, shopping_goal, etc.
  target_time: timestamp?
  recipe_ref: EntityRef?
  description: string?
  status: enum
    - planned
    - active
    - completed
    - cancelled
  attributes: map<string, scalar>?
```

Keep this lightweight. A dedicated planning subsystem is not required in v0.5.

---

# 4. Core object 2 — `ActiveTask`

## 4.1 Purpose

Represents the user's current operational task.

It replaces first-class `CookingSession`, `ShoppingSession`, and `WorkingSnapshot` schemas.

```yaml
ActiveTask:
  meta: RecordMeta
  type: enum
    - cooking
    - shopping
    - planning
    - inventory_refresh
    - other
  status: enum
    - active
    - paused
    - completed
    - cancelled
  goal: string
  phase: string?
  state: object
  completed: list<TaskStepState>?
  next: list<TaskStepState>?
  open_issues: list<OpenIssue>?
  related_recipe: EntityRef?
  started_at: timestamp?
  updated_at: timestamp?
```

`state` is module-specific but must remain compact and operational.

Examples:

### Cooking state

```yaml
state:
  servings: 1
  equipment_refs: [supor_green_pot]
  ingredients:
    beef:
      physical_state: broken_apart
      water_level: high
    onion:
      physical_state: raw
      added: false
```

### Shopping state

```yaml
state:
  goal: "buy ingredients for two planned meals"
  needed:
    beef: "~350 g"
  cart:
    - "500 g ground beef"
  candidates: []
```

---

## 4.2 `TaskStepState`

```yaml
TaskStepState:
  id: string
  label: string
  status: enum
    - pending
    - active
    - done
    - skipped
    - blocked
  depends_on: list<string>?
```

This enables a lightweight dependency graph without a heavyweight workflow engine.

---

## 4.3 `OpenIssue`

```yaml
OpenIssue:
  code: string
  description: string
  severity: enum
    - info
    - attention
    - blocking
    - safety
  resolution_hint: string?
```

---

## 4.4 ActiveTask lifecycle

- created logically when the system infers the user has started an operational task;
- updated only on meaningful state changes;
- completed/cleared when the task ends;
- important results are compacted into KitchenState, Event, and/or Experience;
- old conversational details do not need to remain active.

A `Checkpoint` is simply an authoritative update to ActiveTask; it is not a stored object.

---

# 5. Core object 3 — `Recipe`

## 5.1 Purpose

Represents reusable instructions for making a dish.

It describes **how to make something**, not the user's personal history with it.

```yaml
Recipe:
  meta: RecordMeta
  name: string
  servings: number?
  ingredients: list<IngredientRequirement>
  equipment_requirements: list<EquipmentRequirement>?
  steps: list<RecipeStep>
  tags: list<string>?
  source: RecipeSource?
  notes: string?
```

---

## 5.2 Ingredient requirement

```yaml
IngredientRequirement:
  id: string
  name: string
  role: enum
    - required
    - substitutable
    - optional
  amount: Amount?
  acceptable_subtypes: list<string>?
  alternatives: list<IngredientAlternative>?
```

This replaces the overly strict rule “every listed ingredient must exist.”

All required ingredients must be available or deliberately substituted before a recipe is considered fully feasible.

---

## 5.3 Ingredient alternative

```yaml
IngredientAlternative:
  name: string
  conditions: string?
  adjustment: string?
```

---

## 5.4 Equipment requirement

Prefer capabilities over model names.

```yaml
EquipmentRequirement:
  capability: string
  required: boolean
  constraints: list<string>?
```

Example:

```yaml
- capability: boil
  required: true
- capability: saute
  required: true
```

---

## 5.5 Recipe step

```yaml
RecipeStep:
  id: string
  instruction: string
  depends_on: list<string>?
  completion_condition: string?
  safety_notes: string?
```

Recipes may be DAG-like through `depends_on`; numbering is only presentation.

---

## 5.6 Recipe source

```yaml
RecipeSource:
  type: enum
    - user
    - model_generated
    - imported
    - external
  ref: string?
```

Personal adaptations learned from use should normally live in `Experience`, not by silently mutating the base Recipe.

---

# 6. Core object 4 — `Experience`

## 6.1 Purpose

Stores compact reusable knowledge learned from history.

It is the main mechanism preventing raw history from flooding future context.

```yaml
Experience:
  meta: RecordMeta
  key: string                     # stable dedupe/merge key
  kind: enum
    - recipe_adaptation
    - technique
    - equipment_capability
    - portion_pattern
    - shopping_pattern
    - ingredient_behavior
    - other
  subject_refs: list<EntityRef>?
  summary: string
  conditions: object?
  learned_value: scalar | object?
  confidence: Confidence
  evidence_count: integer
  first_observed_at: timestamp?
  last_observed_at: timestamp?
  status: enum
    - tentative
    - active
    - superseded
    - retired
  tags: list<string>?
  evidence_event_refs: list<string>?
```

Rules:

- Experience should be compact enough to retrieve frequently;
- repeated raw Events should merge into one Experience where appropriate;
- experiences may be superseded rather than duplicated;
- a mature stable personal preference may be promoted into `KitchenState.preferences` while the supporting Experience remains optional/history-facing;
- Experience is not an index and must survive index rebuilds.

Example:

```yaml
key: "frozen_ground_beef:supor_green_pot"
kind: recipe_adaptation
summary: "Frozen ground beef can be softened with a little water, broken apart, then excess water evaporated before browning."
confidence:
  level: high
evidence_count: 3
```

---

# 7. Core object 5 — `Event`

## 7.1 Purpose

Immutable observation of something that happened.

Events support traceability, compaction, repair, and future analytics. They are normally cold data.

```yaml
Event:
  meta: RecordMeta
  type: string
  occurred_at: timestamp?
  recorded_at: timestamp?
  task_ref: EntityRef?
  entity_refs: list<EntityRef>?
  payload: object
  state_effects: list<StateEffect>?
  confidence: Confidence?
```

Events are append-only once committed, except for maintenance metadata when the backend requires it.

---

## 7.2 `StateEffect`

Optional normalized effect useful for audit/reconstruction.

```yaml
StateEffect:
  target: EntityRef
  operation: enum
    - add
    - subtract
    - set
    - clear
    - move
    - observe
  value: scalar | object?
```

Example:

```yaml
Event:
  type: consume_inventory
  entity_refs:
    - {kind: inventory, id: ground_beef}
  payload:
    reason: "tomato beef pasta"
  state_effects:
    - target: {kind: inventory, id: ground_beef}
      operation: subtract
      value:
        mode: approximate
        value: 120
        unit: g
```

Pure Web may not durably retain Events. This does not invalidate the contract; the provider advertises its durability capability.

---

# 8. Core object 6 — `Meta`

## 8.1 Purpose

Small store-level metadata used for versioning, health, continuity, and maintenance.

It must remain small and must not become a dumping ground for kitchen facts.

```yaml
Meta:
  record: RecordMeta
  system_version: string
  schema_version: string
  global_revision: integer?
  active_task_id: string?
  created_at: timestamp?
  last_activity_at: timestamp?
  last_health_check_at: timestamp?
  last_compaction_at: timestamp?
  last_inventory_refresh_at: timestamp?
  index_revision: integer?
  health_flags: list<HealthFlag>?
  feature_flags: map<string, boolean>?
```

Do not store:

- OAuth tokens;
- passwords;
- provider credentials;
- full inventory;
- full event summaries;
- model conversation history.

---

## 8.2 `HealthFlag`

```yaml
HealthFlag:
  code: string
  severity: enum
    - info
    - attention
    - degraded
    - critical
  created_at: timestamp?
  scope_ref: EntityRef?
  summary: string
```

`health_flags` are current health status, not a replacement for Event history.

---

# 9. Common mutation contract — `ChangeSet`

`ChangeSet` is the common write intent produced by DomainModule or HealthEngine and consumed by PersistenceCoordinator.

```yaml
ChangeSet:
  change_id: string
  reason: string?
  base_global_revision: integer?

  state_ops: list<PatchOperation>?
  active_task_ops: list<PatchOperation>?
  recipe_ops: list<PatchOperation>?
  experience_ops: list<PatchOperation>?
  meta_ops: list<PatchOperation>?
  event_appends: list<Event>?

  durability_preference: enum?
    - best_effort
    - session_ok
    - durable_preferred
    - durable_required
```

---

## 9.1 `PatchOperation`

Logical patch operation:

```yaml
PatchOperation:
  op: enum
    - set
    - merge
    - add
    - subtract
    - remove
    - clear
    - upsert
  path: string
  value: scalar | object?
  confidence: Confidence?
  provenance: Provenance?
```

Rules:

- providers map logical paths to their physical representation;
- `subtract` must preserve uncertainty semantics;
- semantic validation occurs in PersistenceCoordinator before provider commit.

---

# 10. Interface 1 — `RuntimeAdapter`

## 10.1 Responsibility

Describe current execution capabilities and host constraints.

It does not persist Kitchen data and does not implement cooking logic.

---

## 10.2 Contract

```text
RuntimeAdapter.capabilities() -> RuntimeCapabilities
RuntimeAdapter.resolve_attachment(ref) -> RuntimeAttachment?      [optional]
RuntimeAdapter.runtime_id() -> string
```

### `RuntimeCapabilities`

```yaml
RuntimeCapabilities:
  conversation_context: boolean
  vision: boolean
  dynamic_module_loading: boolean
  filesystem: boolean
  code_execution: boolean
  external_connectors: boolean
  scheduler: boolean
  background_tasks: boolean
  context_budget_hint: integer?
```

Rules:

- capability detection should be based on current runtime, not plan labels such as Free/Plus;
- provider access is discovered separately;
- `context_budget_hint` is advisory only.

---

# 11. Interface 2 — `StorageProvider`

## 11.1 Responsibility

Provide business-agnostic access to canonical records.

Only `ContextRetriever` should normally read through it; only `PersistenceCoordinator` should normally write through it.

---

## 11.2 Capabilities

```yaml
StorageCapabilities:
  durable_read: boolean
  durable_write: boolean
  partial_update: boolean
  append: boolean
  structured_query: boolean
  text_search: boolean
  shared_remote: boolean
  transactional_write: boolean
```

`shared_remote=true` is the v1 signal that the backend may support sequential cross-platform continuity.

---

## 11.3 Contract

```text
StorageProvider.capabilities() -> StorageCapabilities
StorageProvider.read(ReadRequest) -> ReadResult
StorageProvider.search(SearchRequest) -> SearchResult
StorageProvider.commit(StorageMutationBatch) -> StorageWriteReceipt
StorageProvider.health() -> StorageHealth
```

A provider may implement `search` as filtered scanning when no native index exists.

---

## 11.4 `ReadRequest`

```yaml
ReadRequest:
  collection: enum
    - meta
    - state
    - active_task
    - recipes
    - experiences
    - events
  ids: list<string>?
  paths: list<string>?
  filters: object?
  limit: integer?
  order: object?
```

---

## 11.5 `SearchRequest`

```yaml
SearchRequest:
  collections: list<string>
  query_text: string?
  entity_refs: list<EntityRef>?
  tags: list<string>?
  filters: object?
  limit: integer
```

Search results must retain canonical IDs so the exact records can be read if needed.

---

## 11.6 `StorageMutationBatch`

This is an implementation-facing normalized batch created by PersistenceCoordinator.

```yaml
StorageMutationBatch:
  batch_id: string
  expected_global_revision: integer?
  mutations: list<StorageMutation>
  event_appends: list<Event>?
  metadata: object?
```

Provider-specific APIs must not leak back into DomainModule.

---

## 11.7 Context-only provider behavior

`ContextStateProvider` conforms logically but advertises:

```yaml
durable_read: false
durable_write: false
shared_remote: false
```

Its “commit” means establishing a new session-level authoritative state representation when possible. It must never report durable success.

---

# 12. Interface 3 — `ContextRetriever`

## 12.1 Responsibility

Produce a bounded, task-relevant Context Pack.

It is read-only.

The Retriever is a **context-selection protocol**, not necessarily a vector database.

---

## 12.2 Why two retrieval phases exist

Routing sometimes depends on knowing whether there is an ActiveTask.

Example:

User says: “洋葱什么时候加？”

Without task context this is generic recipe advice; with an active cooking task it is Live Cooking.

To keep Kernel from directly reading storage, Retriever provides a small routing bootstrap.

---

## 12.3 Contract

```text
ContextRetriever.bootstrap(TaskRequest, BootstrapBudget) -> RoutingContext
ContextRetriever.retrieve(TaskRequest, RetrievalSpec, RetrievalBudget) -> ContextPack
```

---

## 12.4 `RoutingContext`

Must remain tiny.

```yaml
RoutingContext:
  active_task:
    id: string?
    type: string?
    phase: string?
    goal: string?
  meta:
    last_activity_at: timestamp?
    health_flags: list<HealthFlag>?
  continuity_confidence: Confidence?
```

No full inventory or event history should be loaded here.

---

## 12.5 `RetrievalSpec`

Produced by the selected DomainModule.

```yaml
RetrievalSpec:
  state_domains: list<string>?       # inventory/equipment/preferences/plans
  entity_queries: list<EntityQuery>?
  include_active_task: boolean
  recipe_queries: list<string>?
  experience_queries: list<string>?
  event_policy: enum
    - none
    - recent_relevant
    - explicit_only
  include_due_checks: boolean
  include_conflicts: boolean
```

Default event policy is `none`.

---

## 12.6 `ContextPack`

```yaml
ContextPack:
  request_id: string
  route_context: RoutingContext
  active_task: ActiveTask?

  state:
    inventory: list<InventoryItem>?
    equipment: list<EquipmentItem>?
    preferences: list<PreferenceRecord>?
    plans: list<PlanEntry>?

  recipes: list<Recipe>?
  experiences: list<Experience>?
  events: list<Event>?

  due_checks: list<DueCheck>?
  conflicts: list<ContextConflict>?
  confidence: Confidence?
  retrieval_diagnostics: RetrievalDiagnostics?
```

---

## 12.7 Context budgets

```yaml
BootstrapBudget:
  target_tokens: integer
  hard_max_tokens: integer

RetrievalBudget:
  target_tokens: integer
  hard_max_tokens: integer
  max_experiences: integer?
  max_events: integer?
  max_recipes: integer?
```

Rules:

- hard max must be respected;
- low-priority records are dropped before high-priority current state;
- old conversation text is never loaded merely because token space is available;
- recent user observations can override retrieved stale records.

---

## 12.8 Due checks

```yaml
DueCheck:
  code: string
  target_ref: EntityRef?
  reason: string
  urgency: enum
    - opportunistic
    - soon
    - blocking
  suggested_prompt: string?
```

DueCheck is a transient retrieval result, not a required stored ReminderQueue item.

---

# 13. Interface 4 — `DomainModule`

## 13.1 Responsibility

Implement kitchen-domain reasoning and user interaction for one area such as cooking, shopping, inventory, recipe, planning, or equipment.

Modules do not know the physical provider.

---

## 13.2 Contract

```text
DomainModule.module_id() -> string
DomainModule.supported_intents() -> list<string>
DomainModule.context_requirements(TaskRequest, RoutingContext) -> RetrievalSpec
DomainModule.handle(TaskRequest, ContextPack) -> ModuleResult
```

Kernel selects the module using the current message plus RoutingContext.

---

## 13.3 `ModuleResult`

```yaml
ModuleResult:
  response: string
  changes: ChangeSet?
  health_signals: list<HealthSignal>?
  completion:
    task_completed: boolean?
    task_paused: boolean?
  confidence: Confidence?
```

`response` should be user-facing and should not expose internal architecture unless the user asks.

---

## 13.4 Domain module rules

### Cooking

- prioritize safety and current physical state;
- Live Cooking normally gives current + next 1–2 actions;
- adapt Recipe through Equipment + Experience + user observation;
- use `ActiveTask(type=cooking)` for current operational state.

### Shopping

- support shopping list planning and in-store comparison;
- consider quantity fit, recipe fit, storage, freshness, value, waste risk, preference;
- treat “bought” observations as candidate inventory updates.

### Inventory

- accept low-precision records;
- ask only decision-changing questions;
- support natural refresh checks.

### Recipe

- distinguish required/substitutable/optional ingredients;
- enforce equipment capability constraints;
- prefer proven/personalized experience when relevant.

### Planning

- combine future plans with current inventory and expected consumption;
- avoid over-reserving inventory without user intent.

### Equipment

- learn declared/inferred/observed capabilities;
- observed capability outranks inferred capability.

---

# 14. Interface 5 — `PersistenceCoordinator`

## 14.1 Responsibility

Convert semantic ChangeSets into safe canonical writes and delegate them to the selected StorageProvider.

It is the only normal write orchestration layer.

---

## 14.2 Contract

```text
PersistenceCoordinator.validate(ChangeSet, PersistenceContext) -> ValidationResult
PersistenceCoordinator.commit(ChangeSet, PersistenceContext) -> CommitResult
PersistenceCoordinator.apply_repair(RepairPlan, PersistenceContext) -> CommitResult
```

---

## 14.3 `PersistenceContext`

```yaml
PersistenceContext:
  runtime_id: string
  storage_capabilities: StorageCapabilities
  current_global_revision: integer?
  request_id: string?
  active_task_id: string?
```

---

## 14.4 Validation responsibilities

PersistenceCoordinator must enforce:

- schema validity;
- unit/amount semantics;
- approximate values remain approximate;
- references are valid when required;
- immutable Event rules;
- current user observation is not overwritten by older lower-priority data;
- provider durability claims are honest;
- prohibited secret/credential fields are not written to canonical Kitchen data.

---

## 14.5 Commit result

```yaml
CommitResult:
  status: enum
    - durable_committed
    - session_committed
    - partially_committed
    - deferred
    - rejected
  new_global_revision: integer?
  written_refs: list<EntityRef>?
  pending_changes: ChangeSet?
  warnings: list<string>?
  continuity_hint: string?
```

`continuity_hint` exists mainly for context-only implementations. It may help the Kernel preserve an authoritative natural-language state anchor without exposing database jargon.

`durable_committed` may only be returned when the provider truly supports durable write.

---

## 14.6 Provider failure/degraded mode

If a normally durable provider becomes unavailable:

- cooking/shopping assistance should continue if safe;
- changes may be retained as session-level pending changes when possible;
- the user should not be told data was durably saved when it was not;
- HealthEngine receives a storage degradation signal.

---

# 15. Interface 6 — `HealthEngine`

## 15.1 Responsibility

Detect and repair degradation of state, retrieval, active tasks, learned knowledge, and storage health.

It contains Monitor/Doctor behavior but remains one interface family.

It does not write providers directly.

---

## 15.2 Contract

```text
HealthEngine.inspect(HealthInput) -> HealthReport
HealthEngine.plan_repair(HealthReport, HealthContext) -> RepairPlan
```

---

## 15.3 `HealthInput`

```yaml
HealthInput:
  phase: enum
    - preflight
    - post_commit
    - maintenance
  meta: Meta?
  active_task: ActiveTask?
  retrieval_diagnostics: RetrievalDiagnostics?
  storage_health: StorageHealth?
  recent_health_signals: list<HealthSignal>?
```

Health does not need full history for routine inspection.

---

## 15.4 Health dimensions

Standard checks:

1. **State freshness** — volatile/high-risk data too old to trust.
2. **State consistency** — contradictory quantities/states.
3. **ActiveTask health** — task state drift, repeated completed steps, missing current phase.
4. **Context health** — excessive duplication, irrelevant retrieval, key current state missing.
5. **Experience health** — duplicate or contradictory learned patterns.
6. **Index health** — stale/missing derived index where relevant.
7. **Storage health** — provider read/write failure or schema mismatch.

---

## 15.5 `HealthReport`

```yaml
HealthReport:
  status: enum
    - healthy
    - attention
    - degraded
    - critical
  findings: list<HealthFinding>
  suggested_level: enum
    - silent
    - opportunistic
    - explicit_refresh
```

### `HealthFinding`

```yaml
HealthFinding:
  code: string
  severity: string
  scope_ref: EntityRef?
  summary: string
  evidence: object?
```

---

## 15.6 `RepairPlan`

```yaml
RepairPlan:
  changes: ChangeSet?
  maintenance_actions: list<MaintenanceAction>?
  user_check: UserCheckRequest?
  rationale: string?
```

### `MaintenanceAction`

```yaml
MaintenanceAction:
  type: enum
    - rebuild_index
    - compact_events
    - merge_experiences
    - reanchor_active_task
    - validate_schema
    - mark_cache_dirty
  scope: string?
```

Provider-specific implementation of maintenance is delegated through PersistenceCoordinator/provider support.

### `UserCheckRequest`

```yaml
UserCheckRequest:
  mode: enum
    - opportunistic
    - explicit
  question: string
  target_refs: list<EntityRef>?
```

The user should not be interrupted for silently repairable problems.

---

# 15.7 Startup / onboarding protocol

Startup behavior must be environment-neutral.

```text
1. Detect RuntimeCapabilities.
2. Resolve an already-configured compatible StorageProvider, if any.
3. If durable storage exists, read only Meta + the minimum continuity state needed.
4. If no durable provider exists, use ContextStateProvider without blocking the user.
5. Apply Simple or Expert onboarding behavior.
```

### Simple onboarding

- default unless the user asks for systematic setup;
- briefly explain that the system can learn inventory/equipment through normal use;
- do not require a database connection before answering the current task;
- progressively enrich KitchenState from conversation/photos/shopping/cooking.

### Expert onboarding

- explicitly present available durable provider choices when useful;
- help initialize inventory, equipment, preferences, plans, and health/refresh behavior;
- still prefer photos and conversation over manual form filling;
- expose architecture/storage details only to the extent the user requested.

### New-session continuity

- if a durable compatible provider is configured, `Meta` is the continuity entry point and Retriever loads only task-relevant slices;
- if only context persistence exists, continuity is best effort and the system must not claim exact cross-session inventory;
- the user should not be required to manually copy checkpoints or create a special conversation.

# 16. Kernel orchestration contract

The Kernel itself is deliberately not counted among the six service interfaces, but its orchestration sequence must be stable.

Recommended turn flow:

```text
1. TaskRequest created from current user input
2. RuntimeAdapter.capabilities()
3. ContextRetriever.bootstrap()
4. Kernel selects DomainModule
5. DomainModule.context_requirements()
6. ContextRetriever.retrieve()
7. Optional HealthEngine.inspect(preflight) for degradation/safety-relevant continuity
8. DomainModule.handle()
9. PersistenceCoordinator.commit(changes) if any
10. HealthEngine.inspect(post_commit) using cheap signals
11. If repair is needed:
      HealthEngine.plan_repair()
      PersistenceCoordinator.apply_repair()
12. Return/finalize response
```

Pure Web implementations may collapse several logical steps into one model turn. The contract describes responsibilities, not mandatory RPC calls.

---

# 17. Routing rules

Kernel route selection should use:

1. explicit current user request;
2. active task type/phase from RoutingContext;
3. recent direct observation;
4. fallback intent classifier.

Example:

User: “洋葱什么时候加？”

If `RoutingContext.active_task.type == cooking`, route to Cooking Live mode.

If no active task exists, route to Recipe/Cooking general advice.

A module may temporarily handle a subquestion without changing ActiveTask type.

Example: during Shopping task, a food-safety question can be answered by Inventory logic while preserving Shopping as the active task.

---

# 18. Context priority and conflict resolution

Retriever and DomainModule should preserve these priority classes:

```text
P0 safety-critical current observation
P1 current user observation
P2 ActiveTask current state
P3 KitchenState current records
P4 recent relevant Event
P5 relevant Experience / Preference
P6 base Recipe
P7 old conversation text
```

When two facts conflict:

- higher-priority evidence wins provisionally;
- state may be patched if the conflict is resolved;
- if the conflict materially changes safety/action and cannot be resolved, ask one focused question;
- do not load more history merely to avoid asking a necessary question.

---

# 19. Freshness / inventory check integration

Inventory refresh is not a separate disruptive workflow by default.

Retriever may generate `DueCheck` based on:

- perishability;
- time since verification;
- storage condition;
- open/thaw evidence;
- confidence;
- current task relevance.

DomainModule decides how to surface it.

Examples:

### Opportunistic before cooking

“如果还是上次那盒冷冻牛肉，我按冷冻状态给你步骤；它现在还一直冷冻着吗？”

### Opportunistic before shopping

“买之前顺便确认一下，上次那盒牛肉已经吃完了吗？”

### Explicit after long inactivity

“易腐库存很久没更新了，我先不按旧数量假设。拍一下冰箱/冷冻室，或者告诉我现在主要还有什么，我帮你快速刷新。”

No separate ReminderQueue is required for these behaviors in v0.5.

---

# 20. Live Cooking implementation contract

`ActiveTask(type=cooking)` should remain compact.

Recommended task-state fields:

```yaml
state:
  servings: number?
  equipment_refs: list<string>?
  ingredient_states: map<string, object>?
  step_states: map<string, TaskStepState>?
  deviations: list<string>?
```

Do not store every utterance.

Update only when:

- ingredient physical state changes materially;
- a stage/step completes;
- an unexpected event changes the plan;
- a safety-relevant fact changes;
- a long conversation needs re-anchoring.

When a deviation occurs:

```text
observe -> patch ActiveTask -> invalidate affected future step(s) -> local re-plan
```

Do not regenerate the entire Recipe unless the plan is globally invalidated.

---

# 21. Shopping implementation contract

`ActiveTask(type=shopping)` may contain:

```yaml
state:
  planned_recipe_refs: list<string>?
  target_items: map<string, object>?
  cart: list<object>?
  current_candidates: list<object>?
  storage_constraints: list<string>?
```

In-store recommendation factors:

- recipe fit;
- quantity fit;
- current inventory;
- freshness;
- price/value;
- storage fit;
- waste risk;
- preference fit;
- past experience where available.

The module may internally calculate a fit score, but the user does not need to see a numeric score unless useful.

When the user confirms purchase, generate a purchase Event and appropriate KitchenState patch.

---

# 22. Recipe feasibility and user-requested dish contract

A Recipe is fully feasible when:

1. all `required` ingredient requirements are available or deliberately substituted;
2. all required equipment capabilities are satisfied;
3. no unresolved safety or task-blocking issue exists.

`substitutable` ingredients may be satisfied by valid alternatives.

`optional` ingredients do not block recommendation.

Recipe ranking may prioritize:

- soon-to-use inventory;
- proven Experience;
- low waste;
- user preference;
- current equipment;
- current time/effort constraints.

When the user explicitly requests a dish, the module should additionally perform **gap analysis** rather than simply rejecting it:

- missing required ingredients -> produce the minimal practical purchase set;
- available valid substitutions -> prefer them when appropriate;
- missing optional ingredients -> do not block the dish;
- missing equipment capability -> first seek a safe adaptation using existing equipment;
- if adaptation is not practical, recommend the smallest additional hardware set that makes the dish feasible.

The gap analysis should respect the user’s current experience and relevant Experience records.

---

# 23. Experience compaction contract

Raw history should be compacted when repeated evidence produces reusable knowledge.

Suggested process:

```text
Event / observation
   ↓
Experience candidate
   ↓
merge by Experience.key
   ↓
update evidence_count/confidence/last_observed
   ↓
optionally promote stable personal value to KitchenState.preferences
```

Do not retain redundant Experience records with slightly different wording if they express the same learned rule.

Recent raw Events may remain available for debugging; they are not normal Context Pack content.

---

# 24. Provider portability contract

A provider is considered portable for future cross-platform continuity only if:

```yaml
shared_remote: true
durable_read: true
durable_write: true
```

and participating clients can access a compatible schema representation.

Examples intended for future portable support:

- Google Drive / Google Sheets;
- Tencent Docs;
- Notion;
- other explicit third-party memory/data platforms.

Local SQLite/local files are valid persistence, but not automatically cross-platform.

v1 assumes sequential use. Concurrent write resolution remains future work.

---

# 25. Deployment / bundle consistency

Source remains modular.

Recommended layers:

```text
core + contracts + domain logic
             ↓
runtime adapter
             ↓
persistence strategy
             ↓
selected storage provider
```

Possible built bundles:

### Pure Web bundle

- Kernel/core rules;
- shared domain contracts/logic;
- Web RuntimeAdapter;
- ContextStateProvider;
- ephemeral PersistenceCoordinator behavior;
- lightweight HealthEngine.

Exclude local DB/SQL/provider instructions.

### Web + Google Drive bundle

- same domain core;
- Web RuntimeAdapter;
- durable PersistenceCoordinator behavior;
- Google Drive provider;
- persistent Retriever implementation;
- durable Health behavior.

Do not include Tencent/Notion/SQLite provider details unless selected.

### Codex + SQLite bundle

- same domain core;
- Codex RuntimeAdapter;
- durable PersistenceCoordinator;
- SQLite provider;
- local indexing/Health implementation.

### Codex + Google Drive bundle

- same domain core;
- Codex RuntimeAdapter;
- durable PersistenceCoordinator;
- Google Drive provider.

Thus Codex and Web may share the same provider without sharing the same runtime implementation.

---

# 26. Interface dependency matrix

Allowed dependencies:

| Caller | RuntimeAdapter | StorageProvider | ContextRetriever | DomainModule | PersistenceCoordinator | HealthEngine |
|---|---:|---:|---:|---:|---:|---:|
| Kernel | yes | no | yes | yes | yes | yes |
| ContextRetriever | optional caps only | read only | — | no | no | no |
| DomainModule | no | no | no | — | no | emits signals only |
| PersistenceCoordinator | runtime/context metadata only | write/read-for-validation | no | no | — | no |
| HealthEngine | no direct runtime need | health/read summaries via inputs | diagnostics input | no | no | — |
| StorageProvider | no | — | no | no | no | no |

Important prohibitions:

- DomainModule -> StorageProvider: **forbidden**
- HealthEngine -> StorageProvider write: **forbidden**
- ContextRetriever -> PersistenceCoordinator: **forbidden**
- StorageProvider -> DomainModule: **forbidden**

---

# 27. Canonical collection ownership

| Object | Primary writer | Primary reader | Normal retrieval frequency |
|---|---|---|---|
| Meta | PersistenceCoordinator / Health repair | Retriever / Health | very high but tiny |
| KitchenState | PersistenceCoordinator | Retriever | high, sliced |
| ActiveTask | PersistenceCoordinator | Retriever | very high while active |
| Recipe | PersistenceCoordinator/import path | Retriever | task-dependent |
| Experience | PersistenceCoordinator/compaction | Retriever | selective |
| Event | PersistenceCoordinator append | Health / explicit retrieval | low |

---

# 28. Failure behavior

## 28.1 Storage unavailable

- continue current user assistance when possible;
- do not claim durable save;
- preserve pending changes at session level if possible;
- mark storage health degraded;
- retry only when supported/currently relevant;
- do not block an active cooking step merely because a cloud write failed.

## 28.2 Context degradation

Signals include:

- asking already-answered questions repeatedly;
- re-running completed steps;
- old state overriding recent observations;
- Context Pack dominated by duplicate history;
- active phase cannot be determined.

Repair:

- rebuild/re-anchor ActiveTask from latest user observation + authoritative state;
- ignore lower-priority old conversational facts;
- ask a single focused state question only when needed.

## 28.3 Long inactivity

- downgrade confidence/freshness for volatile inventory;
- keep stable equipment/preference records unless contradicted;
- trigger opportunistic or explicit refresh depending on current task and risk;
- do not erase everything merely because it is old.

---

# 29. Minimal physical mappings

These mappings are illustrative and do not change canonical contracts.

## 29.1 Google Sheets / Tencent spreadsheet

Possible sheets:

- META
- INVENTORY
- EQUIPMENT
- PREFERENCES
- PLANS
- ACTIVE_TASK
- RECIPES
- EXPERIENCES
- EVENTS

The logical `KitchenState` may span several sheets.

## 29.2 Notion

Possible databases/pages:

- Kitchen State collection(s)
- Active Task page/record
- Recipes DB
- Experiences DB
- Events DB
- Meta page

## 29.3 SQLite

Possible tables:

- meta
- inventory
- equipment
- preferences
- plans
- active_task
- recipes
- experiences
- events
- optional derived search/index tables

## 29.4 Pure Web

No physical schema is guaranteed.

The adapter maintains a compact authoritative conversational representation sufficient for the current interaction.

---

# 30. v0.5 consistency checklist

The following questions should be answered “yes” by every implementation:

1. Can DomainModule run without knowing whether storage is Drive/Notion/SQLite/context?
2. Can Codex use Google Drive without changing domain logic?
3. Can Web use Google Drive without loading Codex-local DB instructions?
4. Can Pure Web continue without pretending durability?
5. Does Retriever read only the context needed for the selected module?
6. Is Event history excluded from normal retrieval unless explicitly needed?
7. Can ActiveTask represent both cooking and shopping without separate session schemas?
8. Does PersistenceCoordinator own semantic write validation?
9. Does Doctor produce repairs rather than directly writing storage?
10. Can shared third-party storage become a future cross-platform Source of Truth?
11. Can history grow without normal Context Pack size growing proportionally?
12. Can the system recover from stale inventory by lowering confidence rather than hallucinating precision?

---

# 31. Open design items intentionally deferred

The following are **not** required to finish v0.5 interface compatibility:

- concurrent multi-client write conflict resolution;
- exact provider APIs for Google Drive/Tencent/Notion;
- UI design for future App;
- nutrition tracking;
- barcode/receipt integrations;
- family/multi-user inventory;
- background scheduler implementation;
- embeddings/vector DB choice;
- exact SQLite schema/index choice;
- provider authentication;
- provider-specific rate-limit strategies.

These should be added only after the canonical contracts stabilize.

---

# 32. Recommended next implementation step

After reviewing this v0.5 draft, implement one end-to-end vertical slice against all three operating modes:

> **Live Cooking + Inventory update for a simple dish**

Use the same test dialogue across:

1. Pure Web / ContextStateProvider;
2. Web + one durable shared provider;
3. Codex + one provider.

The test should verify:

- identical domain behavior;
- different persistence implementations;
- bounded retrieval;
- ActiveTask updates;
- post-cook KitchenState/Event/Experience updates;
- Health re-anchor after a long conversation;
- no provider-specific leakage into user-facing cooking guidance.

This vertical slice is the fastest way to validate whether the interfaces are truly coherent before adding more schema detail.
