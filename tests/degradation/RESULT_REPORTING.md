# Result Reporting Contract

The degradation runner must durably report one frozen evaluation to GitHub Issue #5 before cleanup.

The report must include TEST_COMMIT, valid store URL, dead-target evidence, criterion results, failure classes, D0-D3 frozen user-facing responses, provider-operation trace, D1 read-failure fallback evidence, D2 failed-write/pending-change/revision-integrity evidence, D3 retry/recovery evidence, and confirmation that evaluator expectations were unread until freeze.

PASS cleanup order:

1. write frozen result comment;
2. delete valid temporary Kitchen store;
3. verify provider returns unavailable/not-found;
4. append cleanup receipt;
5. close Issue #5 completed.

FAIL keeps the valid store for debugging and leaves Issue #5 open.
