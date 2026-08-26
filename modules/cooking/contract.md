# Cooking Module Contract

## Responsibility

Guide the user through physically executing a dish using current ingredient/equipment state, with local adaptation when reality deviates from the base recipe.

## Input

- current user request/observation;
- bounded ContextPack;
- optional current ActiveTask.

## Output semantics

The module conceptually returns:

- user-facing response;
- ActiveTask changes;
- optional state observations or tentative experience observations.

In the Pure Web slice these are expressed conversationally; no durable storage is claimed.

## Rules

- Answer the immediate physical problem first.
- Prefer current action + sensory completion cue + at most the next useful action.
- Do not dump the entire recipe unless asked.
- Deviations trigger local re-planning, not a full restart.
- Never repeat a completed major step as pending.
- Ask only decision-changing questions when no safe/useful default exists.
- A single outcome/feedback observation is tentative, not automatically a stable preference.
