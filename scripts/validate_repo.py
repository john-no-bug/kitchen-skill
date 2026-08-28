#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as exc:
        fail(f"YAML parse failed: {path.relative_to(ROOT)}: {exc}")
        return None


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require_path(value: str, source: Path) -> None:
    if value.startswith(("http://", "https://")):
        return
    if any(ch.isspace() for ch in value):
        return
    allowed_prefixes = (
        "README.md",
        "SKILL.md",
        "core/",
        "demo/",
        "dist/",
        "docs/",
        "health/",
        "modules/",
        "persistence/",
        "providers/",
        "retrieval/",
        "runtime/",
        "schemas/",
        "scripts/",
        "tests/",
    )
    if not value.startswith(allowed_prefixes):
        return
    if not re.search(r"\.(md|yaml|yml|py)$", value):
        return
    candidate = ROOT / value
    if not candidate.exists():
        fail(f"Missing referenced path from {source.relative_to(ROOT)}: {value}")


def scan_references(obj, source: Path) -> None:
    if isinstance(obj, dict):
        for value in obj.values():
            scan_references(value, source)
    elif isinstance(obj, list):
        for value in obj:
            scan_references(value, source)
    elif isinstance(obj, str):
        require_path(obj, source)


def check_machine_yaml_files() -> None:
    for base in (ROOT / "tests", ROOT / "dist"):
        for path in sorted(base.rglob("*.yaml")):
            data = load_yaml(path)
            if data is not None:
                scan_references(data, path)


def check_validation_registry() -> None:
    path = ROOT / "tests" / "VALIDATION_REGISTRY.yaml"
    registry = load_yaml(path)
    if not isinstance(registry, dict):
        return

    gates = registry.get("validated_gates", {})
    if not gates:
        fail("Validation registry has no validated_gates")
        return

    for gate_name, gate in gates.items():
        if gate.get("status") != "validated":
            fail(f"Gate {gate_name} is not marked validated")
        for rel, expected in (gate.get("blob_guards") or {}).items():
            target = ROOT / rel
            if not target.exists():
                fail(f"Gate {gate_name} blob guard path missing: {rel}")
                continue
            actual = git_blob_sha(target)
            if actual != expected:
                fail(
                    f"Gate {gate_name} blob guard mismatch for {rel}: "
                    f"expected {expected}, got {actual}"
                )

    distribution = registry.get("distribution", {}).get("public_bootstrap", {})
    if distribution.get("entrypoint") != "SKILL.md":
        fail("distribution.public_bootstrap.entrypoint must be SKILL.md")
    if distribution.get("manifest") != "dist/deployments.yaml":
        fail("distribution.public_bootstrap.manifest must be dist/deployments.yaml")
    if distribution.get("connector_required") is not False:
        fail("Public bootstrap must not require a GitHub connector")

    release = registry.get("release_candidate", {})
    if release.get("tracking_issue") != 7:
        fail("release_candidate.tracking_issue must remain 7 for v0.8.1 validated release")
    if release.get("status") != "validated_release":
        fail("release_candidate.status must remain validated_release")

    notion_probe = registry.get("active_probes", {}).get("notion_plugin_conformance", {})
    if notion_probe.get("issue") != 9:
        fail("Notion plugin conformance probe must track Issue #9")
    if notion_probe.get("connector_required") is not False:
        fail("Notion capability probe must not require GitHub connector access")


def check_deployments() -> None:
    path = ROOT / "dist" / "deployments.yaml"
    data = load_yaml(path)
    if not isinstance(data, dict):
        return

    bootstrap = data.get("bootstrap", {})
    if bootstrap.get("entrypoint") != "SKILL.md":
        fail("Deployment bootstrap entrypoint must be SKILL.md")
    if bootstrap.get("selection_manifest") != "dist/deployments.yaml":
        fail("Bootstrap must select deployments through dist/deployments.yaml")
    if bootstrap.get("connector_required") is not False:
        fail("Deployment bootstrap must not require GitHub connector access")
    expected_raw = "https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/SKILL.md"
    if bootstrap.get("raw_url") != expected_raw:
        fail("Deployment bootstrap raw_url drifted")

    deployments = data.get("deployments", {})
    required = {"pure_web", "web_google_drive_v08"}
    if set(deployments) != required:
        fail(f"Validated deployment identities must be exactly {sorted(required)}")
    for deployment in deployments.values():
        for key in ("entrypoint", "distribution"):
            value = deployment.get(key)
            if value:
                require_path(value, path)

    pure = deployments.get("pure_web", {})
    pure_path = "dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md"
    if pure.get("entrypoint") != pure_path or pure.get("distribution") != pure_path:
        fail("pure_web must point directly to the validated Pure Web dist artifact")

    durable = deployments.get("web_google_drive_v08", {})
    if durable.get("entrypoint") != "dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md":
        fail("web_google_drive_v08 must point to the v0.8 durable bundle")


