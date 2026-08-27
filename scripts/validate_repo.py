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

    release = registry.get("release_candidate", {})
    if release.get("tracking_issue") != 7:
        fail("release_candidate.tracking_issue must be 7 during v0.8.1 hardening")
    if release.get("status") not in {"pending_composite_gate", "validated_release"}:
        fail("release_candidate.status must be pending_composite_gate or validated_release")


def check_deployments() -> None:
    path = ROOT / "dist" / "deployments.yaml"
    data = load_yaml(path)
    if not isinstance(data, dict):
        return
    deployments = data.get("deployments", {})
    required = {"pure_web", "web_google_drive_v08"}
    if set(deployments) != required:
        fail(f"Deployment identities must be exactly {sorted(required)}")
    for deployment in deployments.values():
        for key in ("entrypoint", "distribution"):
            value = deployment.get(key)
            if value:
                require_path(value, path)

    pure = deployments.get("pure_web", {})
    if pure.get("entrypoint") != "SKILL.md":
        fail("pure_web entrypoint must remain SKILL.md")

    durable = deployments.get("web_google_drive_v08", {})
    if durable.get("entrypoint") != "dist/KITCHEN_SKILL_WEB_GOOGLE_DRIVE_SHOPPING_COOKING_V08.md":
        fail("web_google_drive_v08 must point to the v0.8 bundle")


def check_pure_web_identity() -> None:
    root_skill = ROOT / "SKILL.md"
    dist_skill = ROOT / "dist" / "KITCHEN_SKILL_WEB_LIVE_COOKING.md"
    if root_skill.read_bytes() != dist_skill.read_bytes():
        fail("SKILL.md and Pure Web dist bundle are no longer identical")
    expected = "37a8d15bb376579a9a33ede514b121dff04c249d"
    actual = git_blob_sha(root_skill)
    if actual != expected:
        fail(f"Pure Web validated blob changed: expected {expected}, got {actual}")


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
        fail("Google Drive schema_version changed; release hardening must not perform a schema migration")
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


def check_release_files() -> None:
    required = [
        "docs/Kitchen_System_v0.8_Validated_Baseline.md",
        "tests/VALIDATION_REGISTRY.yaml",
        "dist/deployments.yaml",
        "tests/release/active_task_shape.yaml",
        "tests/release/manifest.yaml",
        "tests/release/01_current_head_composite_regression.md",
        "tests/release/expectations/01_current_head_composite_regression.md",
        "demo/RELEASE_SESSION_A_PROMPT.md",
        "demo/RELEASE_SESSION_B_PROMPT.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            fail(f"Required release-hardening file missing: {rel}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    stale_phrases = [
        "This v0.8 real long-history gate has not yet been executed",
        "must not be reported as passed",
    ]
    for phrase in stale_phrases:
        if phrase in readme:
            fail(f"README still contains stale validation status: {phrase}")


def main() -> int:
    check_machine_yaml_files()
    check_validation_registry()
    check_deployments()
    check_pure_web_identity()
    check_google_drive_store()
    check_domain_provider_separation()
    check_no_legacy_top_level_schema()
    check_release_active_task_shape()
    check_release_files()

    if ERRORS:
        print("STATIC VALIDATION: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("STATIC VALIDATION: PASS")
    print("- machine YAML/manifest references parse and resolve")
    print("- validation blob guards match tested baselines")
    print("- Pure Web fallback identity preserved")
    print("- Google Drive five-tab schema preserved")
    print("- Domain/provider separation preserved")
    print("- release ActiveTask harness shape is canonical")
    print("- release-hardening assets present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
