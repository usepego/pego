#!/usr/bin/env python3
"""Smoke tests for PEGO context update recorder."""

from __future__ import annotations

import tempfile
from pathlib import Path

import record_context_update


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private_root = root / "private"
        record_context_update.PRIVATE = private_root
        output = private_root / "context" / "updates" / "test.md"
        destination = private_root / "person" / "observations.md"
        record_context_update.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--title",
                "Synthetic Pattern",
                "--source",
                "Outcome",
                "--raw-observation",
                "Synthetic directive completed.",
                "--update-class",
                "Pattern",
                "--evidence-strength",
                "Directive outcome",
                "--stability",
                "Current but changeable",
                "--destination-file",
                str(destination),
                "--proposed-update",
                "Synthetic pattern should be remembered.",
                "--action",
                "Update destination",
                "--output",
                str(output),
                "--apply",
            ]
        )
        if "Synthetic directive completed" not in output.read_text():
            raise AssertionError(output.read_text())
        if "Synthetic pattern should be remembered" not in destination.read_text():
            raise AssertionError(destination.read_text())

    print("context update recorder smoke tests passed.")


if __name__ == "__main__":
    main()
