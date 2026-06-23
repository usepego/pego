#!/usr/bin/env python3
"""Generate a protected PEGO monthly strategy review."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


AGENTS = [
    "finance",
    "health",
    "career",
    "relationships",
    "exploration",
    "happiness",
    "operations",
    "governance",
]


def count_files(path: Path, pattern: str = "*.md") -> int:
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text()


def extract_register_questions(register_text: str, limit: int = 5) -> list[str]:
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


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def bullet_lines(values: list[str], fallback: str = "None recorded.") -> list[str]:
    if not values:
        return [f"- {fallback}"]
    return [f"- {value}" for value in values]


def month_default() -> str:
    today = date.today()
    return f"{today.year:04d}-{today.month:02d}"


def agent_assessment(agent: str, counts: dict[str, int], args: argparse.Namespace) -> dict:
    missing_evidence = []
    if counts["outcome_count"] == 0:
        missing_evidence.append("No directive outcome records were available for the month.")
    if counts["review_count"] == 0:
        missing_evidence.append("No outcome review records were available for the month.")
    if counts["context_update_count"] == 0:
        missing_evidence.append("No context update records were available for the month.")

    if agent == "operations":
        learned = (
            f"Monthly evidence available: {counts['outcome_count']} outcomes, "
            f"{counts['review_count']} outcome reviews, {counts['queue_count']} queues."
        )
        continue_items = ["Keep daily directives small and review outcomes before increasing recurrence."]
        change_items = ["Use missing evidence to choose next month's measurement and review priorities."]
    elif agent == "governance":
        learned = (
            f"Governance evidence available: {counts['governance_review_count']} formal reviews "
            f"and {counts['preflight_count']} preflight outputs."
        )
        continue_items = ["Keep high-impact decisions behind decision packets and explicit review."]
        change_items = ["Escalate any repeated risk, privacy, protected-time, or authority ambiguity."]
    else:
        learned = "No domain-specific monthly assessment was supplied; treat this as a prompt for agent review."
        continue_items = ["Continue low-risk directives that produced evidence without protected-time conflict."]
        change_items = ["Request a targeted domain assessment before changing strategy materially."]

    return {
        "what_learned": learned,
        "continue": continue_items,
        "stop": ["Stop treating unevidenced assumptions as strategy."],
        "change": change_items,
        "missing_evidence": missing_evidence or ["Domain evidence should be reviewed before authority increases."],
        "dissent": args.dissent or "No dissent supplied; preserve agent dissent during the next council review.",
    }


def build_review(args: argparse.Namespace) -> dict:
    private = args.private_root_resolved
    register_questions = extract_register_questions(read_if_exists(args.register))
    counts = {
        "outcome_count": count_files(private / "outcomes" / "directives"),
        "review_count": count_files(private / "reviews" / "outcomes"),
        "session_review_count": count_files(private / "reviews" / "sessions"),
        "context_update_count": count_files(private / "context" / "updates"),
        "governance_review_count": count_files(private / "governance" / "reviews"),
        "preflight_count": count_files(private / "governance" / "preflight", "*.json"),
        "queue_count": count_files(private / "directives" / "queues"),
        "weekly_plan_count": count_files(private / "directives" / "weekly"),
    }
    outcome_summary = (
        f"Evidence counts only: {counts['outcome_count']} directive outcomes, "
        f"{counts['review_count']} outcome reviews, {counts['session_review_count']} session reviews, "
        f"{counts['context_update_count']} context updates, {counts['weekly_plan_count']} weekly plans."
    )
    artifact: dict = {
        "artifact_type": "monthly_strategy_review",
        "schema_version": 1,
        "month": args.month,
        "strategic_thesis": args.thesis
        or "Review whether PEGO is governing toward the right life before increasing next-month execution pressure.",
        "outcome_summary": outcome_summary,
    }
    artifact["goal_progress"] = [
        {
            "goal_id": "active-goals",
            "status": "needs_review",
            "evidence": "Monthly runner found private evidence counts but does not inspect private goal content.",
            "progress": args.goal_progress or "Review active private goal strategies before setting next-month priorities.",
            "friction": "Goal-level progress requires human or agent assessment of private goals.",
            "next_adjustment": "Run domain-agent reviews and update goal strategy only after evidence review.",
        }
    ]
    artifact["agent_assessments"] = {
        agent: agent_assessment(agent, counts, args) for agent in AGENTS
    }
    artifact["assumptions_revisited"] = [
        {
            "assumption": "Daily and weekly directives are producing enough evidence for monthly strategy review.",
            "status": "supported" if counts["outcome_count"] or counts["review_count"] else "unknown",
            "evidence": artifact["outcome_summary"],
            "next_test": "Increase outcome capture if evidence is too thin to govern next-month priorities.",
        }
    ]
    artifact["strategy_changes"] = split_values(args.strategy_changes) or [
        "Do not make major strategy changes from count-only evidence; request targeted agent assessments first."
    ]
    artifact["decision_packets_needed"] = split_values(args.decision_packets) or [
        "Create decision packets for any financial, career, health, relationship, privacy, housing, or hard-to-reverse change."
    ]
    artifact["constitution_concerns"] = split_values(args.constitution_concerns)
    artifact["next_month_priorities"] = split_values(args.next_month_priorities) or [
        "Produce enough directive outcomes and reviews to make next monthly strategy review evidence-based.",
        (register_questions[0] if register_questions else "Resolve the highest-leverage operating-register question before it becomes urgent."),
    ]
    artifact["stop_conditions"] = split_values(args.stop_conditions) or [
        "Stop and escalate if next-month priorities would affect protected time, privacy, health risk, stakeholder impact, or authority above Level 1.",
        "Stop if monthly evidence is too thin to justify a strategy change.",
    ]
    return artifact


def build_markdown(review: dict, register_questions: list[str]) -> str:
    assessments = []
    for agent in AGENTS:
        assessment = review["agent_assessments"][agent]
        assessments.extend(
            [
                f"### {agent.replace('_', ' ').title()}",
                "",
                assessment["what_learned"],
                "",
                "Continue:",
                *bullet_lines(assessment["continue"]),
                "",
                "Stop:",
                *bullet_lines(assessment["stop"]),
                "",
                "Change:",
                *bullet_lines(assessment["change"]),
                "",
                "Missing Evidence:",
                *bullet_lines(assessment["missing_evidence"]),
                "",
                "Dissent:",
                "",
                assessment["dissent"],
                "",
            ]
        )

    goal_rows = [
        f"| {item['goal_id']} | {item['status']} | {item['evidence']} | {item['progress']} | {item['friction']} | {item['next_adjustment']} |"
        for item in review["goal_progress"]
    ]
    assumption_rows = [
        f"| {item['assumption']} | {item['status']} | {item['evidence']} | {item['next_test']} |"
        for item in review["assumptions_revisited"]
    ]
    return "\n".join(
        [
            f"# Monthly Strategy Review: {review['month']}",
            "",
            "## Month",
            "",
            review["month"],
            "",
            "## Strategic Thesis",
            "",
            review["strategic_thesis"],
            "",
            "## Outcome Summary",
            "",
            review["outcome_summary"],
            "",
            "## Goal Progress",
            "",
            "| Goal | Status | Evidence | Progress | Friction | Next Adjustment |",
            "| --- | --- | --- | --- | --- | --- |",
            *goal_rows,
            "",
            "## Agent Assessments",
            "",
            *assessments,
            "## Assumptions Revisited",
            "",
            "| Assumption | Status | Evidence | Next Test |",
            "| --- | --- | --- | --- |",
            *assumption_rows,
            "",
            "## Register Questions",
            "",
            *bullet_lines(register_questions, "No operating-register questions available."),
            "",
            "## Strategy Changes",
            "",
            *bullet_lines(review["strategy_changes"]),
            "",
            "## Decision Packets Needed",
            "",
            *bullet_lines(review["decision_packets_needed"]),
            "",
            "## Constitution Concerns",
            "",
            *bullet_lines(review["constitution_concerns"]),
            "",
            "## Next Month Priorities",
            "",
            *bullet_lines(review["next_month_priorities"]),
            "",
            "## Stop Conditions",
            "",
            *bullet_lines(review["stop_conditions"]),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", default=month_default())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--register", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--thesis", default="")
    parser.add_argument("--goal-progress", default="")
    parser.add_argument("--strategy-changes", default="")
    parser.add_argument("--decision-packets", default="")
    parser.add_argument("--constitution-concerns", default="")
    parser.add_argument("--next-month-priorities", default="")
    parser.add_argument("--stop-conditions", default="")
    parser.add_argument("--dissent", default="")
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)
    print(f"wrote: {path}")


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.private_root_resolved = private
    args.register = args.register or private / "operator" / "operating-register.md"
    register_questions = extract_register_questions(read_if_exists(args.register))
    review = build_review(args)
    output = args.output or private / "directives" / "monthly" / f"{args.month}-strategy-review.md"
    json_output = args.json_output or private / "directives" / "monthly" / f"{args.month}-strategy-review.json"
    write_output(output, build_markdown(review, register_questions), args.force)
    write_output(json_output, json.dumps(review, indent=2, sort_keys=True) + "\n", args.force)
    return review


if __name__ == "__main__":
    main_with_args()
