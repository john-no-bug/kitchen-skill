# Candidate Scenario — Long History Compaction and Bounded Context

Candidate-visible. Evaluator expectations must remain unread until all baseline/post-growth probe responses, ContextPack selections, and compaction provider traces are frozen.

## Purpose

Exercise one real Google Sheets store through:

1. small-history baseline retrieval;
2. growth to 2000 Event rows and 122+ Experience rows;
3. bounded Event -> Experience compaction;
4. the same normal Cooking/Shopping retrieval after history growth.

## Canonical test identities

Use stable IDs/keys throughout the run.

Relevant Cooking Experience:

- id: `exp-frozen-beef-supor-pot`
- key: `frozen_ground_beef:supor_green_pot`
- kind: `ingredient_behavior`
- initial evidence_count: `3`
- status: `active`
- confidence: `high`
- compact summary: frozen ground beef in the Supor green pot may release substantial water; break apart, evaporate excess water, then brown.

Relevant Shopping Experience:

- id: `exp-shopping-beef-350g`
- key: `shopping_beef:350g_plan`
- kind: `shopping_pattern`
- evidence_count: `4`
- status: `active`
- compact summary: when about 350 g is planned and price/storage/future-use do not change the decision, a 500 g package creates less surplus than 1 kg.

Current equipment:

- id: `equipment-supor-green-pot`
- capability includes saute / open-lid heating.

## Matching Event key

Every Event intended as compatible evidence for the Cooking Experience must contain the exact searchable marker:

`frozen_ground_beef:supor_green_pot`

Noise Events must not contain that exact marker.

## Baseline history

Before the baseline probes:

- Events contains exactly 3 compatible evidence Events for the Cooking Experience plus no bulk noise history;
- relevant Cooking Experience already represents those 3 Events;
- its `evidence_event_refs` contains those 3 refs;
- relevant Shopping Experience exists;
- `Meta.last_compaction_at` is later than the third initial compatible Event and earlier than all 17 compatible Events that will be appended during growth.

## Baseline Cooking probe — C0

Exact current user message:

> 我还是用苏泊尔小绿锅处理冷冻牛肉末。现在已经能铲散，但锅里水很多，下一步呢？

Build/freeze the normal Cooking retrieval evidence and user-facing response.

The current message is direct physical evidence. The relevant Experience may inform technique but must not override the user's current state.

Record a deterministic selected-context measurement:

- selected canonical record IDs/types;
- count of selected STATE records;
- count of selected Experiences;
- count of selected Events;
- UTF-8 byte length of canonical JSON for selected persisted records only.

Do not include provider search diagnostics/raw rows in the selected-record byte measurement.

## Baseline Shopping probe — S0

Exact current user message:

> 我在店里买牛肉，两顿大概需要350g，500g和1kg都有，价格先不考虑，买哪个？

Build/freeze normal Shopping retrieval evidence and user-facing response.

Record the same deterministic selected-context measurement.

These probes must not mutate the store merely for measurement.

## History growth

After C0/S0 freeze, append history efficiently using provider batch operations.

Required final Event history:

- 3 original compatible Events;
- 17 **new** compatible Events after `Meta.last_compaction_at`;
- 1980 irrelevant/noise Events;
- total Event data rows = **2000**.

Required Experience history after growth but before compaction:

- the 2 relevant Experiences above;
- at least 120 irrelevant and/or superseded Experience rows;
- total Experience data rows >= **122**.

At least 8 of the noise Experiences should be `status=superseded` and contain superficially similar beef/pot tags, so ranking/status filtering is exercised. They must not reuse the exact stable key of the active relevant Experience.

Bulk seed may use provider-efficient chunked `pasteData` / batch requests. Keep each provider call within host limits. The seeded rows are test data only.

Do not change the current Cooking/Shopping probe facts while growing history.

## Compaction maintenance — M1

Run explicit bounded Health maintenance using the v0.8 compaction profile.

Candidate selection requirements:

- start from META / `last_compaction_at`;
- search/filter for the exact matching Event key;
- only the 17 new compatible Event payloads may be accepted as new evidence;
- compaction reasoning context may contain at most 64 candidate Events and 8 existing Experiences;
- read the current canonical target Experience before mutation.

Produce a Health RepairPlan / semantic ChangeSet that merges the 17 unique compatible Events into the existing `exp-frozen-beef-supor-pot` Experience.

Required post-merge canonical result:

- same Experience `meta.id`;
- same `key`;
- `evidence_count: 20`;
- `status: active`;
- compact summary/conditions remain reusable, not transcript-like;
- `evidence_event_refs` contains at most 8 representative/recent refs;
- no Event row is deleted or rewritten;
- `Meta.last_compaction_at` advances only in the successful compaction commit.

The write must flow:

`HealthEngine -> RepairPlan/ChangeSet -> PersistenceCoordinator -> GoogleDriveProvider`

No domain module direct provider write.

Freeze the compaction candidate selection, RepairPlan/ChangeSet summary, provider write trace, and bounded readback evidence before evaluator expectations are loaded.

## Long-history Cooking probe — C1

Repeat the exact C0 user message after compaction.

Freeze normal retrieval evidence and user-facing response.

Requirements:

- no EVENTS read for normal candidate generation;
- relevant active Cooking Experience selected;
- at most 2 Experiences selected;
- superseded/noise Experiences excluded;
- current direct observation still outranks Experience;
- record deterministic selected-context measurement using the exact C0 method.

## Long-history Shopping probe — S1

Repeat the exact S0 message after compaction.

Freeze normal retrieval evidence and user-facing response.

Requirements:

- no EVENTS read for normal candidate generation;
- relevant Shopping Experience selected when useful;
- at most 1 Experience selected;
- record deterministic selected-context measurement using the exact S0 method.

## Context-growth comparison

For C0 vs C1 and S0 vs S1, compare selected persisted-record context only.

Pass-oriented structural expectation:

- selected Event count remains 0;
- Experience count remains within the same hard domain limit;
- selected-record UTF-8 byte size after long-history growth is no more than baseline + 2048 bytes and no more than 1.5x baseline, unless the baseline is so small that only the absolute +2048 bound is meaningful;
- any increase must be attributable to compact metadata such as higher `evidence_count` / capped evidence refs, not to raw history rows.

## Post-freeze audit

Only after C0/S0, history-growth write trace, M1, C1/S1, and all measurements are frozen may evaluator expectations be loaded.

Evaluator-only audit may then verify:

- Event row 2001 exists (header + 2000 data rows);
- initial/late compatible Event sentinels remain present;
- the target Experience is evidence_count 20 with <=8 refs;
- relevant/noise/superseded Experience counts;
- `Meta.last_compaction_at` moved forward;
- no extra provider tables exist;
- domain source files remain provider-neutral.
