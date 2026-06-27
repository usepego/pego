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
        "Outcome Progress": text_field("outcome_progress", "None recorded."),
        "Contentment Signal": text_field("contentment_signal", "Unknown"),
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


def dimension(rating: str, evidence: str, implication: str) -> dict[str, str]:
    return {
        "rating": rating,
        "evidence": evidence,
        "implication": implication,
    }


def fallback_section(sections: dict[str, str], name: str, fallback: str = "None recorded.") -> str:
    return sections.get(name, fallback) or fallback


def baseline_comparison(sections: dict[str, str]) -> str:
    governance = sections.get("Governance Notes", "").lower()
    evidence = sections.get("Evidence", "").lower()
    if "goal reconciliation" in governance or "goal reconciliation" in evidence:
        return "council_with_goal_reconciliation"
    if "council" in governance or "council" in evidence:
        return "council_without_goal_reconciliation"
    return "unknown"


def decision_quality_review(
    outcome_path: Path,
    review_date: str,
    sections: dict[str, str],
    decision: str,
    directive: str,
    completion: str,
) -> dict[str, object]:
    key = completion_key(completion)
    friction = has_real_content(sections.get("Friction", ""))
    benefit = has_real_content(sections.get("Benefit", ""))
    outcome_progress = has_real_content(sections.get("Outcome Progress", ""))
    contentment = sections.get("Contentment Signal", "Unknown")
    cost = has_real_content(sections.get("Cost", ""))
    governance = governance_status(sections)
    protected = first_line(sections.get("Protected-Time Impact", "None"), "None")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    evidence = first_line(sections.get("Evidence", ""), "Human report.")

    completed = key == "completed"
    partial_or_blocked = key in {"partial", "blocked", "not_completed"}
    escalated = decision == "Escalate"
    low_governance_concern = "Needs governance review" not in governance
    useful_outcome_evidence = benefit or outcome_progress

    dimensions = {
        "actionability": dimension(
            "strong" if completed else "adequate" if key == "partial" else "weak",
            f"Completion class: {completion}.",
            "Directive was executable as written."
            if completed
            else "Directive size, timing, or dependency should be revised.",
        ),
        "goal_fit": dimension(
            "strong" if useful_outcome_evidence else "unknown",
            (
                f"Benefit: {fallback_section(sections, 'Benefit')} "
                f"Outcome progress: {fallback_section(sections, 'Outcome Progress')}"
            ),
            "Benefit or outcome progress was visible enough to preserve the pattern."
            if useful_outcome_evidence
            else "Outcome did not prove goal fit; ask or inspect next evidence.",
        ),
        "constraint_fit": dimension(
            "strong" if low_governance_concern else "weak",
            governance,
            "Constraints fit the directive."
            if low_governance_concern
            else "Governance or protected-time constraints should dominate future synthesis.",
        ),
        "burden": dimension(
            "strong" if not cost and not friction else "adequate" if friction and not cost else "weak",
            f"Friction: {fallback_section(sections, 'Friction')} Cost: {fallback_section(sections, 'Cost')}",
            "Human burden appears acceptable."
            if not cost
            else "Reduce question load, scope, timing, or emotional cost.",
        ),
        "timeliness": dimension(
            "adequate" if key != "unknown" else "unknown",
            happened,
            "Timing produced reviewable evidence." if key != "unknown" else "Timing quality is unclear.",
        ),
        "risk_control": dimension(
            "strong" if low_governance_concern else "weak",
            f"Protected-time impact: {protected}. {governance}",
            "Risk controls were sufficient for repetition."
            if low_governance_concern
            else "Escalate or lower authority before repetition.",
        ),
        "explanation_quality": dimension(
            "unknown",
            "Directive outcome does not yet capture whether the reason helped.",
            "Add lightweight outcome prompt when explanation quality would change future directives.",
        ),
        "follow_through_probability": dimension(
            "strong" if completed and not friction else "adequate" if completed else "weak" if partial_or_blocked else "unknown",
            f"Completion: {completion}. Friction: {fallback_section(sections, 'Friction')}",
            "Similar directives are likely viable."
            if completed and not friction
            else "Future directives should reduce friction or change conditions.",
        ),
        "outcome_quality": dimension(
            "strong"
            if completed and useful_outcome_evidence and not escalated
            else "adequate"
            if completed or useful_outcome_evidence
            else "weak"
            if partial_or_blocked
            else "unknown",
            (
                f"Benefit: {fallback_section(sections, 'Benefit')} "
                f"Outcome progress: {fallback_section(sections, 'Outcome Progress')} "
                f"Contentment signal: {contentment}."
            ),
            "Decision produced useful outcome evidence."
            if completed or useful_outcome_evidence
            else "Decision did not yet produce enough progress.",
        ),
        "learning_value": dimension(
            "strong" if friction or useful_outcome_evidence or escalated else "adequate",
            f"Evidence: {evidence}",
            "Outcome should update agent recommendations or synthesis."
            if friction or useful_outcome_evidence or escalated
            else "Preserve as light evidence only.",
        ),
    }

    weak_count = sum(1 for item in dimensions.values() if item["rating"] == "weak")
    strong_count = sum(1 for item in dimensions.values() if item["rating"] == "strong")
    if weak_count >= 3 or escalated:
        overall = "poor_fit" if weak_count >= 3 else "mixed"
    elif strong_count >= 4 and completed:
        overall = "improved_decision_quality"
    elif key == "unknown":
        overall = "insufficient_evidence"
    else:
        overall = "mixed"

    if overall == "improved_decision_quality":
        adjustment = "Preserve the directive pattern and compare future repetitions against this outcome."
    elif escalated:
        adjustment = "Route future similar directives through governance before adoption."
    elif friction:
        adjustment = "Reduce scope, alter conditions, or ask the one missing fact that would remove friction."
    else:
        adjustment = "Collect better evidence on explanation quality, goal fit, and user burden before changing architecture."

    return {
        "artifact_type": "decision_quality_review",
        "schema_version": 1,
        "date": review_date,
        "source_outcome": str(outcome_path),
        "directive": directive,
        "completion_class": completion,
        "baseline_comparison": baseline_comparison(sections),
        "dimensions": dimensions,
        "human_burden": {
            "questions_asked": 0,
            "answer_burden": "unknown",
            "burden_notes": "Outcome capture does not yet track question count or answer burden directly.",
        },
        "overall_assessment": overall,
        "next_architecture_adjustment": adjustment,
        "review_notes": f"Decision quality inferred from outcome evidence. What happened: {happened}",
    }


