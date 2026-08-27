# History Compaction Test Suite

This suite validates the frozen invariant:

> history growth must not cause proportional ContextPack growth.

The v0.8 slice treats compaction as logical Event -> Experience aggregation:

- Events remain append-only cold data;
- compatible repeated evidence merges into compact Experience;
- normal Cooking/Shopping retrieval selects only a bounded number of Experiences;
- normal retrieval uses zero Events by default;
- Experience evidence refs are capped so the selected Experience itself cannot grow linearly with raw evidence count.

## Real gate

Run exactly one dedicated test conversation with:

`demo/HISTORY_COMPACTION_LONG_CONTEXT_PROMPT.md`

The runner creates an isolated Google Sheet, captures small-history Cooking/Shopping baselines, seeds 2000 Event rows and 122+ Experience rows, runs bounded compaction, repeats the normal retrieval probes, reports to GitHub Issue #6, and cleans up only after a clean PASS.

Do not execute the formal gate in a conversation that has already read `tests/history/expectations/*`.
