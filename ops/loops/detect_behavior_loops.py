#!/usr/bin/env python3
"""Detect protected PEGO behavior loops from repeated operating evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


DOMAINS = {
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
}

AGENT_DOMAIN_MAP = {
    "Finance": "finance",
    "Health": "health",
    "Career": "career",
    "Venture": "venture",
    "Home": "home_environment",
    "Home and Environment": "home_environment",
    "Relationships": "relationships",
    "Exploration": "exploration",
    "Communications": "communications",
    "Happiness": "happiness",
    "Operations": "operations",
    "Governance": "governance",
}


@dataclass(frozen=True)
class LoopEvent:
    source: str
    domain: str
    trigger: str
    routine: str
    reward_or_relief: str
    strategic_effect: str
    evidence: str
    summary: str


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "behavior-loop"


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


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


def first_line(value: object, fallback: str = "") -> str:
    text = str(value or "")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return fallback


def has_real_content(value: object) -> bool:
    normalized = str(value or "").strip().lower()
    return bool(normalized) and normalized not in {
        "none",
        "none recorded.",
        "not supplied.",
        "unknown",
        "no material change",
    }


def infer_domain_from_text(value: object) -> str:
    text = str(value or "")
    for key in sorted(AGENT_DOMAIN_MAP, key=len, reverse=True):
        if key.lower() in text.lower():
            return AGENT_DOMAIN_MAP[key]
    return "operations"


def normalize_domain(value: object) -> str:
    text = str(value or "").strip().lower().replace(" ", "_").replace("-", "_")
    if text == "home":
        text = "home_environment"
    return text if text in DOMAINS else "operations"


def classify_trigger(text: str, directive: str = "") -> str:
    combined = f"{text} {directive}".lower()
    if any(word in combined for word in ["rain", "weather", "storm", "outside", "dry window"]):
        return "Weather or outdoor condition changes the feasible action"
    if any(word in combined for word in ["snack", "hunger", "food", "kitchen", "restaurant", "grocery"]):
        return "Food or hunger environment changes the default choice"
    if any(word in combined for word in ["calendar", "meeting", "time", "window", "late"]):
        return "Calendar pressure or missing time window appears"
    if any(word in combined for word in ["tired", "fatigue", "energy", "sleep"]):
        return "Low-energy state appears before the directive"
    if any(word in combined for word in ["app", "scroll", "media", "phone", "screen"]):
        return "App or media exposure creates an attention default"
    if any(word in combined for word in ["store", "route", "errand", "location"]):
        return "Location or route context changes the available default"
    words = [word for word in re.findall(r"[A-Za-z0-9]+", text) if len(word) > 2]
    return " ".join(words[:8]).capitalize() if words else "Repeated context changes the feasible action"


def routine_for_event(completion: str, trigger: str, directive: str) -> str:
    normalized = completion.lower()
    if "blocked" in normalized:
        return f"{directive or 'Planned directive'} stalls when {trigger.lower()}."
    if "not completed" in normalized or "partial" in normalized:
        return f"{directive or 'Planned directive'} loses momentum when {trigger.lower()}."
    if "food" in trigger.lower() or "hunger" in trigger.lower():
        return "The easier food default wins before a planned choice is made."
    if "app" in trigger.lower() or "media" in trigger.lower():
        return "Attention follows the available app or media default."
    return f"{directive or 'Planned directive'} becomes harder to execute under this condition."


def reward_for_trigger(trigger: str) -> str:
    lowered = trigger.lower()
    if "food" in lowered or "hunger" in lowered:
        return "Immediate convenience, relief, or satiety."
    if "app" in lowered or "media" in lowered:
        return "Immediate stimulation, rest, or avoidance of decision load."
    if "weather" in lowered or "calendar" in lowered or "energy" in lowered:
        return "Avoids immediate friction and preserves effort."
    return "Immediate relief from ambiguity or execution friction."


def strategic_effect(completion: str, friction: str, contentment: str = "") -> str:
    normalized = completion.lower()
    if "blocked" in normalized or "not completed" in normalized:
        return "works_against_strategy"
    if "partial" in normalized:
        return "mixed"
    if "less contentment" in contentment.lower():
        return "works_against_strategy"
    if has_real_content(friction):
        return "mixed"
    if "completed" in normalized:
        return "supports_strategy"
    return "unknown"


def event_from_outcome_review(path: Path) -> LoopEvent:
    data = read_json(path)
    if data and data.get("artifact_type") == "outcome_review":
        directive = str(data.get("directive", "Directive"))
        completion = str(data.get("completion_class", "Unknown"))
        friction = str(data.get("friction_summary", ""))
        contentment = str(data.get("contentment_signal", "Unknown"))
        domain = infer_domain_from_text(data.get("agent_routing", ""))
        trigger = classify_trigger(friction or str(data.get("evidence_summary", "")), directive)
        return LoopEvent(
            source=str(path),
            domain=domain,
            trigger=trigger,
            routine=routine_for_event(completion, trigger, directive),
            reward_or_relief=reward_for_trigger(trigger),
            strategic_effect=strategic_effect(completion, friction, contentment),
            evidence="repeated_outcome",
            summary=f"{completion}: {directive}. Friction: {friction or 'None recorded.'}",
        )

    sections = parse_sections(path.read_text())
    directive = first_line(sections.get("Directive"), path.stem)
    completion = first_line(sections.get("Completion Class"), "Unknown")
    friction = sections.get("Friction Summary", "")
    contentment = first_line(sections.get("Contentment Signal"), "Unknown")
    domain = infer_domain_from_text(sections.get("Agent Routing", ""))
    trigger = classify_trigger(friction or sections.get("Evidence Summary", ""), directive)
    return LoopEvent(
        source=str(path),
        domain=domain,
        trigger=trigger,
        routine=routine_for_event(completion, trigger, directive),
        reward_or_relief=reward_for_trigger(trigger),
        strategic_effect=strategic_effect(completion, friction, contentment),
        evidence="repeated_outcome",
        summary=f"{completion}: {directive}. Friction: {friction or 'None recorded.'}",
    )


def event_from_state_signal(path: Path) -> LoopEvent:
    data = read_json(path)
    if not data or data.get("artifact_type") != "state_signal":
        raise SystemExit(f"state signal must be JSON with artifact_type state_signal: {path}")
    domain = normalize_domain(data.get("domain", "operations"))
    summary = str(data.get("summary", "State signal recorded."))
    signal_type = str(data.get("signal_type", "other"))
    trigger = classify_trigger(summary, signal_type)
    routine = (
        f"{signal_type.replace('_', ' ')} recurs when {trigger.lower()}."
        if signal_type != "other"
        else f"Behavior recurs when {trigger.lower()}."
    )
    effect = "works_against_strategy" if signal_type in {"risk", "blocker"} else "unknown"
    evidence = "telemetry" if data.get("evidence_strength") == "direct_telemetry" else "human_report"
    return LoopEvent(
        source=str(path),
        domain=domain,
        trigger=trigger,
        routine=routine,
        reward_or_relief=reward_for_trigger(trigger),
        strategic_effect=effect,
        evidence=evidence,
        summary=summary,
    )


def group_key(event: LoopEvent) -> tuple[str, str]:
    return (event.domain, slugify(event.trigger))


def confidence_for_count(count: int, threshold: int, evidence_values: set[str]) -> str:
    if count < threshold:
        return "provisional"
    if count >= threshold + 2 or "telemetry" in evidence_values:
        return "strong"
    return "supported"


def status_for_confidence(confidence: str) -> str:
    return "active" if confidence in {"supported", "strong"} else "proposed"


def replacement_frame(trigger: str, domain: str) -> str:
    lowered = trigger.lower()
    if "weather" in lowered:
        return "Choose an indoor fallback or pre-stage the outdoor tool only when conditions are usable."
    if "food" in lowered or "hunger" in lowered:
        return "Stage the preferred food default before entering the food-choice environment."
    if "calendar" in lowered:
        return "Shrink the directive to the smallest useful action before the open window closes."
    if "energy" in lowered:
        return "Switch to the low-energy version before the directive is abandoned."
    if "app" in lowered or "media" in lowered:
        return "Change the app, device, or media default before attention drifts."
    if domain == "home_environment":
        return "Convert the visible condition into a small maintenance block before it becomes aversive."
    return "Change the environment or timing before the routine starts."


def disruption_directive(trigger: str, frame: str) -> str:
    return f"When {trigger.lower()}, use this operating default: {frame}"


def build_loop_artifact(
    events: list[LoopEvent],
    output_date: str,
    threshold: int,
) -> dict[str, object]:
    first = events[0]
    evidence_values = {event.evidence for event in events}
    confidence = confidence_for_count(len(events), threshold, evidence_values)
    evidence = "repeated_outcome" if len(events) >= threshold else first.evidence
    if "telemetry" in evidence_values and len(events) >= threshold:
        evidence = "telemetry"
    frame = replacement_frame(first.trigger, first.domain)
    return {
        "artifact_type": "behavior_loop",
        "schema_version": 1,
        "date": output_date,
        "loop": first.trigger,
        "domain": first.domain,
        "status": status_for_confidence(confidence),
        "confidence": confidence,
        "occurrence_count": len(events),
        "source_events": [event.source for event in events],
        "trigger": first.trigger,
        "routine": first.routine,
        "reward_or_relief": first.reward_or_relief,
        "strategic_effect": first.strategic_effect,
        "evidence": evidence,
        "replacement_frame": frame,
        "disruption_directive_candidate": disruption_directive(first.trigger, frame),
        "guardrails": [
            "Frame as environment design, not willpower.",
            "Keep the first disruption small and reversible.",
            "Escalate if the loop involves privacy, health, financial, legal, or relationship risk.",
        ],
        "authority_level": "level_1_recommend",
        "review_rule": "Review after the next trigger exposure or two additional outcomes.",
    }


def clean_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/").strip()


def bullet_rows(values: object) -> list[str]:
    items = values if isinstance(values, list) else []
    return [f"- {clean_cell(item)}" for item in items] or ["- None."]


def build_loop_markdown(artifact: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Behavior Loop: {artifact['loop']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Loop",
            "",
            str(artifact["loop"]),
            "",
            "## Domain",
            "",
            str(artifact["domain"]),
            "",
            "## Status",
            "",
            str(artifact["status"]),
            "",
            "## Confidence",
            "",
            str(artifact["confidence"]),
            "",
            "## Occurrence Count",
            "",
            str(artifact["occurrence_count"]),
            "",
            "## Source Events",
            "",
            *bullet_rows(artifact["source_events"]),
            "",
            "## Trigger",
            "",
            str(artifact["trigger"]),
            "",
            "## Routine",
            "",
            str(artifact["routine"]),
            "",
            "## Reward or Relief",
            "",
            str(artifact["reward_or_relief"]),
            "",
            "## Strategic Effect",
            "",
            str(artifact["strategic_effect"]),
            "",
            "## Evidence",
            "",
            str(artifact["evidence"]),
            "",
            "## Replacement Frame",
            "",
            str(artifact["replacement_frame"]),
            "",
            "## Disruption Directive Candidate",
            "",
            str(artifact["disruption_directive_candidate"]),
            "",
            "## Guardrails",
            "",
            *bullet_rows(artifact["guardrails"]),
            "",
            "## Authority Level",
            "",
            str(artifact["authority_level"]),
            "",
            "## Review Rule",
            "",
            str(artifact["review_rule"]),
            "",
        ]
    )


def location_for_domain(domain: str, trigger: str) -> str:
    lowered = trigger.lower()
    if "weather" in lowered or "outside" in lowered:
        return "outside"
    if domain in {"health", "home_environment", "happiness"}:
        return "home"
    if domain in {"career", "venture", "communications"}:
        return "computer"
    if domain == "relationships":
        return "phone"
    return "other"


def candidate_from_loop(artifact: dict[str, object]) -> dict[str, object]:
    return {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": f"Disrupt loop: {artifact['loop']}",
        "domain": artifact["domain"],
        "altitude": "directive",
        "proposed_action": artifact["disruption_directive_candidate"],
        "target_behavior": artifact["replacement_frame"],
        "environment_design": (
            f"Intercept trigger: {artifact['trigger']}. "
            f"Replacement frame: {artifact['replacement_frame']}"
        ),
        "duration": "5-15 min",
        "timing": "Next time the trigger appears",
        "energy_required": "low",
        "location_required": location_for_domain(str(artifact["domain"]), str(artifact["trigger"])),
        "dependencies": ["Trigger appears or is anticipated."],
        "expected_benefit": "The repeated loop is intercepted before the old routine starts.",
        "consequence_of_deferral": "PEGO may keep issuing directives that collide with the same trigger.",
        "protected_time_impact": "none",
        "authority_level": "level_1_recommend",
        "governance_status": "reviewed",
        "conflicts": [],
        "stop_condition": "Stop if the disruption adds stress, shame, protected-time conflict, or high-impact risk.",
    }


def build_candidate_markdown(candidate: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Directive Candidate: {candidate['candidate']}",
            "",
            "## Candidate",
            "",
            str(candidate["candidate"]),
            "",
            "## Domain",
            "",
            str(candidate["domain"]),
            "",
            "## Altitude",
            "",
            str(candidate["altitude"]),
            "",
            "## Proposed Action",
            "",
            str(candidate["proposed_action"]),
            "",
            "## Target Behavior",
            "",
            str(candidate["target_behavior"]),
            "",
            "## Environment Design",
            "",
            str(candidate["environment_design"]),
            "",
            "## Duration",
            "",
            str(candidate["duration"]),
            "",
            "## Timing",
            "",
            str(candidate["timing"]),
            "",
            "## Energy Required",
            "",
            str(candidate["energy_required"]),
            "",
            "## Location Required",
            "",
            str(candidate["location_required"]),
            "",
            "## Dependencies",
            "",
            *bullet_rows(candidate["dependencies"]),
            "",
            "## Expected Benefit",
            "",
            str(candidate["expected_benefit"]),
            "",
            "## Consequence of Deferral",
            "",
            str(candidate["consequence_of_deferral"]),
            "",
            "## Protected-Time Impact",
            "",
            str(candidate["protected_time_impact"]),
            "",
            "## Authority Level",
            "",
            str(candidate["authority_level"]),
            "",
            "## Governance Status",
            "",
            str(candidate["governance_status"]),
            "",
            "## Conflicts",
            "",
            *bullet_rows(candidate["conflicts"]),
            "",
            "## Stop Condition",
            "",
            str(candidate["stop_condition"]),
            "",
        ]
    )


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def output_path(private: Path, path: Path) -> str:
    try:
        relative = path.expanduser().resolve().relative_to(private.expanduser().resolve())
    except ValueError:
        return str(path)
    return private_root_config.framework_relative_private_path(private, str(relative))


def build_summary(
    output_date: str,
    loops: list[dict[str, object]],
    candidates: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "artifact_type": "behavior_loop_detection_summary",
        "schema_version": 1,
        "date": output_date,
        "loop_count": len(loops),
        "active_loop_count": sum(1 for loop in loops if loop.get("status") == "active"),
        "candidate_count": len(candidates),
        "loops": [
            {
                "loop": loop["loop"],
                "domain": loop["domain"],
                "status": loop["status"],
                "confidence": loop["confidence"],
                "occurrence_count": loop["occurrence_count"],
            }
            for loop in loops
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--outcome-review", action="append", type=Path, default=[])
    parser.add_argument("--state-signal", action="append", type=Path, default=[])
    parser.add_argument("--min-occurrences", type=int, default=2)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--durable-only", action="store_true")
    parser.add_argument("--include-provisional-candidates", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path | None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.min_occurrences < 1:
        raise SystemExit("--min-occurrences must be at least 1")
    private = private_root_config.resolve_private_root(args.private_root)
    output_dir = args.output_dir or private / "behavior-loops"
    candidate_dir = args.candidate_dir or private / "directives" / "candidates"
    summary_output = args.summary_output or private / "behavior-loops" / "detection-summary.json"

    events = [event_from_outcome_review(path) for path in args.outcome_review]
    events.extend(event_from_state_signal(path) for path in args.state_signal)
    if not events:
        raise SystemExit("at least one --outcome-review or --state-signal is required")

    grouped: dict[tuple[str, str], list[LoopEvent]] = {}
    for event in events:
        grouped.setdefault(group_key(event), []).append(event)

    loops = [
        build_loop_artifact(values, args.date, args.min_occurrences)
        for _, values in sorted(grouped.items(), key=lambda item: item[0])
    ]
    if args.durable_only:
        loops = [loop for loop in loops if loop["status"] == "active"]

    written_first: Path | None = None
    candidates: list[dict[str, object]] = []
    for loop in loops:
        slug = slugify(f"{loop['domain']}-{loop['loop']}")
        json_path = output_dir / f"{slug}.json"
        markdown_path = output_dir / f"{slug}.md"
        write_output(json_path, json.dumps(loop, indent=2, sort_keys=True) + "\n", args.force)
        write_output(markdown_path, build_loop_markdown(loop), args.force)
        written_first = written_first or json_path
        print(f"wrote: {output_path(private, markdown_path)}")
        print(f"wrote: {output_path(private, json_path)}")

        if loop["status"] == "active" or args.include_provisional_candidates:
            candidate = candidate_from_loop(loop)
            candidates.append(candidate)
            candidate_slug = slugify(f"behavior-loop-{loop['domain']}-{loop['loop']}")
            candidate_json = candidate_dir / f"{candidate_slug}.json"
            candidate_markdown = candidate_dir / f"{candidate_slug}.md"
            write_output(
                candidate_json,
                json.dumps(candidate, indent=2, sort_keys=True) + "\n",
                args.force,
            )
            write_output(candidate_markdown, build_candidate_markdown(candidate), args.force)
            print(f"wrote: {output_path(private, candidate_markdown)}")
            print(f"wrote: {output_path(private, candidate_json)}")

    summary = build_summary(args.date, loops, candidates)
    write_output(summary_output, json.dumps(summary, indent=2, sort_keys=True) + "\n", args.force)
    print(f"wrote: {output_path(private, summary_output)}")
    return written_first


if __name__ == "__main__":
    main_with_args()
