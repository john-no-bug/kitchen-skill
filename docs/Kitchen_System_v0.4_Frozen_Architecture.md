# Kitchen System v0.4 — Frozen Architecture Snapshot

**Status:** Frozen baseline / rollback point  
**Date:** 2026-08-25  
**Purpose:** This document is a self-contained snapshot of the Kitchen System architecture agreed before formal interface/schema definition. If later design work becomes inconsistent or over-complex, start a new session with this file and continue from v0.4.

---

## 0. New-session bootstrap

When this document is supplied in a new session, treat it as the authoritative architecture baseline.

Continue from the following next step unless the user asks to revise v0.4 first:

> Formally define the six stable interfaces — `RuntimeAdapter`, `StorageProvider`, `ContextRetriever`, `DomainModule`, `PersistenceCoordinator`, `HealthEngine` — and the six core data objects — `KitchenState`, `ActiveTask`, `Recipe`, `Experience`, `Event`, `Meta` — using minimal, runtime-neutral schemas and contracts.

Do **not** reintroduce removed first-class concepts such as separate `CookingSession`, `ShoppingSession`, `WorkingSnapshot`, `Checkpoint`, `KitchenCapsule`, or a dedicated `ReminderQueue` unless there is a demonstrated need. These are currently treated as representations, operations, or derived views of the six core objects.

---

# 1. Product goal

Kitchen System is a low-friction personal kitchen assistant that helps with:

- food/inventory management;
- recipe discovery and recommendation;
- adaptation to the user's actual equipment;
- live cooking guidance;
- shopping planning;
- in-store ingredient/product selection;
- freshness and inventory refresh checks;
- learning from cooking history and feedback;
- sustainable long-term personalization without letting context grow without bound.

The system should feel like a helpful cooking companion, **not** a household ERP system. The user should not be asked to maintain tables or databases manually.

Core product maxim:

> **The user lives; the system organizes.**

---

# 2. Design constitution

The following principles are considered system-level rules.

## 2.1 Low-friction capture

Prefer information acquisition in this order:

1. natural conversation;
2. photos / visual recognition;
3. information naturally produced during shopping;
4. information naturally produced during cooking;
5. history-based inference;
6. a short confirmation question;
7. explicit structured entry only as a last resort.

Never make database completeness a prerequisite for helping the user.

## 2.2 Ask only decision-changing questions

Missing information does not automatically justify a question.

Ask only when the missing fact materially changes the current decision, safety judgment, shopping recommendation, or cooking action.

## 2.3 Progressive precision

The internal schema may support rich detail, but the user should be allowed to provide minimal information.

Inventory precision can be:

- presence: `salt = available`;
- level: `olive oil = about half bottle`;
- approximate: `onion ≈ 2`;
- exact: `ground beef = 320 g`.

Do not fabricate exactness when only approximate information is known.

## 2.4 Store richly, retrieve sparsely

Long-term history may grow, but a single model call must load only the information relevant to the current task.

Normal reasoning must never depend on reading the entire history.

100 cooking events and 1,000 cooking events should produce approximately the same-sized task context.

## 2.5 Current reality outranks records

Evidence priority:

1. user's current direct observation;
2. latest authoritative task state;
3. current persistent state;
4. recent events;
5. experience summaries / learned patterns;
6. old conversation text.

If the user says the pan is burning, the system must react to the pan, not to an old recipe timer.

## 2.6 Personalization grows from evidence

A single observation should not immediately become a permanent preference.

Suggested progression:

`Observation -> Tentative Pattern -> Learned Preference -> Stable Preference`

Learned preferences should support confidence, evidence count, and last verification time.

## 2.7 Do not pollute global/general memory with volatile kitchen data

Inventory such as “half an onion” or “200 g beef” belongs to Kitchen State, not general-purpose user memory.

If domain-scoped memory is unavailable, prefer an external kitchen store or no durable memory over polluting unrelated conversations.

## 2.8 Graceful degradation

The system must still be useful in the weakest environment.

No database, file system, cloud connector, scheduler, or project feature may be required for basic cooking assistance.

## 2.9 Architecture concepts must not leak into normal UX

