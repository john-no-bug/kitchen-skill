# Context Retriever — Web Ephemeral

## Goal

Select only enough context to answer the current live-cooking decision. Do not attempt to search or reconstruct the entire conversation.

## Bootstrap

Infer a minimal routing context from:

1. newest user message;
2. latest clearly active cooking state if visible.

## Retrieval slots for live cooking

Required when available:

- current physical observation;
- current phase and completed major milestones;
- directly involved ingredients;
- current equipment constraint.

Optional:

- one small relevant prior experience/base-recipe dependency;
- one due clarification if it materially changes the next action.

## Budget discipline

Prefer a compact state summary over multiple historical mentions of the same fact. Old semantically similar text must not displace newer state.

If state is ambiguous, preserve `unknown`; do not fabricate a precise reconstruction.
