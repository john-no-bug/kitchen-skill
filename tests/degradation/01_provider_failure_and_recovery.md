# Degradation Acceptance Test 01 — Provider Failure and Recovery

Status: candidate-visible failure-injection script. Evaluator expectations live separately.

## Purpose

Exercise the existing Web durable degradation contract with a real Google Sheets connector failure while keeping fault injection outside domain logic.

The harness owns two isolated test artifacts:

- one valid Kitchen store used for baseline/recovery;
- one sacrificial native Sheet that is deleted immediately, leaving a known-dead spreadsheet ID used only to force deterministic connector 404s.

The dead ID is a test transport shunt. It must never become canonical Kitchen data or production provider configuration.

## D0 — establish a durable live task

User:

> 我在做番茄牛肉意面。牛肉已经铲散，锅里没明显积水，开始滋滋响，洋葱还没加。现在怎么做？

After the response, persist the compact Cooking ActiveTask to the valid test store and verify a successful durable revision.

## D1 — injected provider read failure

Before normal persistent bootstrap for this turn, the harness routes the provider read attempt to the known-dead sacrificial spreadsheet ID so the connector returns a real not-found/read failure.

User:

> 现在继续怎么做？

The domain response must be generated from current conversation/session working state. Do not repair or restore the provider until the D1 user-facing response is frozen.

After freeze, restore the valid test-store target. D1 need not create a semantic write if no new physical observation was supplied.

## D2 — injected provider write failure

With normal bounded reads restored against the valid store, process:

User:

> 现在牛肉已经有明显褐色了，洋葱我刚倒进去，有一点点粘锅。

Generate the candidate guidance and semantic change from this newest direct observation.

Immediately before the PersistenceCoordinator delegates the provider commit, the harness routes exactly that provider commit attempt to the known-dead sacrificial spreadsheet ID. The real connector call must fail.

Do not alter the valid Kitchen store during this injected failure.

Keep the failed semantic change session-pending for retry. Do not regenerate the D2 domain response after seeing the injected failure.

## D3 — provider recovery and pending retry

Restore the valid Kitchen store as the provider target.

Without inventing a new physical observation, retry the pending D2 semantic change through the normal PersistenceCoordinator/provider path after bounded refresh of META plus affected current records.

After retry succeeds, process:

User:

> 继续。

The response should continue from `beef browned + onion already added + slight sticking`, not from the pre-failure state.

## Store/evidence rules

- Candidate-phase retrieval stays bounded.
- Do not read full EVENTS/history for any D0-D3 response.
- Do not put fault-injection metadata into KitchenState/ActiveTask/Event canonical payloads.
- The valid store's revision must not advance because of the failed D2 write.
- The successful retry must advance revision and persist the newest D2 observation.
- Fault injection is harness behavior only; DomainModules never receive dead spreadsheet IDs or connector API details.