Users should not be instructed to create `CookingSession`, save checkpoints, manage JSON, or understand Context Packs.

These are implementation concepts only.

## 2.10 Two onboarding modes

### Simple mode

Default for ordinary users. Initialization is progressive and must not block the current cooking/shopping task. The user only needs a short explanation of what the assistant can do. Kitchen knowledge is accumulated naturally through conversation, photos, shopping, and cooking.

### Expert mode

For users who explicitly want systematic setup. The system may explain storage choices and help initialize inventory, equipment, preferences, planning, reminders/health checks, and other supported features in a structured way. Even here, photos and conversation should be preferred over form-like data entry.

Storage setup is optional in Simple mode and configurable in Expert mode. If no durable provider exists, fall back to context-only operation rather than blocking assistance.

## 2.11 Evolvability without self-corruption

The fixed Kernel and safety rules should remain stable. Personalization evolves through `KitchenState.preferences`, `Experience`, observed equipment capability, and compact learned patterns. The system should not arbitrarily rewrite its core rules based on a few interactions.

---

# 3. Runtime and storage are separate dimensions

A major architecture decision in v0.4 is that **execution environment and persistence backend are independent**.

## 3.1 Execution runtimes

Two primary execution runtimes are currently recognized:

### `WEB_CHAT`

A normal conversational web environment such as ChatGPT, Claude, DeepSeek, or another chat host.

Capabilities may vary by host and account. Therefore the design must not hard-code Free/Plus/Project assumptions.

### `CODEX`

A coding/workspace runtime with stronger access to local files, code execution, indexing, and potentially databases.

Codex does **not** imply local persistence. It may also use a remote shared provider such as Google Drive.

## 3.2 Persistence backends

Possible storage providers include:

- `CONTEXT_ONLY`;
- Google Drive / Google Sheets;
- Tencent Docs;
- Notion;
- generic persistent file storage;
- local files;
- SQLite;
- future providers.

## 3.3 Three user-facing operating modes

The project currently focuses on three practical modes:

### Mode A — Pure Web

`WEB_CHAT + CONTEXT_ONLY`

- no guaranteed durable state;
- current conversation is the working substrate;
- cross-session continuity is best effort only;
- must never pretend exact old inventory is still known.

### Mode B — Web + Persistent Store

`WEB_CHAT + remote/file persistent provider`

Examples:

- Google Drive / Sheets;
- Tencent Docs;
- Notion;
- another persistent file store.

This is the preferred long-term web mode.

### Mode C — Codex

`CODEX + selected provider`

The provider may be:

- SQLite;
- local files;
- Google Drive;
- Tencent Docs;
- Notion;
- another compatible provider.

No architecture rule binds Codex to local storage.

---

# 4. Cross-platform support

Cross-platform continuity is enabled only when the selected persistence backend is itself portable/shared across clients.

Examples:

- ChatGPT Web + Google Drive -> potentially cross-platform;
- Claude Web + Google Drive -> potentially cross-platform;
- Codex + Google Drive -> potentially cross-platform;
- Codex + SQLite -> local only;
- Pure Web context-only -> not reliably portable.

Current v1 scope explicitly **does not solve concurrent conflicting writes** between multiple clients.

Sequential multi-client use may be supported later through shared storage.

It is still useful to retain lightweight fields such as:

- `revision`;
- `updated_at`;
- `provenance` / source.

These support freshness checks, schema maintenance, debugging, and future synchronization without requiring distributed conflict resolution now.

---

# 5. Final top-level architecture

The architecture is frozen at seven components:

```text
Kitchen Kernel
│
├── Runtime Adapter
├── Domain Modules
├── Context Retriever
├── Persistence Coordinator
├── Storage Provider
├── Health Engine
└── Builder / Loader
```

Each component has one responsibility.

---

# 6. Kitchen Kernel

The Kernel should remain small and stable.

Responsibilities:

- detect runtime capabilities;
- identify user intent;
- select the relevant domain module;
- request a Context Pack;
- call the domain module;
- pass requested state changes to Persistence Coordinator;
- trigger cheap health checks;
- return the user-facing response.

The Kernel must **not**:

