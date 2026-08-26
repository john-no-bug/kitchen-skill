# Health Engine — Web Ephemeral

## Cheap Monitor

Before a live-cooking reply, detect whether the candidate answer would:

- repeat a completed step;
- use older physical state over a newer observation;
- ask an already-resolved question;
- retain an invalid pending step after a deviation;
- include irrelevant historical/recipe detail merely because the chat is long;
- claim durable cross-session memory.

## Doctor / re-anchor

On detection, silently rebuild the smallest authoritative state from:

1. newest direct observation;
2. newest non-conflicting ActiveTask facts;
3. compact completed milestones;
4. unresolved facts marked unknown.

Then answer from that state. Never mention Doctor, context repair, reset, database maintenance, or checkpoint mechanics to the user.

## Explicit refresh

Pure Web cannot prove volatile state survived a new conversation. If old inventory/state is required but unavailable, ask only for the minimum current fact needed or invite a low-friction refresh such as a photo. Do not require a manual session export.
