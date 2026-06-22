#!/usr/bin/env python3
"""Review a protected PEGO directive outcome into a learning decision."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "outcome-review"


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.removeprefix("## ").strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def first_line(value: str, fallback: str = "Not supplied.") -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return fallback


def completion_key(completion: str) -> str:
    normalized = completion.lower()
    if "completed" in normalized and "partially" not in normalized and "not" not in normalized:
        return "completed"
    if "partially" in normalized or "partial" in normalized:
        return "partial"
    if "not completed" in normalized:
        return "not_completed"
    if "blocked" in normalized:
        return "blocked"
    if "canceled" in normalized or "cancelled" in normalized:
        return "canceled"
    return "unknown"


def has_real_content(value: str) -> bool:
    normalized = value.strip().lower()
    return bool(normalized) and normalized not in {
        "none",
        "none recorded.",
        "not supplied.",
        "no governance issue recorded.",
    }


def learning_decision(sections: dict[str, str]) -> str:
    key = completion_key(sections.get("Completion", ""))
    friction = has_real_content(sections.get("Friction", ""))
    benefit = has_real_content(sections.get("Benefit", ""))
    protected = sections.get("Protected-Time Impact", "").lower()
    governance = has_real_content(sections.get("Governance Notes", ""))
    if "medium" in protected or "high" in protected or governance:
        return "Escalate"
    if key == "completed" and benefit and not friction:
        return "Repeat"
    if key == "completed" and friction:
        return "Reduce"
    if key == "partial":
        return "Split"
    if key == "blocked":
        return "Block pending dependency"
    if key == "not_completed":
        return "Reschedule with smaller scope"
    if key == "canceled":
        return "Stop or defer"
    return "Gather more information"


def queue_implication(decision: str) -> str:
    if decision == "Repeat":
        return "Add follow-up candidate if recurrence is useful."
    if decision == "Reduce":
        return "Add smaller follow-up candidate."
    if decision == "Split":
        return "Split into smaller directive candidates."
    if decision == "Block pending dependency":
        return "Move candidate to blocked until dependency changes."
    if decision == "Reschedule with smaller scope":
        return "Defer original and add a smaller replacement candidate."
    if decision == "Stop or defer":
        return "Remove or defer until strategy changes."
    if decision == "Escalate":
        return "Escalate to governance review before repetition."
    return "Ask targeted question before queue synthesis."


def context_recommendation(decision: str, sections: dict[str, str]) -> str:
    friction = has_real_content(sections.get("Friction", ""))
    benefit = has_real_content(sections.get("Benefit", ""))
    if decision == "Repeat" and benefit:
        return "Record provisional pattern if repeated once more."
    if decision in {"Reduce", "Split", "Reschedule with smaller scope"} and friction:
        return "Record provisional execution-friction pattern."
    if decision == "Block pending dependency":
        return "Update operating register with blocker or dependency."
    if decision == "Escalate":
        return "Governance review before durable context change."
    return "No durable update yet."


def agent_routing(sections: dict[str, str]) -> str:
    explicit = sections.get("Agent Updates", "")
    if has_real_content(explicit) and "should ingest" not in explicit.lower():
        return explicit
    directive = sections.get("Directive Summary", "").lower()
    routes = ["Operations"]
    domain_keywords = [
        ("breakfast", "Health"),
        ("walk", "Health"),
        ("exercise", "Health"),
        ("garden", "Home and Environment"),
        ("weed", "Home and Environment"),
        ("yard", "Home and Environment"),
        ("venture", "Venture"),
        ("business", "Venture"),
        ("finance", "Finance"),
        ("money", "Finance"),
        ("spouse", "Relationships"),
        ("partner", "Relationships"),
    ]
    for keyword, route in domain_keywords:
        if keyword in directive and route not in routes:
            routes.append(route)
    return ", ".join(routes)


def governance_status(sections: dict[str, str]) -> str:
    protected = first_line(sections.get("Protected-Time Impact", "None"), "None")
    stakeholder = sections.get("Stakeholder Impact", "")
    governance = sections.get("Governance Notes", "")
    if protected in {"Medium", "High"} or has_real_content(stakeholder) or has_real_content(governance):
        return "Needs governance review before repetition or authority increase."
    return "Level 1 learning review; no authority increase approved."


def build_review(outcome_path: Path, review_date: str) -> str:
    sections = parse_sections(outcome_path.read_text())
    directive = first_line(sections.get("Directive Summary", ""), outcome_path.stem)
    completion = first_line(sections.get("Completion", ""), "Unknown")
    decision = learning_decision(sections)
    evidence = first_line(sections.get("Evidence", ""), "Human report.")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    return "\n".join(
        [
            f"# Outcome Review: {review_date} - {directive}",
            "",
            "## Date",
            "",
            review_date,
            "",
            "## Source Outcome",
            "",
            str(outcome_path),
            "",
            "## Directive",
            "",
            directive,
            "",
            "## Completion Class",
            "",
            completion,
            "",
            "## Evidence Summary",
            "",
            f"{happened} Evidence: {evidence}",
            "",
            "## Friction Summary",
            "",
            sections.get("Friction", "None recorded.") or "None recorded.",
            "",
            "## Benefit Summary",
            "",
            sections.get("Benefit", "None recorded.") or "None recorded.",
            "",
            "## Cost Summary",
            "",
            sections.get("Cost", "None recorded.") or "None recorded.",
            "",
            "## Learning Decision",
            "",
            decision,
            "",
            "## Queue Implication",
            "",
            queue_implication(decision),
            "",
            "## Context Update Recommendation",
            "",
            context_recommendation(decision, sections),
            "",
            "## Agent Routing",
            "",
            agent_routing(sections),
            "",
            "## Governance Status",
            "",
            governance_status(sections),
            "",
            "## Next Review",
            "",
            first_line(sections.get("Next Review", ""), "Next weekly review."),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--outcome", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.outcome.is_file():
        raise SystemExit(f"missing outcome file: {args.outcome}")
    output = args.output or (
        PRIVATE / "reviews" / "outcomes" / f"{args.date}-{slugify(args.outcome.stem)}.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_review(args.outcome, args.date))
    print(f"wrote: {output}")
    return output


if __name__ == "__main__":
    main_with_args()