- contain provider-specific API instructions;
- execute SQL directly;
- manipulate Google Drive directly;
- implement inventory logic itself;
- implement recipe logic itself;
- scan full history;
- become a giant all-feature prompt.

---

# 7. Runtime Adapter

The Runtime Adapter describes what the current host can do.

It answers capability questions, not kitchen questions.

Example capability dimensions:

- conversation context available;
- vision available;
- dynamic module loading available;
- file system available;
- code execution available;
- external connectors available;
- scheduler/background task capability available.

Runtime should not encode Google Drive/Notion as a business rule. Provider selection is separate.

Key principle:

> Branch on capabilities, not subscription names.

---

# 8. Domain Modules

Current domain modules:

- inventory;
- cooking;
- shopping;
- recipes;
- planning;
- equipment.

Possible future modules may be added, but the Kernel must not expand linearly with them.

Each domain module expresses **what should happen**, not where data is stored.

Modules should return structured requested changes rather than writing storage directly.

---

# 9. Storage Provider

Storage providers are business-agnostic.

They do not know what beef, recipes, or cooking mean.

Conceptual capabilities:

- read;
- write;
- patch;
- append;
- search.

Possible provider capabilities:

- durable read;
- durable write;
- partial update;
- append support;
- structured search;
- text search;
- shared remote storage.

Providers include:

- ContextStateProvider;
- GoogleDriveProvider;
- TencentDocsProvider;
- NotionProvider;
- GenericFileProvider;
- LocalFileProvider;
- SQLiteProvider.

## 9.1 Context-only as a provider

Pure Web should still conform to the same high-level storage contract through `ContextStateProvider`.

Its behavior is approximate:

- `read` -> reconstruct latest authoritative state from visible context;
- `patch` -> create/update a natural authoritative state anchor;
- `append` -> fold essential information into current task/state when useful;
- `search` -> use currently visible conversational context.

Its durability capability is false.

This keeps upper layers consistent across environments.

---

# 10. Persistence Coordinator

Only the Persistence Coordinator should perform state write orchestration.

Domain modules and Doctor produce patches/plans; they do not write providers directly.

Responsibilities may include:

- validate patches;
- normalize units;
- apply canonical schema;
- update Kitchen State;
- update ActiveTask;
- append Events;
- store/merge Experience observations;
- update metadata;
- mark derived indexes dirty;
- delegate actual persistence to the selected Storage Provider.

This single write path improves traceability and debugging.

---

# 11. Context Retriever

The Context Retriever is read-only.

It selects the smallest useful Context Pack for the current task.

Conceptual contract:

```text
retrieve(
    task_request,
    active_task,
    budget
) -> ContextPack
```

The implementation differs by environment/provider.

### Pure Web

Use:

- current user message;
- latest authoritative task state;
- relevant recent facts;
- at most a small amount of directly relevant experience from visible context.

### Web + persistent store

Use:

- current message;
- relevant current state entries;
- active task;
- relevant equipment;
- relevant recipes/experience;
- due checks.

Do not load the whole spreadsheet/document.

### Codex

May use:

- key lookup;
- local indexing;
- FTS;
- optional semantic retrieval;
- structured queries.

Still must obey a bounded context budget.

## 11.1 Context Pack

Conceptual contents:

- task;
- current state;
- active task;
- relevant inventory;
- relevant equipment;
- relevant recipes;
- relevant experiences;
- relevant preferences;
- due checks;
- conflicts;
- confidence.

A Context Pack is temporary and should not accumulate across turns.

---

# 12. ActiveTask

`ActiveTask` replaces several earlier first-class concepts.

It represents the user's current operational activity.

Possible task types:

- cooking;
- shopping;
- planning;
- potentially other future task types.

Conceptual minimal fields:

- type;
- goal;
- phase;
- state;
- completed;
- next;
- open issues;
- updated time.

## 12.1 Removed duplicate concepts

- `CookingSession` is no longer a separate first-class schema.
- `ShoppingSession` is no longer a separate first-class schema.
- `Working Snapshot` is the representation of ActiveTask in context-only environments.
- `Checkpoint` is the operation of replacing/updating the authoritative ActiveTask state.

Thus there is one schema, not four.

---

# 13. Live Cooking

