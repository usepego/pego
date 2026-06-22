#!/usr/bin/env python3
"""Create a protected private PEGO instance skeleton.

The generated files live under private/. This script intentionally writes
generic placeholders only.
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
TEMPLATES = ROOT / "pego" / "templates"


FILES: dict[str, str] = {
    "constitution/onboarding.md": "onboarding.md",
    "constitution/constitution.md": "constitution.md",
    "current-state/current-state.md": "current-state.md",
    "person/profile.md": "person-profile.md",
    "happiness/model.md": "happiness-model.md",
    "time/protected-time.md": "protected-time.md",
    "governance/compliance-review-template.md": "compliance-review.md",
}


STATIC_FILES: dict[str, str] = {
    "README.md": """# Private PEGO Instance

This directory contains the protected private PEGO instance.

Do not commit private instance files.
""",
    "goals/README.md": """# Goals

Local private goals and goal strategies.
""",
    "directives/README.md": """# Directives

Local private PEGO directives.
""",
    "directives/daily/README.md": """# Daily Directives

Local private daily directive packets.
""",
    "directives/weekly/README.md": """# Weekly Directives

Local private weekly operating plans.
""",
    "directives/monthly/README.md": """# Monthly Directives

Local private monthly strategy reviews.
""",
    "directives/escalations/README.md": """# Escalations

Local private high-impact directive packets.
""",
    "finance/README.md": """# Finance

Local private financial summaries, scenario assumptions, and outputs.

Raw source files should remain under private/_local/finance/.
""",
    "career/README.md": """# Career

Local private career and work strategy.
""",
    "health/README.md": """# Health

Local private health baseline, directives, and reviews.
""",
    "telemetry/README.md": """# Telemetry

Local private telemetry sources and summaries.
""",
}


def write_file(path: Path, content: str, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    if existed and not force:
        return "skipped"
    path.write_text(content)
    return "written" if existed else "created"


def read_template(template_name: str) -> str:
    template_path = TEMPLATES / template_name
    return template_path.read_text()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite existing private files")
    args = parser.parse_args()

    results: list[tuple[str, str]] = []

    for relative_path, template_name in FILES.items():
        target = PRIVATE / relative_path
        content = read_template(template_name)
        status = write_file(target, content, args.force)
        results.append((relative_path, status))

    for relative_path, content in STATIC_FILES.items():
        target = PRIVATE / relative_path
        status = write_file(target, content, args.force)
        results.append((relative_path, status))

    (PRIVATE / "_local" / "finance").mkdir(parents=True, exist_ok=True)

    for relative_path, status in results:
        print(f"{status}: private/{relative_path}")

    print("ready: private/_local/finance")


if __name__ == "__main__":
    main()
