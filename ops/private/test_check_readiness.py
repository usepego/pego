#!/usr/bin/env python3
"""Smoke tests for protected private instance readiness checks."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import check_readiness


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("placeholder")


def mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def populate_ready_instance(root: Path) -> None:
    for relative in [
        "README.md",
        "active-operating-brief.md",
        "constitution/constitution.md",
        "current-state/current-state.md",
        "time/protected-time.md",
        "operator/operating-register.md",
    ]:
        touch(root / relative)
    for relative in [
        "directives/candidates",
        "directives/queues",
        "directives/command-responses",
        "operator/sessions",
        "outcomes/directives",
        "governance/preflight",
        "governance/reviews",
    ]:
        mkdir(root / relative)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "private"
        result = check_readiness.assess(root)
        if result["decision"] != "not_ready_missing_state":
            raise AssertionError(result)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "private"
        populate_ready_instance(root)
        output = Path(directory) / "readiness.json"
        result = check_readiness.main_with_args(
            ["--private-root", str(root), "--output", str(output)]
        )
        if result["decision"] != "ready":
            raise AssertionError(result)
        data = json.loads(output.read_text())
        if data["privacy"]["prints_private_contents"]:
            raise AssertionError(data)
        if data["checks"]["active_operating_brief"]["relative_path"] != "private/active-operating-brief.md":
            raise AssertionError(data)

    print("private readiness smoke tests passed.")


if __name__ == "__main__":
    main()