Live Cooking is a behavior of the cooking module operating on `ActiveTask(type=cooking)`.

The user never manually creates a session.

The system should maintain only the operational state needed to guide the next action.

Important behavior:

- prioritize safety;
- prioritize the user's current physical observation;
- respond with the current action and usually only the next 1–2 steps;
- update task state when meaningful changes occur;
- locally re-plan when unexpected states occur;
- avoid reprinting the entire recipe after every interruption.

## 13.1 Lightweight task graph

Cooking flow may be represented conceptually as dependencies rather than a rigid numbered list.

Example:

```text
soften_beef -> break_apart -> evaporate_water -> brown_beef -> add_onion
```

This supports deviations such as frozen ingredients.

The implementation should stay lightweight; do not introduce a large workflow engine unless later proven necessary.

---

# 14. Shopping

Shopping includes both:

- pre-shopping planning/list generation;
- in-store product/ingredient selection.

Selection should consider, when relevant:

- planned recipes;
- expected quantity;
- current inventory;
- package size;
- storage capacity;
- freshness;
- price/value;
- waste risk;
- user preferences;
- previous purchase/use experience.

The shopping process should also act as a low-friction inventory capture mechanism.

If the user says “I bought this 500 g beef pack,” the system should naturally treat that as a purchase observation instead of later asking the user to re-enter it.

---

# 15. Inventory

Inventory is a part of `KitchenState`, not a separate database service.

Useful characteristics:

- identity/name;
- amount at flexible precision;
- storage location/state when needed;
- freshness/safety-relevant facts when needed;
- confidence;
- last verified/updated information;
- optional richer detail.

Do not force rich fields during normal entry.

High-risk inventory checks should be integrated into natural flows such as:

- before cooking;
- before shopping;
- after shopping;
- when an ingredient is about to be used;
- when a user reports opening/freezing/thawing/discarding;
- when returning after long inactivity.

Avoid annoying standalone audits.

If the kitchen has not been updated for a long time, stale volatile inventory should be downgraded in confidence rather than treated as precise fact.

---

## 15.1 User-requested dish / upgrade analysis

When the user specifies a dish rather than asking for discovery, the system should perform a gap analysis:

- compare required ingredients with current inventory;
- identify valid substitutions already available;
- recommend only the missing purchases that materially improve feasibility;
- compare required equipment capabilities with current equipment;
- if hardware is insufficient, identify the smallest practical additional hardware set rather than proposing a full kitchen upgrade;
- adapt the cooking flow to the user’s experience and proven equipment capabilities.

This is a Recipe/Planning behavior, not a separate top-level subsystem.

# 16. Recipes and Experience

These concepts are intentionally separate.

## Recipe

Represents **how to make something**.

May contain:

- ingredients;
- required equipment/capabilities;
- optional substitutions;
- base steps;
- constraints.

## Experience

Represents **what was learned from actual user interaction/history**.

Examples:

- this user's Supor pot can successfully sauté ground beef open-lid;
- frozen ground beef worked with a soften -> break apart -> evaporate -> brown adaptation;
- the user's pasta portion appears to be ~85 g.

Repeated events should be compacted into Experience rather than repeatedly retrieved raw.

---

# 17. Event

An Event describes **what happened**.

Examples:

- purchased 500 g beef;
- used ~120 g beef;
- discarded milk;
- froze leftover meat;
- recipe feedback: portion too large;
- equipment capability observed.

Events provide traceability and can support rebuilding/repair, but are cold data and should not normally be loaded into model context.

---

# 18. State vs Event vs Experience vs Preference

These meanings must remain distinct:

### State

What is true now.

Example: `ground beef ≈ 250 g frozen`.

### Event

What changed/happened.

Example: `used ~120 g beef`.

### Experience

What reusable operational knowledge was learned.

Example: `frozen beef can be handled with this pot using X adaptation`.

### Preference

A relatively stable user-specific tendency.

Example: `one-person dry pasta portion ≈ 85 g`.

Avoid storing the same observation redundantly in multiple first-class stores.

---

# 19. Health Engine

Health Engine contains two conceptual roles:

- Monitor;
- Doctor.

They should not become heavyweight autonomous agents.

