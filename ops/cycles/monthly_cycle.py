#!/usr/bin/env python3
"""Generate a protected PEGO monthly strategy review."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


AGENTS = [
    "finance",
    "health",
    "career",
    "venture",
    "home_environment",
    "relationships",
    "exploration",
    "communications",
    "happiness",
    "operations",
    "governance",
]


def count_files(path: Path, pattern: str = "*.md") -> int:
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))


def count_artifact_files(path: Path) -> int:
    if not path.exists():
        return 0
    return len(list(path.glob("*.md"))) + len(list(path.glob("*.json")))


def json_files(*paths: Path) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.exists():
            files.extend(sorted(path.glob("*.json")))
    return files


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text()


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def month_matches(data: dict[str, Any], path: Path, month: str) -> bool:
    value = data.get("month") or data.get("date")
    if value:
        return str(value).startswith(month)
    return path.stem.startswith(month)


def load_json_artifacts(
    *,
    month: str,
    artifact_type: str,
    paths: list[Path],
) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for path in json_files(*paths):
        data = read_json(path)
        if not data or data.get("artifact_type") != artifact_type:
            continue
        if not month_matches(data, path, month):
            continue
        data = dict(data)
        data["_source_path"] = str(path)
        artifacts.append(data)
    return artifacts


def counter_dict(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(value or "unknown" for value in values).items()))


def unique_ordered(values: list[str], limit: int | None = None) -> list[str]:
    output: list[str] = []
    seen = set()
    for value in values:
        cleaned = str(value).strip()
        if not cleaned or cleaned in seen:
            continue
        output.append(cleaned)
        seen.add(cleaned)
        if limit is not None and len(output) >= limit:
            break
    return output


def governance_item(source: str, item: str, severity: str = "medium") -> dict[str, str]:
    return {
        "source": source,
        "severity": severity,
        "item": item,
    }


def evidence_directive(source: str, directive: str, reason: str) -> dict[str, str]:
    return {
        "source": source,
        "directive": directive,
        "reason": reason,
    }


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


def count_summary(values: dict[str, int]) -> str:
    if not values:
        return "none"
    return ", ".join(f"{key}: {value}" for key, value in values.items())


def governance_item_lines(values: list[dict[str, str]]) -> list[str]:
    if not values:
        return ["- None recorded."]
    return [
        f"- [{item.get('severity', 'medium')}] {item.get('source', 'unknown')}: {item.get('item', '')}"
        for item in values
    ]


def evidence_directive_lines(values: list[dict[str, str]]) -> list[str]:
    if not values:
        return ["- None recorded."]
    return [
        f"- {item.get('directive', '')} Reason: {item.get('reason', '')}"
        for item in values
    ]


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


def collect_evidence(private: Path, month: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "outcome_reviews": load_json_artifacts(
            month=month,
            artifact_type="outcome_review",
            paths=[private / "reviews" / "outcomes"],
        ),
        "agent_calibration_records": load_json_artifacts(
            month=month,
            artifact_type="agent_calibration_record",
            paths=[private / "agents" / "calibration"],
        ),
        "goal_progress": load_json_artifacts(
            month=month,
            artifact_type="goal_progress",
            paths=[private / "goals" / "progress"],
        ),
        "behavior_loops": load_json_artifacts(
            month=month,
            artifact_type="behavior_loop",
            paths=[private / "behavior-loops"],
        ),
        "scenario_benchmarks": load_json_artifacts(
            month=month,
            artifact_type="scenario_benchmark",
            paths=[
                private / "evaluations" / "benchmarks",
                private / "evaluations" / "scenario-benchmarks",
                ROOT / "benchmarks",
            ],
        ),
    }


def nested_calibration_records(outcome_reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for review in outcome_reviews:
        for record in review.get("agent_calibration_records", []):
            if isinstance(record, dict) and record.get("artifact_type") == "agent_calibration_record":
                copied = dict(record)
                copied["_source_path"] = str(review.get("_source_path", "nested outcome review"))
                records.append(copied)
    return records


def decision_quality_summary(outcome_reviews: list[dict[str, Any]]) -> dict[str, Any]:
    quality_values = []
    learning_values = []
    council_reviews = []
    concerns = []
    for review in outcome_reviews:
        quality = review.get("decision_quality_review", {})
        if isinstance(quality, dict):
            quality_values.append(str(quality.get("overall_assessment", "unknown")))
        learning_values.append(str(review.get("learning_decision", "unknown")))
        council = review.get("council_synthesis_review")
        if isinstance(council, dict):
            council_reviews.append(council)
            governance_fit = council.get("governance_fit", {})
            if isinstance(governance_fit, dict) and governance_fit.get("rating") in {"weak", "missing"}:
                concerns.append(
                    f"Council governance fit needs review: {governance_fit.get('notes', 'No notes supplied.')}"
                )
        governance_status = str(review.get("governance_status", ""))
        if review.get("learning_decision") == "Escalate" or "Needs governance review" in governance_status:
            concerns.append(f"Outcome review requires governance attention: {governance_status}")

    council_outcomes = [
        str(item.get("review_outcome", "unknown"))
        for item in council_reviews
    ]
    return {
        "review_count": len(outcome_reviews),
        "council_review_count": len(council_reviews),
        "decision_quality_counts": counter_dict(quality_values),
        "learning_decision_counts": counter_dict(learning_values),
        "council_review_outcome_counts": counter_dict(council_outcomes),
        "concern_count": len(concerns),
        "concerns": unique_ordered(concerns, limit=8),
        "summary": (
            f"{len(outcome_reviews)} outcome reviews; {len(council_reviews)} include council synthesis review."
            if outcome_reviews
            else "No monthly outcome review artifacts were available."
        ),
    }


def calibration_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_agent: dict[str, dict[str, Any]] = {}
    cautions = []
    for record in records:
        agent = str(record.get("agent", "Unknown Agent"))
        entry = by_agent.setdefault(
            agent,
            {
                "record_count": 0,
                "score_delta_total": 0,
                "calibration_actions": Counter(),
                "missed_risks": Counter(),
            },
        )
        entry["record_count"] += 1
        entry["score_delta_total"] += int(record.get("score_delta", 0))
        entry["calibration_actions"].update([str(record.get("calibration_action", "unknown"))])
        entry["missed_risks"].update(str(value) for value in record.get("missed_risks", []))
        for caution in record.get("cautions", []):
            cautions.append(f"{agent}: {caution}")

    normalized_agents = {
        agent: {
            "record_count": entry["record_count"],
            "score_delta_total": entry["score_delta_total"],
            "calibration_actions": dict(sorted(entry["calibration_actions"].items())),
            "missed_risks": dict(sorted(entry["missed_risks"].items())),
        }
        for agent, entry in sorted(by_agent.items())
    }
    actions = counter_dict([str(record.get("calibration_action", "unknown")) for record in records])
    return {
        "record_count": len(records),
        "calibration_action_counts": actions,
        "agents": normalized_agents,
        "cautions": unique_ordered(cautions, limit=8),
        "summary": (
            f"{len(records)} agent calibration records across {len(normalized_agents)} agents."
            if records
            else "No monthly agent calibration records were available."
        ),
    }


def monthly_goal_status(progress_status: str, trajectory: str) -> str:
    if progress_status == "on_track" and trajectory == "improving":
        return "advanced"
    if progress_status == "on_track":
        return "stable"
    if progress_status == "stalled":
        return "stalled"
    if progress_status == "at_risk":
        return "regressed"
    return "needs_review"


def goal_progress_items(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    items = []
    for record in records:
        progress_status = str(record.get("progress_status", "unknown"))
        trajectory = str(record.get("trajectory", "unknown"))
        items.append(
            {
                "goal_id": str(record.get("goal_id", record.get("goal", "goal"))),
                "status": monthly_goal_status(progress_status, trajectory),
                "evidence": str(record.get("current_state_summary", "No summary supplied.")),
                "progress": f"{progress_status.replace('_', ' ')}; trajectory {trajectory}.",
                "friction": str(record.get("next_measurement_need", "No measurement need recorded.")),
                "next_adjustment": str(record.get("next_measurement_need", "Review next month.")),
            }
        )
    return items


def goal_progress_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    measurement_needs = []
    governance_notes = []
    for record in records:
        if record.get("confidence") == "low" or record.get("progress_status") in {"unknown", "at_risk", "stalled"}:
            measurement_needs.append(
                f"{record.get('domain', 'unknown')}: {record.get('next_measurement_need', 'Refresh goal evidence.')}"
            )
        for note in record.get("governance_notes", []):
            governance_notes.append(f"{record.get('domain', 'unknown')}: {note}")

    return {
        "record_count": len(records),
        "progress_status_counts": counter_dict([str(record.get("progress_status", "unknown")) for record in records]),
        "trajectory_counts": counter_dict([str(record.get("trajectory", "unknown")) for record in records]),
        "confidence_counts": counter_dict([str(record.get("confidence", "unknown")) for record in records]),
        "measurement_needs": unique_ordered(measurement_needs, limit=8),
        "governance_notes": unique_ordered(governance_notes, limit=8),
        "summary": (
            f"{len(records)} goal progress records available for monthly review."
            if records
            else "No monthly goal progress records were available."
        ),
    }


def behavior_loop_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    active = [
        f"{record.get('domain', 'unknown')}: {record.get('loop', 'unnamed loop')}"
        for record in records
        if record.get("status") == "active"
    ]
    disruptions = [
        str(record.get("disruption_directive_candidate", ""))
        for record in records
        if record.get("disruption_directive_candidate")
    ]
    return {
        "record_count": len(records),
        "active_loop_count": len(active),
        "status_counts": counter_dict([str(record.get("status", "unknown")) for record in records]),
        "strategic_effect_counts": counter_dict([str(record.get("strategic_effect", "unknown")) for record in records]),
        "active_loops": unique_ordered(active, limit=8),
        "disruption_directive_candidates": unique_ordered(disruptions, limit=8),
        "summary": (
            f"{len(records)} behavior loop records; {len(active)} active."
            if records
            else "No monthly behavior loop records were available."
        ),
    }


def scenario_benchmark_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    scenario_count = 0
    pego_wins = 0
    baseline_wins = 0
    ties = 0
    failure_modes = 0
    suites = []
    public_safe = True
    for record in records:
        summary = record.get("summary", {})
        if isinstance(summary, dict):
            scenario_count += int(summary.get("scenario_count", 0))
            pego_wins += int(summary.get("pego_wins", 0))
            baseline_wins += int(summary.get("baseline_wins", 0))
            ties += int(summary.get("ties", 0))
        failure_modes += len(record.get("failure_modes", []))
        suites.append(str(record.get("benchmark_suite", "unknown")))
        public_safe = public_safe and bool(record.get("public_safe", False))
    return {
        "record_count": len(records),
        "benchmark_suites": unique_ordered(suites),
        "scenario_count": scenario_count,
        "pego_wins": pego_wins,
        "baseline_wins": baseline_wins,
        "ties": ties,
        "failure_mode_count": failure_modes,
        "public_safe": public_safe if records else None,
        "summary": (
            f"{scenario_count} synthetic benchmark scenarios across {len(records)} benchmark artifacts."
            if records
            else "No monthly scenario benchmark artifacts were available."
        ),
    }


def build_governance_review_items(
    *,
    decision_quality: dict[str, Any],
    calibration: dict[str, Any],
    goal_progress: dict[str, Any],
    loops: dict[str, Any],
    benchmarks: dict[str, Any],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    items = [
        governance_item("manual", value, "medium")
        for value in split_values(args.constitution_concerns)
    ]
    items.extend(
        governance_item("decision_quality_summary", concern, "high")
        for concern in decision_quality.get("concerns", [])
    )
    for agent, summary in calibration.get("agents", {}).items():
        actions = summary.get("calibration_actions", {})
        if any(action in actions for action in ["decrease_weight", "quarantine", "escalate"]):
            items.append(
                governance_item(
                    "agent_calibration_summary",
                    f"Review {agent} calibration before increasing council weight.",
                    "medium",
                )
            )
    items.extend(
        governance_item("goal_progress_summary", note, "medium")
        for note in goal_progress.get("governance_notes", [])
    )
    if loops.get("active_loop_count", 0):
        items.append(
            governance_item(
                "behavior_loop_summary",
                "Active behavior loops should shape next-month directives before cadence increases.",
                "medium",
            )
        )
    if benchmarks.get("baseline_wins", 0):
        items.append(
            governance_item(
                "scenario_benchmark_summary",
                "Synthetic benchmark baseline win should trigger architecture review before public claims expand.",
                "medium",
            )
        )
    if benchmarks.get("public_safe") is False:
        items.append(
            governance_item(
                "scenario_benchmark_summary",
                "Benchmark artifact failed public-safety review.",
                "high",
            )
        )

    deduped = []
    seen = set()
    for item in items:
        key = (item["source"], item["severity"], item["item"])
        if key in seen:
            continue
        deduped.append(item)
        seen.add(key)
    return deduped


def build_evidence_gathering_directives(
    *,
    evidence: dict[str, list[dict[str, Any]]],
    goal_progress: dict[str, Any],
    benchmarks: dict[str, Any],
) -> list[dict[str, str]]:
    directives = []
    if not evidence["outcome_reviews"]:
        directives.append(
            evidence_directive(
                "outcome_reviews",
                "Capture at least one directive outcome review before changing monthly strategy.",
                "Decision quality cannot be assessed without reviewable outcomes.",
            )
        )
    if not evidence["agent_calibration_records"] and not nested_calibration_records(evidence["outcome_reviews"]):
        directives.append(
            evidence_directive(
                "agent_calibration_records",
                "Run outcome review with source recommendations or write calibration records for the most important agents.",
                "Agent weighting should not change without calibration evidence.",
            )
        )
    if not evidence["goal_progress"]:
        directives.append(
            evidence_directive(
                "goal_progress",
                "Create or refresh goal progress records for active domains.",
                "Monthly strategy needs goal trajectory, confidence, and indicators.",
            )
        )
    for need in goal_progress.get("measurement_needs", []):
        directives.append(
            evidence_directive(
                "goal_progress_summary",
                need,
                "A goal progress record has low confidence, unknown status, risk, or stale measurement.",
            )
        )
    if not evidence["behavior_loops"]:
        directives.append(
            evidence_directive(
                "behavior_loops",
                "Run behavior loop detection after enough outcome reviews or state signals exist.",
                "Repeated friction should be detected before next-month directives increase recurrence.",
            )
        )
    if not evidence["scenario_benchmarks"]:
        directives.append(
            evidence_directive(
                "scenario_benchmark_summary",
                "Run the synthetic scenario benchmark suite before expanding research-facing claims.",
                "Public claims need synthetic benchmark evidence and preserved failure modes.",
            )
        )
    elif benchmarks.get("baseline_wins", 0):
        directives.append(
            evidence_directive(
                "scenario_benchmark_summary",
                "Add or revise benchmark scenarios where PEGO did not beat the strongest baseline.",
                "Architecture review should learn from benchmark losses or ties.",
            )
        )
    return directives


def council_strategy_summary(
    *,
    decision_quality: dict[str, Any],
    calibration: dict[str, Any],
    goal_progress: dict[str, Any],
    loops: dict[str, Any],
    benchmarks: dict[str, Any],
    evidence_directives: list[dict[str, str]],
) -> dict[str, str]:
    posture = (
        "hold_strategy_and_gather_evidence"
        if evidence_directives
        else "eligible_for_agent_strategy_review"
    )
    return {
        "strategy_posture": posture,
        "decision_quality": str(decision_quality.get("summary", "")),
        "agent_calibration": str(calibration.get("summary", "")),
        "goal_progress": str(goal_progress.get("summary", "")),
        "behavior_loops": str(loops.get("summary", "")),
        "scenario_benchmarks": str(benchmarks.get("summary", "")),
        "council_use": (
            "Future councils should treat this monthly review as strategic context, not execution authority."
        ),
    }


def build_review(args: argparse.Namespace) -> dict:
    private = args.private_root_resolved
    register_questions = extract_register_questions(read_if_exists(args.register))
    counts = {
        "outcome_count": count_artifact_files(private / "outcomes" / "directives"),
        "review_count": count_artifact_files(private / "reviews" / "outcomes"),
        "session_review_count": count_artifact_files(private / "reviews" / "sessions"),
        "context_update_count": count_artifact_files(private / "context" / "updates"),
        "governance_review_count": count_artifact_files(private / "governance" / "reviews"),
        "preflight_count": count_files(private / "governance" / "preflight", "*.json"),
        "queue_count": count_artifact_files(private / "directives" / "queues"),
        "weekly_plan_count": count_artifact_files(private / "directives" / "weekly"),
    }
    evidence = collect_evidence(private, args.month)
    calibration_records = (
        evidence["agent_calibration_records"]
        + nested_calibration_records(evidence["outcome_reviews"])
    )
    decision_quality = decision_quality_summary(evidence["outcome_reviews"])
    calibration = calibration_summary(calibration_records)
    progress_summary = goal_progress_summary(evidence["goal_progress"])
    loop_summary = behavior_loop_summary(evidence["behavior_loops"])
    benchmark_summary = scenario_benchmark_summary(evidence["scenario_benchmarks"])
    evidence_directives = build_evidence_gathering_directives(
        evidence=evidence,
        goal_progress=progress_summary,
        benchmarks=benchmark_summary,
    )
    governance_items = build_governance_review_items(
        decision_quality=decision_quality,
        calibration=calibration,
        goal_progress=progress_summary,
        loops=loop_summary,
        benchmarks=benchmark_summary,
        args=args,
    )
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
    artifact["decision_quality_summary"] = decision_quality
    artifact["agent_calibration_summary"] = calibration
    artifact["goal_progress_summary"] = progress_summary
    artifact["behavior_loop_summary"] = loop_summary
    artifact["scenario_benchmark_summary"] = benchmark_summary
    artifact["governance_review_items"] = governance_items
    artifact["evidence_gathering_directives"] = evidence_directives
    artifact["council_strategy_summary"] = council_strategy_summary(
        decision_quality=decision_quality,
        calibration=calibration,
        goal_progress=progress_summary,
        loops=loop_summary,
        benchmarks=benchmark_summary,
        evidence_directives=evidence_directives,
    )
    artifact["goal_progress"] = goal_progress_items(evidence["goal_progress"]) or [
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
    artifact["constitution_concerns"] = split_values(args.constitution_concerns) or [
        item["item"] for item in governance_items if item["source"] == "manual"
    ]
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
    decision_quality = review["decision_quality_summary"]
    calibration = review["agent_calibration_summary"]
    progress_summary = review["goal_progress_summary"]
    loop_summary = review["behavior_loop_summary"]
    benchmark_summary = review["scenario_benchmark_summary"]
    council_context = review["council_strategy_summary"]
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
            "## Decision Quality Summary",
            "",
            str(decision_quality["summary"]),
            "",
            f"Decision quality counts: {count_summary(decision_quality['decision_quality_counts'])}",
            "",
            f"Learning decision counts: {count_summary(decision_quality['learning_decision_counts'])}",
            "",
            f"Council review outcomes: {count_summary(decision_quality['council_review_outcome_counts'])}",
            "",
            "Concerns:",
            "",
            *bullet_lines(decision_quality["concerns"]),
            "",
            "## Agent Calibration Summary",
            "",
            str(calibration["summary"]),
            "",
            f"Calibration actions: {count_summary(calibration['calibration_action_counts'])}",
            "",
            "Cautions:",
            "",
            *bullet_lines(calibration["cautions"]),
            "",
            "## Goal Progress Summary",
            "",
            str(progress_summary["summary"]),
            "",
            f"Progress statuses: {count_summary(progress_summary['progress_status_counts'])}",
            "",
            f"Trajectories: {count_summary(progress_summary['trajectory_counts'])}",
            "",
            f"Confidence: {count_summary(progress_summary['confidence_counts'])}",
            "",
            "Measurement Needs:",
            "",
            *bullet_lines(progress_summary["measurement_needs"]),
            "",
            "## Behavior Loop Summary",
            "",
            str(loop_summary["summary"]),
            "",
            f"Loop statuses: {count_summary(loop_summary['status_counts'])}",
            "",
            f"Strategic effects: {count_summary(loop_summary['strategic_effect_counts'])}",
            "",
            "Active Loops:",
            "",
            *bullet_lines(loop_summary["active_loops"]),
            "",
            "Disruption Directive Candidates:",
            "",
            *bullet_lines(loop_summary["disruption_directive_candidates"]),
            "",
            "## Scenario Benchmark Summary",
            "",
            str(benchmark_summary["summary"]),
            "",
            (
                f"Scenarios: {benchmark_summary['scenario_count']}; "
                f"PEGO wins: {benchmark_summary['pego_wins']}; "
                f"Baseline wins: {benchmark_summary['baseline_wins']}; "
                f"Ties: {benchmark_summary['ties']}; "
                f"Failure modes preserved: {benchmark_summary['failure_mode_count']}; "
                f"Public safe: {benchmark_summary['public_safe']}"
            ),
            "",
            "## Governance Review Items",
            "",
            *governance_item_lines(review["governance_review_items"]),
            "",
            "## Evidence Gathering Directives",
            "",
            *evidence_directive_lines(review["evidence_gathering_directives"]),
            "",
            "## Council Strategy Summary",
            "",
            f"Strategy posture: {council_context['strategy_posture']}",
            "",
            council_context["council_use"],
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
