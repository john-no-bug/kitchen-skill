# Kitchen Skill — Public Web Bootstrap

**Purpose:** public distribution/bootstrap only. This file is intentionally small and is **not** the full Kitchen Skill implementation.

Repository: `john-no-bug/kitchen-skill`

Human-readable source:
`https://github.com/john-no-bug/kitchen-skill/blob/main/SKILL.md`

Raw machine-readable source:
`https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/SKILL.md`

## Distribution rule

Kitchen Skill must be usable without installing a skill package and without connecting the user's account to this GitHub repository.

**A GitHub connector is not required for normal use.** Use ordinary public web / browser / HTTP-fetch capability to read this bootstrap and the selected public bundle. GitHub connector access is only a development convenience for repository mutation and test-evidence writeback.

## Bootstrap protocol

1. Read the public deployment manifest:
   `https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/dist/deployments.yaml`
2. Detect capabilities actually available in the current host/runtime. Do not branch on subscription labels alone.
3. For normal use, select only a deployment whose status is `validated_release` or `validated_fallback` and whose runtime/storage requirements are actually available.
4. Ignore `integration_candidate`, experimental provider, and capability-probe assets unless the user explicitly asks to test them.
5. Fetch the selected deployment's `entrypoint` from the same public repository using:
   `https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/<entrypoint>`
6. Treat the fetched deployment bundle—not this bootstrap—as the active Kitchen Skill instructions for the task.
7. If no validated durable deployment matches the available provider, use the validated Pure Web fallback.

## Fallback transport

Preferred transport order:

1. ordinary public web / HTTP fetch;
2. installed skill/app copy, when the host supports it;
3. user-pasted or user-uploaded copy of the selected bundle.

If public-web access is unavailable or disabled by workspace policy, ask the user to paste/upload the selected public bundle. **Do not require them to connect GitHub.**

## Public artifact identity

The validated Pure Web artifact remains:
`dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md`

The validated Web + Google Drive artifact remains:
`dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md`

The deployment manifest is authoritative for current status. Experimental Notion capability probes are not production deployments.

## Test / developer note

Formal regression prompts may pin an exact commit and may optionally write evidence to GitHub Issues. Those are development harness behaviors, not end-user requirements. When GitHub write access is unavailable, a probe/test must return its complete report in the conversation so the developer can inspect it separately.
