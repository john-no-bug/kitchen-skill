# Degradation Gate Test Plan

Tracking issue: GitHub Issue #5.

Run exactly one dedicated test conversation using:

`demo/DEGRADATION_FAILURE_INJECTION_PROMPT.md`

The runner will create and clean isolated Google Sheets test artifacts, execute D0-D3 sequentially, freeze candidate responses before reading evaluator expectations, write the full result to Issue #5, and close the issue only on a verified PASS cleanup.

No manual Kitchen-state entry or cross-session handoff is required for this gate.