def check_public_bootstrap() -> None:
    path = ROOT / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) > 12000:
        fail("Public SKILL.md bootstrap grew too large; product logic belongs in dist bundles")
    required_markers = [
        "Public Web Bootstrap",
        "https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/dist/deployments.yaml",
        "A GitHub connector is not required for normal use",
        "user-pasted or user-uploaded copy",
        "dist/KITCHEN_SKILL_WEB_LIVE_COOKING.md",
    ]
    for marker in required_markers:
        if marker not in text:
            fail(f"Public bootstrap missing required marker: {marker}")


def check_pure_web_artifact_identity() -> None:
    dist_skill = ROOT / "dist" / "KITCHEN_SKILL_WEB_LIVE_COOKING.md"
    expected = "37a8d15bb376579a9a33ede514b121dff04c249d"
    actual = git_blob_sha(dist_skill)
    if actual != expected:
        fail(f"Pure Web validated artifact changed: expected {expected}, got {actual}")


def check_google_drive_store() -> None:
    path = ROOT / "schemas" / "google_drive_store.yaml"
    data = load_yaml(path)
    if not isinstance(data, dict):
        return
    store = data.get("GoogleDriveSheetStore", {})
    expected_tabs = {"META", "STATE", "ACTIVE_TASK", "EXPERIENCES", "EVENTS"}
    actual_tabs = set((store.get("tabs") or {}).keys())
    if actual_tabs != expected_tabs:
        fail(f"Google Drive tabs changed without an explicit migration: {sorted(actual_tabs)}")
    if store.get("file", {}).get("schema_version") != "0.6-drive-slice-1":
        fail("Google Drive schema_version changed; distribution work must not perform a schema migration")
    if store.get("file", {}).get("identity_marker", {}).get("store_format") != "kitchen-skill-google-sheets-v1":
        fail("Google Drive store_format changed")


