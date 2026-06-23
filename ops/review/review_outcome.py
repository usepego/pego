#!/usr/bin/env python3
"""Review a protected PEGO directive outcome into a learning decision."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


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


def read_outcome_sections(outcome_path: Path) -> dict[str, str]:
    text = outcome_path.read_text()
    if outcome_path.suffix == ".json":
        data = json.loads(text)
        if data.get("artifact_type") != "directive_outcome":
            raise SystemExit("json outcome must have artifact_type directive_outcome")
        return sections_from_json_outcome(data)
    return parse_sections(text)


def sections_from_json_outcome(data: dict[str, object]) -> dict[str, str]:
    def text_field(name: str, fallback: str = "") -> str:
        value = data.get(name, fallback)
        return str(value) if value is not None else fallback

    def list_field(name: str) -> str:
        value = data.get(name, [])
        if isinstance(value, list):
            return "\n".join(str(item) for item in value) or "None recorded."
        return str(value)

    completion = text_field("completion", "unknown").replace("_", " ").title()
    return {
        "Date": text_field("date"),
        "Source Directive": text_field("source_directive"),
        "Directive Summary": text_field("directive_summary"),
        "Completion": completion,
        "What Happened": text_field("what_happened", "Not supplied."),
        "Evidence": list_field("evidence"),
        "Friction": list_field("friction"),
        "Benefit": text_field("benefit", "None recorded."),
        "Cost": text_field("cost", "None recorded."),
        "Protected-Time Impact": text_field("protected_time_impact", "none").title(),
        "Stakeholder Impact": text_field("stakeholder_impact", "None recorded."),
        "Environment Impact": text_field("environment_impact", "None recorded."),
        "Follow-Up Directive Candidates": list_field("follow_up_directive_candidates"),
        "Agent Updates": list_field("agent_updates"),
        "Governance Notes": text_field("governance_notes", "None recorded."),
        "Next Review": text_field("next_review", "Next weekly review."),
    }


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


def build_review_artifact(outcome_path: Path, review_date: str) -> dict[str, object]:
    sections = read_outcome_sections(outcome_path)
    directive = first_line(sections.get("Directive Summary", ""), outcome_path.stem)
    completion = first_line(sections.get("Completion", ""), "Unknown")
    decision = learning_decision(sections)
    evidence = first_line(sections.get("Evidence", ""), "Human report.")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    return {
        "artifact_type": "outcome_review",
        "schema_version": 1,
        "date": review_date,
        "source_outcome": str(outcome_path),
        "directive": directive,
        "completion_class": completion,
        "evidence_summary": f"{happened} Evidence: {evidence}",
        "friction_summary": sections.get("Friction", "None recorded.") or "None recorded.",
        "benefit_summary": sections.get("Benefit", "None recorded.") or "None recorded.",
        "cost_summary": sections.get("Cost", "None recorded.") or "None recorded.",
        "learning_decision": decision,
        "queue_implication": queue_implication(decision),
        "context_update_recommendation": context_recommendation(decision, sections),
        "agent_routing": agent_routing(sections),
        "governance_status": governance_status(sections),
        "next_review": first_line(sections.get("Next Review", ""), "Next weekly review."),
    }


def build_review(outcome_path: Path, review_date: str) -> str:
    artifact = build_review_artifact(outcome_path, review_date)
    return "\n".join(
        [
            f"# Outcome Review: {review_date} - {artifact['directive']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Source Outcome",
            "",
            str(artifact["source_outcome"]),
            "",
            "## Directive",
            "",
            str(artifact["directive"]),
            "",
            "## Completion Class",
            "",
            str(artifact["completion_class"]),
            "",
            "## Evidence Summary",
            "",
            str(artifact["evidence_summary"]),
            "",
            "## Friction Summary",
            "",
            str(artifact["friction_summary"]),
            "",
            "## Benefit Summary",
            "",
            str(artifact["benefit_summary"]),
            "",
            "## Cost Summary",
            "",
            str(artifact["cost_summary"]),
            "",
            "## Learning Decision",
            "",
            str(artifact["learning_decision"]),
            "",
            "## Queue Implication",
            "",
            str(artifact["queue_implication"]),
            "",
            "## Context Update Recommendation",
            "",
            str(artifact["context_update_recommendation"]),
            "",
            "## Agent Routing",
            "",
            str(artifact["agent_routing"]),
            "",
            "## Governance Status",
            "",
            str(artifact["governance_status"]),
            "",
            "## Next Review",
            "",
            str(artifact["next_review"]),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--outcome", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    if not args.outcome.is_file():
        raise SystemExit(f"missing outcome file: {args.outcome}")
    output = args.output or (
        private / "reviews" / "outcomes" / f"{args.date}-{slugify(args.outcome.stem)}.md"
    )
    write_output(output, build_review(args.outcome, args.date), args.force)
    if args.json_output:
        artifact = build_review_artifact(args.outcome, args.date)
        write_output(
            args.json_output,
            json.dumps(artifact, indent=2, sort_keys=True) + "\n",
            args.force,
        )
    print(f"wrote: {output}")
    if args.json_output:
        print(f"wrote: {args.json_output}")
    return output


if __name__ == "__main__":
    main_with_args()
