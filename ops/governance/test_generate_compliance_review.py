#!/usr/bin/env python3
"""Smoke tests for PEGO compliance review generation."""

from __future__ import annotations

import tempfile
from pathlib import Path

import generate_compliance_review


DIRECTIVE = """# Synthetic Directive

Authority level: Level 2

Recommend a synthetic action after review.
"""


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        directive = root / "directive.md"
        output_root = root / "pego-private"
        directive.write_text(DIRECTIVE)

        result = generate_compliance_review.main_with_args(
            [
                "--private-root",
                str(output_root),
                "--directive",
                str(directive),
                "--date",
                "2026-06-23",
                "--slug",
                "synthetic-directive",
                "--force",
            ]
        )

        expected = output_root / "governance" / "reviews" / "2026-06-23-synthetic-directive.md"
        if result != expected:
            raise AssertionError(f"expected {expected}, got {result}")
        text = expected.read_text()
        if "Request more information" not in text:
            raise AssertionError(text)
        if "Level 2: Direct" not in text:
            raise AssertionError(text)
        if str(directive) not in text:
            raise AssertionError(text)

    print("compliance review smoke tests passed.")


if __name__ == "__main__":
    main()
