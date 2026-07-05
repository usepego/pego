#!/usr/bin/env python3
"""Smoke tests for deterministic public release planning."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("public_release_plan.py")
SPEC = importlib.util.spec_from_file_location("public_release_plan", MODULE_PATH)
assert SPEC and SPEC.loader
release_plan = importlib.util.module_from_spec(SPEC)
sys.modules["public_release_plan"] = release_plan
SPEC.loader.exec_module(release_plan)


def test_allowlist() -> None:
    assert release_plan.is_public_release_file("README.md")
    assert release_plan.is_public_release_file("private/README.md")
    assert release_plan.is_public_release_file("ops/state/record_state_signal.py")
    assert release_plan.is_public_release_file("pego/schemas/state-signal.schema.json")
    assert release_plan.is_public_release_file(".github/workflows/pego-ci.yml")
    assert release_plan.is_public_release_file("src/usepego/cli.py")
    assert not release_plan.is_public_release_file("private/operator/session.md")
    assert not release_plan.is_public_release_file("src/other_package/cli.py")
    assert not release_plan.is_public_release_file(".env")


def test_name_status_parser() -> None:
    items = release_plan.parse_name_status(
        "M\tREADME.md\nA\tops/new.py\nR100\told.md\tpego/new.md\n"
    )
    assert [item.status for item in items] == ["M", "A", "R100"]
    assert [item.target for item in items] == ["README.md", "ops/new.py", "pego/new.md"]
    assert items[2].old_path == "old.md"


if __name__ == "__main__":
    test_allowlist()
    test_name_status_parser()
    print("public release planner smoke tests passed.")