## 19.1 Monitor

Monitor checks system health.

Important areas:

- state freshness;
- state consistency;
- active-task drift;
- context degradation;
- index freshness;
- duplicate/contradictory learned knowledge;
- storage health.

A cheap monitor can run frequently; full checks run only when justified.

## 19.2 Doctor

Doctor proposes repairs.

Possible repairs:

- rebuild authoritative task state;
- merge duplicate experiences/preferences;
- mark stale inventory uncertain;
- request refresh at the next natural opportunity;
- rebuild derived index;
- recover from storage failures;
- re-anchor to current user observations.

Doctor should return a repair plan / patch, not write storage directly.

## 19.3 Repair levels

### Silent repair

No user interruption.

Examples: rebuild index, merge duplicates, compact history.

### Opportunistic check

Ask naturally inside an already relevant workflow.

Example before cooking: “If this is still the same frozen beef, I’ll use the frozen-beef steps.”

### Explicit refresh

Used when data has become too stale to responsibly rely on.

Example after long inactivity: ask for a quick fridge/freezer photo or a short inventory refresh.

The system should be willing to say old inventory is stale rather than maintain a false appearance of precision.

---

# 20. Persistence and history compaction

Long-term history should conceptually follow:

```text
Raw Events
   ↓
Experience / learned patterns
   ↓
Stable compact knowledge
```

Recent detailed events may be retained for traceability, while older repetitive history can be compacted.

Normal retrieval should strongly prefer compact Experience over raw event history.

---

# 21. Index

Index is derived data, never a source of truth.

It may index:

- state entries;
- recipes;
- experiences;
- selected events.

If the index is lost or inconsistent, Doctor rebuilds it from canonical data.

Do not reconstruct true inventory from an index alone.

---

# 22. Canonical Kitchen Schema

Storage-specific formats should map to the same logical collections:

- `META`;
- `STATE`;
- `ACTIVE_TASK`;
- `RECIPES`;
- `EXPERIENCES`;
- `EVENTS`;
- optional derived `INDEX`.

Provider mappings may differ:

- Google Sheets -> sheets/tables;
- Notion -> databases/pages;
- SQLite -> tables;
- JSON -> collections;
- context-only -> conversational representation.

Business semantics must remain provider-independent.

---

# 23. Module and write-flow consistency

A domain module should conceptually follow:

```text
handle(TaskRequest, ContextPack) -> ModuleResult
```

Possible `ModuleResult` contents:

- user response;
- state patch;
- active-task patch;
- events;
- experience observations;
- health signals.

The module does not write storage.

Write flow:

```text
Domain Module / Doctor
        ↓
requested Patch / Event / RepairPlan
        ↓
Persistence Coordinator
        ↓
Storage Provider
```

There should be one orchestrated write path.

---

# 24. Core data-flow

The current frozen data flow is:

```text
User Message
     ↓
Runtime Adapter
     ↓
Kitchen Kernel
     ↓
Intent Router
     ↓
Context Retriever ─────────→ Storage Provider
     ↓
ContextPack
     ↓
Domain Module
     ↓
ModuleResult
     │
     ├── response
     ├── state_patch
     ├── active_task_patch
     ├── events
     └── experience observations
     ↓
Persistence Coordinator
     ↓
Storage Provider
     ↓
Health Monitor
     ↓
(optional) Doctor
     ↓
RepairPlan
     ↓
Persistence Coordinator
```

Important invariant:

> Storage Provider is the component that actually touches storage; domain logic should not contain provider-specific writes.

---

# 25. Source layout / modular Skill packaging

The source should remain modular even if a target platform cannot dynamically load files.

Recommended conceptual source structure:

