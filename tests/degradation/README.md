# Provider Degradation Integration Gate

This suite is the reliability follow-up after the validated v0.7 Shopping -> canonical KitchenState -> fresh Cooking gate.

It does not add product behavior. It exercises already-documented degradation semantics in:

- `runtime/web_persistent.md`
- `persistence/web_durable.md`
- `health/web_google_drive.md`

The suite deliberately injects real Google Sheets connector failures outside DomainModules. A deleted sacrificial spreadsheet ID is used as a deterministic dead transport target for one read attempt and one write attempt while the valid Kitchen test store remains intact.

The required runner is:

- `demo/DEGRADATION_FAILURE_INJECTION_PROMPT.md`

Candidate script and evaluator expectations remain separated:

- `tests/degradation/01_provider_failure_and_recovery.md`
- `tests/degradation/expectations/01_provider_failure_and_recovery.md`

A PASS proves the current durable Web stack can degrade to session working state, avoid false durability claims, retain a failed semantic change, preserve valid-store revision integrity, and retry the pending change when the provider target is healthy again.