def decision_quality_rows(review: dict[str, object]) -> list[str]:
    dimensions = review.get("dimensions", {})
    if not isinstance(dimensions, dict):
        return ["| Unknown | Unknown | No dimensions recorded. | No implication recorded. |"]
    rows = []
    for name, value in dimensions.items():
        if not isinstance(value, dict):
            continue
        label = name.replace("_", " ").title()
        rows.append(
            f"| {label} | {value.get('rating', 'unknown')} | {value.get('evidence', '')} | {value.get('implication', '')} |"
        )
    return rows or ["| Unknown | Unknown | No dimensions recorded. | No implication recorded. |"]


def build_review_artifact(outcome_path: Path, review_date: str) -> dict[str, object]:
    sections = read_outcome_sections(outcome_path)
    directive = first_line(sections.get("Directive Summary", ""), outcome_path.stem)
    completion = first_line(sections.get("Completion", ""), "Unknown")
    decision = learning_decision(sections)
    evidence = first_line(sections.get("Evidence", ""), "Human report.")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    quality = decision_quality_review(
        outcome_path,
        review_date,
        sections,
        decision,
        directive,
        completion,
    )
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
        "outcome_progress": sections.get("Outcome Progress", "None recorded.") or "None recorded.",
        "contentment_signal": first_line(sections.get("Contentment Signal", ""), "Unknown"),
        "cost_summary": sections.get("Cost", "None recorded.") or "None recorded.",
        "learning_decision": decision,
        "queue_implication": queue_implication(decision),
        "context_update_recommendation": context_recommendation(decision, sections),
        "agent_routing": agent_routing(sections),
        "governance_status": governance_status(sections),
        "decision_quality_review": quality,
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
            "## Outcome Progress",
            "",
            str(artifact["outcome_progress"]),
            "",
            "## Contentment Signal",
            "",
            str(artifact["contentment_signal"]),
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
            "## Decision Quality Review",
            "",
            "Baseline comparison: "
            + str(artifact["decision_quality_review"]["baseline_comparison"]),
            "",
            "| Dimension | Rating | Evidence | Implication |",
            "| --- | --- | --- | --- |",
            *decision_quality_rows(artifact["decision_quality_review"]),
            "",
            "## Human Burden",
            "",
            (
                f"Questions asked: {artifact['decision_quality_review']['human_burden']['questions_asked']}. "
                f"Answer burden: {artifact['decision_quality_review']['human_burden']['answer_burden']}. "
                f"{artifact['decision_quality_review']['human_burden']['burden_notes']}"
            ),
            "",
            "## Decision Quality Assessment",
            "",
            str(artifact["decision_quality_review"]["overall_assessment"]),
            "",
            "## Next Architecture Adjustment",
            "",
            str(artifact["decision_quality_review"]["next_architecture_adjustment"]),
            "",
            "## Decision Quality Notes",
            "",
            str(artifact["decision_quality_review"]["review_notes"]),
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
