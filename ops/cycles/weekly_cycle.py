#!/usr/bin/env python3
"""Generate a protected PEGO weekly operating plan.

The weekly cycle reads protected private operating artifacts and writes a
protected weekly plan. It avoids printing private content; stdout is limited to the output
path.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


def read_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text()
    return ""


def count_files(path: Path, pattern: str = "*.md") -> int:
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))


def extract_register_questions(register_text: str, limit: int = 4) -> list[str]:
    questions: list[str] = []
    in_questions = False
    for line in register_text.splitlines():
        if line.startswith("## Questions to Ask"):
            in_questions = True
            continue
        if in_questions and line.startswith("## "):
            break
        if not in_questions or not line.startswith("|"):
            continue
        if "---" in line or "Question" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] and cells[0] != "TBD":
            questions.append(cells[0])
        if len(questions) >= limit:
            break
    return questions


def bullet_list(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def build_plan(args: argparse.Namespace) -> str:
    register_text = read_if_exists(args.register)
    questions = extract_register_questions(register_text)
    outcome_count = count_files(PRIVATE / "outcomes" / "directives")
    context_count = count_files(PRIVATE / "context" / "updates")

    return "\n".join(
        [
            f"# Weekly Operating Plan: {args.week}",
            "",
            "Status: Draft local weekly plan",
            "",
            "Authority level: Level 1, Recommend",
            "",
            "## Week",
            "",
            args.week,
            "",
            "## Weekly Thesis",
            "",
            args.thesis
            or "Convert recent outcomes, register items, and active goals into a bounded week of directives.",
            "",
            "## Governance Status",
            "",
            "Weekly priorities are recommendations unless separately reviewed. High-impact actions require decision packets.",
            "",
            "## Protected Time",
            "",
            args.protected_time
            or "Preserve protected time from the private protected-time rules. Do not expand PEGO tasks into protected time by default.",
            "",
            "## Review of Last Week",
            "",
            f"- Directive outcome records available: {outcome_count}",
            f"- Context update records available: {context_count}",
            "- Review private outcome details before increasing authority or recurrence.",
            "",
            "## Anticipation Scan",
            "",
            bullet_list(questions, "No operating-register questions available."),
            "",
            "## Primary Priority",
            "",
            args.primary_priority
            or "Select one strategic artifact or evidence action that advances the highest-leverage active goal.",
            "",
            "## Domain Priorities",
            "",
            "### Health",
            "",
            args.health_priority
            or "Maintain one low-friction food or movement default that can be repeated.",
            "",
            "### Finance",
            "",
            args.finance_priority
            or "Run or review finance scenarios only if a decision depends on updated assumptions. No execution authority is implied.",
            "",
            "### Career",
            "",
            args.career_priority
            or "Advance career or venture optionality through evidence, artifacts, or skill work without public commitment.",
            "",
            "### Relationships",
            "",
            args.relationships_priority
            or "Protect relationship and household constraints before scheduling discretionary PEGO work.",
            "",
            "### Exploration",
            "",
            args.exploration_priority
            or "Keep exploration bounded unless it directly supports a current goal or recovery need.",
            "",
            "## Daily Constraints",
            "",
            "- Daily directives should remain small.",
            "- Use `ops/cycles/daily_cycle.py next` for intra-day selection.",
            "- Record outcomes when directives complete, block, or fail.",
            "- Convert durable learning through context updates rather than chat memory.",
            "",
            "## Escalations",
            "",
            "- Escalate financial execution, career-risking moves, medical/legal/tax issues, privacy exposure, housing actions, or stakeholder-impacting actions.",
            "",
            "## Stop Conditions",
            "",
            "- Stop or resynthesize if protected time, privacy, health, stakeholder impact, or authority constraints change.",
            "",
            "## End-of-Week Review",
            "",
            "- What happened?",
            "- What failed?",
            "- What produced progress?",
            "- What produced drag?",
            "- What should PEGO change next week?",
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", default=date.today().isoformat())
    parser.add_argument("--register", type=Path, default=PRIVATE / "operator" / "operating-register.md")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--thesis", default="")
    parser.add_argument("--protected-time", default="")
    parser.add_argument("--primary-priority", default="")
    parser.add_argument("--health-priority", default="")
    parser.add_argument("--finance-priority", default="")
    parser.add_argument("--career-priority", default="")
    parser.add_argument("--relationships-priority", default="")
    parser.add_argument("--exploration-priority", default="")
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    output = args.output or PRIVATE / "directives" / "weekly" / f"{args.week}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_plan(args))
    print(f"wrote: {output}")
    return output


if __name__ == "__main__":
    main_with_args()