```text
kitchen/
│
├── SKILL.md
├── core/
│   ├── kernel.md
│   ├── routing.md
│   ├── state-policy.md
│   └── safety.md
│
├── contracts/
│   ├── runtime.md
│   ├── storage.md
│   ├── module.md
│   ├── retrieval.md
│   ├── persistence.md
│   └── health.md
│
├── modules/
│   ├── inventory/
│   ├── cooking/
│   ├── shopping/
│   ├── recipes/
│   ├── planning/
│   └── equipment/
│
├── runtime/
│   ├── web.md
│   └── codex.md
│
├── persistence/
│   ├── ephemeral.md
│   └── durable.md
│
├── providers/
│   ├── context.md
│   ├── google_drive.md
│   ├── tencent_docs.md
│   ├── notion.md
│   ├── local_files.md
│   └── sqlite.md
│
├── health/
│   ├── monitor.md
│   └── doctor.md
│
└── schemas/
    ├── state.md
    ├── active_task.md
    ├── event.md
    ├── experience.md
    └── meta.md
```

## 25.1 Contracts vs implementations

Common business rules belong in shared contracts/logic.

Runtime/provider details must not be copied into each business module unless truly necessary.

This avoids three independent inventory/cooking/shopping implementations drifting over time.

## 25.2 Dynamic loading vs build-time bundling

Do not assume all hosts support runtime module import.

Two valid deployment strategies:

### Loader-capable host

Load only the needed module and runtime/provider implementation.

### Prompt-only host

Use a build step that produces small runtime bundles, e.g.:

- pure-web bundle;
- web + selected persistent provider bundle;
- codex + selected provider bundle.

Source modularity is preserved even when runtime loading is unavailable.

---

# 26. Context-size sustainability rules

The architecture specifically targets the failure mode “works well in early turns, becomes slow/confused later.”

Hard rules:

1. A normal response must not depend on full history.
2. Historical growth must not produce proportional Context Pack growth.
3. Context Packs are temporary and replaced each turn.
4. Old conversation text is weaker evidence than current structured/authoritative state.
5. Repetitive history should compact into Experience.
6. Pure-web mode should maintain a rolling authoritative state anchor instead of treating all prior turns equally.
7. If context appears degraded, Doctor re-anchors from current user observation and authoritative state.

---

# 27. What is explicitly NOT first-class in v0.4

The following earlier concepts have been intentionally removed or demoted:

### `CookingSession`

Use `ActiveTask(type=cooking)`.

### `ShoppingSession`

Use `ActiveTask(type=shopping)`.

### `WorkingSnapshot`

A context-only representation of `ActiveTask`, not a separate schema.

### `Checkpoint`

An update/overwrite operation on authoritative task state, not a persistent object.

### `KitchenCapsule`

May later exist as an export/backup representation, but is not a core object.

### `ReminderQueue`

Not currently a core object. Due checks can be represented through state/meta/health until a dedicated scheduler need is proven.

### giant agent swarm

Do not create separate Planner Agent, Inventory Agent, Recipe Agent, Memory Agent, Monitor Agent, Doctor Agent, etc. unless later evidence proves the need.

Prefer one Kitchen Agent using deterministic/structured services.

---

# 28. Current frozen interfaces and core objects

The architecture is ready to formally define the following six interfaces:

1. `RuntimeAdapter`
2. `StorageProvider`
3. `ContextRetriever`
4. `DomainModule`
5. `PersistenceCoordinator`
6. `HealthEngine`

And the following six core data objects:

1. `KitchenState`
2. `ActiveTask`
3. `Recipe`
4. `Experience`
5. `Event`
6. `Meta`

The next design version should define minimal schemas and contracts without expanding the top-level architecture unless a concrete inconsistency is found.

---

# 29. Validation questions for future revisions

Any future feature should pass these checks:

1. Does it require a new first-class object, or can it be expressed through existing six objects?
2. Is it business logic, runtime behavior, persistence behavior, provider behavior, retrieval behavior, or health behavior?
3. Is provider-specific knowledge leaking into a domain module?
4. Is a domain module writing storage directly?
5. Is derived/indexed data being treated as truth?
6. Will this feature make normal Context Packs grow with history size?
7. Does it impose manual database maintenance on the user?
8. Does it work gracefully in pure-web mode?
9. Does it remain portable when a shared third-party provider is used?
10. Does the user need to know the underlying architecture? If yes, can that leakage be removed?

---

# 30. Rollback statement

This document is the authoritative **Kitchen System v0.4 frozen architecture**.

If later work becomes inconsistent, over-engineered, provider-bound, or too large for web contexts, revert to this file and restart formal design from the six interfaces and six core data objects listed above.
