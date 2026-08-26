# Demo Session Prompt

Use the connected GitHub tool to test the repository `john-no-bug/kitchen-skill` as an automated regression harness.

You are the TEST ORCHESTRATOR, not the end-user kitchen assistant.

Follow the repository's `tests/manifest.yaml` exactly.

Important integrity rules:

1. Resolve the repository's current default-branch HEAD first and record the exact commit SHA under test. When the GitHub tool supports `ref`, fetch all candidate/test/evaluator files from that same commit so one run never mixes repository revisions. If the connector cannot pin reads to a commit, state that limitation explicitly and do not modify the repository while testing.
2. Read `README.md`, `tests/manifest.yaml`, and the candidate `SKILL.md` first.
3. During candidate generation, fetch only each candidate-visible test script. Do not fetch `tests/EVALUATION_RUBRIC.md` or any `tests/expectations/` file until all four candidate transcripts for that suite run are frozen.
4. Run three independent suite runs as specified by the manifest. Each test begins with fresh simulated task state unless its script says otherwise.
5. For each test, simulate the candidate kitchen assistant under the rules in `SKILL.md`. Feed every scripted user message sequentially and freeze the candidate response after every turn. Do not batch-answer a scenario and do not rewrite frozen responses later.
6. For the noise-stress test, actually generate and process 20 separate harmless noise turns; do not compress them into one synthetic message.
7. After a suite run's four transcripts are frozen, fetch its expectation files and `tests/EVALUATION_RUBRIC.md`, then score the combined suite evidence out of 36. Do not regenerate candidate responses after seeing evaluator-only material.
8. Report exact failing test/turns and classify failures using the manifest categories. Recommend the smallest patch that fixes the failed invariant; do not expand architecture unless necessary.
9. Check that files referenced by README/manifest exist and are internally consistent.
10. Do not modify `SKILL.md`, tests, or other production files during testing.
11. If GitHub issue creation is available, create one issue in the same repository titled `Regression report: Pure Web Live Cooking - YYYY-MM-DD` containing the tested commit SHA, three run scores, exact failures, minimal patch recommendations, repository defects, and testing limitations. Otherwise return that compact report in chat.
12. Explicitly state that this automated in-session simulation is a regression approximation and does not fully reproduce real host-level context truncation across actual ChatGPT/Claude/DeepSeek conversations.

Start immediately. Do not ask me to paste files, manually send test turns, choose test cases, or restate the repository contents.
