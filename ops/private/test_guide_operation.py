#!/usr/bin/env python3
"""Tests for safe PEGO operating guide generation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import guide_operation
import check_readiness


def create_required_paths(private_root: Path) -> None:
    for relative in check_readiness.REQUIRED_PATHS.values():
        path = private_root / relative
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic test content\n")
        else:
            path.mkdir(parents=True, exist_ok=True)


def test_missing_private_root_recommends_bootstrap() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "external-private"
        result = guide_operation.assess(private_root, backup_confirmed=False)

        assert result["artifact_type"] == "operating_guide"
        assert result["private_root"] == "external_private_root"
        assert result["storage_decision"] == "missing_private_root"
        assert result["next_step"]["command"].endswith("bootstrap")
        assert str(private_root) not in json.dumps(result)


def test_existing_private_root_recommends_persistent_backup_confirmation() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "external-private"
        private_root.mkdir()
        result = guide_operation.assess(private_root, backup_confirmed=False)

        assert result["storage_decision"] == "backup_not_confirmed"
        assert result["next_step"]["command"].endswith("storage --confirm-backup")
        assert str(private_root) not in json.dumps(result)


def test_ready_private_root_recommends_user_mode() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "external-private"
        create_required_paths(private_root)

        result = guide_operation.assess(private_root, backup_confirmed=True)

        assert result["readiness_decision"] == "ready"
        assert result["storage_decision"] == "backup_ready_manual"
        assert result["missing_check_count"] == 0
        assert "check-in" in result["next_step"]["command"]
        assert str(private_root) not in guide_operation.render_text(result)


def main() -> None:
    test_missing_private_root_recommends_bootstrap()
    test_existing_private_root_recommends_persistent_backup_confirmation()
    test_ready_private_root_recommends_user_mode()
    print("guide operation tests passed")


if __name__ == "__main__":
    main()
