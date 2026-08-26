# Runtime Adapter — Web Ephemeral

## Runtime

`WEB_CHAT`

## Assumptions

- current conversation context is available;
- no guaranteed filesystem;
- no guaranteed database;
- no guaranteed durable cross-chat memory;
- no guaranteed background process or scheduler.

Do not branch on Free/Plus or any vendor plan name. Branch only on actual capabilities surfaced by the host.

## ActiveTask representation

`ActiveTask` is a logical state represented by the newest authoritative conversational facts. There is no requirement to create a file, session object, or checkpoint artifact.

A checkpoint means only that a newer task state supersedes an older one.

## Degradation rule

If the host later exposes durable storage, persistence may be upgraded by a separate provider without changing cooking-domain logic.
