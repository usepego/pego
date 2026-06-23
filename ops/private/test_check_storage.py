#!/usr/bin/env python3
"""Smoke tests for private storage and backup readiness checks."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import check_storage


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "private"
        result = check_storage.assess(root, False, False)
        if result["decision"] != "missing_private_root":
            raise AssertionError(result)
        if result["privacy"]["prints_private_contents"]:
            raise AssertionError(result)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "private"
        root.mkdir()
        result = check_storage.assess(root, False, False)
        if result["decision"] != "backup_not_confirmed":
            raise AssertionError(result)
        if result["private_root"] != "external_private_root":
            raise AssertionError(result)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "private"
        root.mkdir()
        output = Path(directory) / "storage.json"
        result = check_storage.main_with_args(
            [
                "--private-root",
                str(root),
                "--backup-confirmed",
                "--output",
                str(output),
            ]
        )
        if result["decision"] != "backup_ready_manual":
            raise AssertionError(result)
        data = json.loads(output.read_text())
        if data["privacy"]["absolute_path_revealed"]:
            raise AssertionError(data)
        if data["git_tracking"]["tracked_private_paths"] != ["private/README.md"]:
            raise AssertionError(data)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "private"
        root.mkdir()
        result = check_storage.main_with_args(
            [
                "--private-root",
                str(root),
                "--confirm-backup",
                "--confirmed-at",
                "2026-06-23",
            ]
        )
        if result["decision"] != "backup_ready_manual":
            raise AssertionError(result)
        if not result["persisted_backup_confirmation"]:
            raise AssertionError(result)
        if str(root) in json.dumps(result):
            raise AssertionError(result)

        follow_up = check_storage.assess(root, False, False)
        if follow_up["decision"] != "backup_ready_manual":
            raise AssertionError(follow_up)
        if not follow_up["persisted_backup_confirmation"]:
            raise AssertionError(follow_up)

    print("private storage smoke tests passed.")


if __name__ == "__main__":
    main()
