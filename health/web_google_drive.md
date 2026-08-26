# Health Engine — Web + Google Drive

## Scope

Cheap persistent-mode Monitor/Doctor behavior for the first durable slice.

Health may inspect provider/retrieval/task signals, but it does not write Google Drive directly.

## Preflight checks

Before a live-cooking reply, detect whether:

- META cannot be read or has an incompatible store marker/schema;
- META points to an ActiveTask that is missing or contradictory;
- a newer direct observation conflicts with stored task state;
- volatile inventory used by the current decision is too stale to trust;
- retrieval included irrelevant/duplicate historical records;
- the candidate answer would repeat a completed step;
- storage is degraded but the response is about to imply durability.

## Post-commit checks

After a durable write, cheaply verify:

- provider reported success;
- expected new global revision is available;
- active task continuity metadata is consistent with the committed task state;
- no pending durable change was silently discarded.

Routine post-commit checks do not require rereading full state/history.

## Repair behavior

Possible RepairPlan actions:

- re-anchor ActiveTask from newest observation + non-conflicting task state;
- patch META/ActiveTask consistency through PersistenceCoordinator;
- mark stale inventory uncertain;
- validate/rebuild derived lookup keys later;
- keep a failed durable change session-pending until storage recovers.

Do not tell the user “Doctor repaired the database.”

## Provider unavailable

If Drive is unavailable:

- downgrade continuity to session-only;
- keep the active cooking interaction moving when safe;
- avoid claiming cross-session save;
- do not repeatedly ask the user to reconnect while they are in the middle of a cooking action;
- retry/resolve persistence when it becomes relevant and low-friction.

## Long inactivity

Durable storage preserves records, not certainty.

After long inactivity:

- downgrade confidence for volatile/perishable inventory based on freshness evidence;
- keep stable equipment capability/preferences unless contradicted;
- ask only a task-relevant refresh question or invite a photo when old volatile state materially affects the decision.
