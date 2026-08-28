# Public Distribution and Bootstrap Contract

## Goal

Kitchen Skill must be usable by a normal user without:

- installing a custom skill package;
- granting access to the developer's GitHub account/repository through a connector;
- having GitHub write permissions;
- running from the development/test harness.

The repository is public distribution storage, not user Kitchen storage.

## Public bootstrap

Primary machine-readable bootstrap:

`https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/SKILL.md`

Human-readable mirror:

`https://github.com/john-no-bug/kitchen-skill/blob/main/SKILL.md`

The bootstrap is deliberately small. It loads:

`https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/dist/deployments.yaml`

and then selects a validated deployment compatible with the current runtime/provider capabilities.

## Transport hierarchy

1. public web/browser/HTTP fetch;
2. installed skill/app copy when available;
3. user-pasted or user-uploaded public bundle.

GitHub connector access is not part of this hierarchy.

A runtime may expose no web/browser capability because of workspace/admin restrictions. In that case the user-supplied copy is the portability fallback.

## Artifact roles

- `SKILL.md` — bootstrap/router only.
- `dist/deployments.yaml` — machine-readable deployment status and entrypoints.
- `dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md` — validated Pure Web artifact.
- `dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md` — validated Web + Google Drive artifact.
- `demo/*` / `tests/*` — development and conformance harnesses, not normal runtime requirements.

## Validation rule

Product validation binds to the selected `dist/` artifact and its guarded Git blob identity. Root `SKILL.md` may evolve as distribution/bootstrap logic without invalidating an unchanged product artifact.

A bootstrap change must still pass static validation and must not silently modify guarded product files.

## Test/reporting rule

Test prompts may read public specifications by raw GitHub URL. If GitHub Issue write access is available in the developer environment, reports may be mirrored there. If it is unavailable, the complete report must be returned in the conversation.

No formal test may declare `harness_defect` merely because the tested user's runtime lacks the developer's GitHub connector, unless the test specifically targets GitHub integration itself.

## Example user startup instruction

> Read and follow the public Kitchen Skill bootstrap at https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/SKILL.md using ordinary web/HTTP access. Do not require a GitHub connector. Select only a validated deployment compatible with the capabilities available in this runtime.
