# ruff: noqa: S101
"""Architectural boundary tests for API/OpenClaw integration usage."""

from __future__ import annotations

import re
from pathlib import Path


def test_api_does_not_import_openclaw_gateway_client_directly() -> None:
    """API modules should use OpenClaw services, not integration client imports."""
    repo_root = Path(__file__).resolve().parents[2]
    api_root = repo_root / "backend" / "app" / "api"

    violations: list[str] = []
    for path in api_root.rglob("*.py"):
        rel = path.relative_to(repo_root)
        for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            line = raw_line.strip()
            if line.startswith("from app.integrations.openclaw_gateway import "):
                violations.append(f"{rel}:{lineno}")
            elif line.startswith("import app.integrations.openclaw_gateway"):
                violations.append(f"{rel}:{lineno}")

    assert not violations, (
        "Import OpenClaw integration details via service modules (for example "
        "`app.services.openclaw.shared`) instead of directly from `app.api`. "
        f"Violations: {', '.join(violations)}"
    )


def test_api_uses_safe_gateway_dispatch_helper() -> None:
    """API modules should use `send_gateway_agent_message_safe`, not direct send."""
    repo_root = Path(__file__).resolve().parents[2]
    api_root = repo_root / "backend" / "app" / "api"
    direct_send_pattern = re.compile(r"\bsend_gateway_agent_message\b")

    violations: list[str] = []
    for path in api_root.rglob("*.py"):
        rel = path.relative_to(repo_root)
        for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            line = raw_line.strip()
            if not direct_send_pattern.search(line):
                continue
            if "send_gateway_agent_message_safe" in line:
                continue
            violations.append(f"{rel}:{lineno}")

    assert not violations, (
        "Use `send_gateway_agent_message_safe` from `app.services.openclaw.shared` "
        "for API-level gateway notification dispatch. "
        f"Violations: {', '.join(violations)}"
    )