def check_domain_provider_separation() -> None:
    forbidden_patterns = {
        "docs.google.com": re.compile(r"docs\.google\.com", re.I),
        "google drive provider": re.compile(r"GoogleDriveProvider", re.I),
        "google sheets api": re.compile(r"GoogleSheets|Google Sheets API", re.I),
        "spreadsheet connector api": re.compile(r"(?:batch_update|get|search)_spreadsheet", re.I),
        "provider module path": re.compile(r"providers/google_drive", re.I),
    }
    for path in sorted((ROOT / "modules").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for label, pattern in forbidden_patterns.items():
            if pattern.search(text):
                fail(f"Domain/provider separation violation ({label}) in {path.relative_to(ROOT)}")


def check_no_legacy_top_level_schema() -> None:
    forbidden_stems = {
        "cooking_session",
        "shopping_session",
        "working_snapshot",
        "checkpoint",
        "kitchen_capsule",
        "reminder_queue",
    }
    for path in (ROOT / "schemas").iterdir():
        if path.is_file() and path.stem.lower() in forbidden_stems:
            fail(f"Deprecated top-level schema object reintroduced: {path.name}")


def check_release_active_task_shape() -> None:
    path = ROOT / "tests" / "release" / "active_task_shape.yaml"
    data = load_yaml(path)
    if not isinstance(data, dict):
        return

    expected_allowed = {
        "meta", "type", "status", "goal", "phase", "state", "completed", "next",
        "open_issues", "related_recipe", "started_at", "updated_at",
    }
    expected_required = {"meta", "type", "status", "goal", "state"}
    expected_forbidden = {
        "ingredient_states", "equipment_state", "completed_milestones",
        "next_actions", "pan_state", "inventory_refs",
    }

    if data.get("source_contract") != "schemas/active_task.yaml":
        fail("Release ActiveTask fixture must derive from schemas/active_task.yaml")
    if set(data.get("allowed_top_level") or []) != expected_allowed:
        fail("Release ActiveTask allowed_top_level drifted from canonical contract")
    if set(data.get("required_top_level") or []) != expected_required:
        fail("Release ActiveTask required_top_level drifted from persisted release contract")
    if set(data.get("forbidden_module_specific_top_level") or []) != expected_forbidden:
        fail("Release ActiveTask forbidden top-level sentinel set changed")
    if set(data.get("required_meta_fields") or []) != {"id", "revision"}:
        fail("Release persisted ActiveTask must require meta.id and meta.revision")

    b_prompt = (ROOT / "demo" / "RELEASE_SESSION_B_PROMPT.md").read_text(encoding="utf-8")
    scenario = (ROOT / "tests" / "release" / "01_current_head_composite_regression.md").read_text(encoding="utf-8")
    required_markers = [
        "tests/release/active_task_shape.yaml",
        "ACTIVE_TASK_SHAPE_VALID: true",
        "state",
        "completed",
        "next",
    ]
    for marker in required_markers:
        if marker not in b_prompt:
            fail(f"Release Session B prompt missing canonical ActiveTask marker: {marker}")
    if "tests/release/active_task_shape.yaml" not in scenario:
        fail("Release scenario must bind Session B to active_task_shape.yaml")


def check_notion_probe_public_loading() -> None:
    raw_matrix = "https://raw.githubusercontent.com/john-no-bug/kitchen-skill/main/tests/notion/capability_matrix.yaml"
    for rel in ("demo/NOTION_WEB_CAPABILITY_PROMPT.md", "demo/NOTION_CODEX_CAPABILITY_PROMPT.md"):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if raw_matrix not in text:
            fail(f"Notion probe does not load public matrix URL: {rel}")
        if "GitHub connector is **not required**" not in text:
            fail(f"Notion probe still lacks explicit connector-free rule: {rel}")
        if "Always return one complete report in the conversation" not in text:
            fail(f"Notion probe must return report even without GitHub writeback: {rel}")


def check_required_files() -> None:
    required = [
        "SKILL.md",
        "docs/Kitchen_System_v0.8_Validated_Baseline.md",
        "docs/RELEASE_v0.8.1.md",
        "tests/VALIDATION_REGISTRY.yaml",
        "dist/deployments.yaml",
        "tests/release/active_task_shape.yaml",
        "tests/release/manifest.yaml",
        "tests/release/01_current_head_composite_regression.md",
        "tests/release/expectations/01_current_head_composite_regression.md",
        "tests/notion/capability_matrix.yaml",
        "demo/NOTION_WEB_CAPABILITY_PROMPT.md",
        "demo/NOTION_CODEX_CAPABILITY_PROMPT.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            fail(f"Required repository file missing: {rel}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required_readme_markers = [
        "Start without installing a skill or connecting GitHub",
        "Root `SKILL.md` is now intentionally a **small capability/distribution bootstrap**",
        "Notion capability/conformance",
    ]
    for marker in required_readme_markers:
        if marker not in readme:
            fail(f"README missing distribution/probe status marker: {marker}")


def main() -> int:
    check_machine_yaml_files()
    check_validation_registry()
    check_deployments()
    check_public_bootstrap()
    check_pure_web_artifact_identity()
    check_google_drive_store()
    check_domain_provider_separation()
    check_no_legacy_top_level_schema()
    check_release_active_task_shape()
    check_notion_probe_public_loading()
    check_required_files()

    if ERRORS:
        print("STATIC VALIDATION: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("STATIC VALIDATION: PASS")
    print("- machine YAML/manifest references parse and resolve")
    print("- validation blob guards match tested product baselines")
    print("- public SKILL.md bootstrap is connector-free and bounded")
    print("- validated Pure Web artifact identity preserved in dist")
    print("- Google Drive five-tab schema preserved")
    print("- Domain/provider separation preserved")
    print("- release ActiveTask harness shape is canonical")
    print("- Notion capability probes load public specs and return reports without GitHub write access")
    return 0


if __name__ == "__main__":
    sys.exit(main())
