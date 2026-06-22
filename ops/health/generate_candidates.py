#!/usr/bin/env python3
"""Generate protected PEGO health directive candidates from a private baseline."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_INPUT = Path("private/health/baseline.json")
DEFAULT_OUTPUT = Path("private/directives/candidates/health-candidates.md")


@dataclass(frozen=True)
class Candidate:
    name: str
    duration: str
    energy: str
    location: str
    deadline: str
    benefit: str
    deferral: str
    dependencies: str
    stop: str


def minutes(value: object) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def list_text(values: object) -> str:
    if isinstance(values, list):
        return ", ".join(str(value) for value in values if str(value).strip()) or "None recorded"
    if isinstance(values, str) and values.strip():
        return values.strip()
    return "None recorded"


def has_medical_escalation(baseline: dict) -> bool:
    constraints = baseline.get("constraints", {})
    return bool(constraints.get("medical_constraints") or constraints.get("injuries"))


def metric_groups_with_values(baseline: dict) -> list[str]:
    groups = baseline.get("metrics", {})
    if not isinstance(groups, dict):
        return []
    present: list[str] = []
    for name, values in groups.items():
        if not isinstance(values, dict):
            continue
        if any(value not in ("", None, [], {}) for value in values.values()):
            present.append(str(name))
    return present


def measurement_rule(baseline: dict) -> str:
    policy = baseline.get("evidence_policy", {})
    rule = policy.get("measurement_rule")
    if isinstance(rule, str) and rule.strip():
        return rule.strip()
    return "Ask for new metrics only when they change a directive, risk classification, escalation, or strategy review."


def breakfast_candidate(baseline: dict) -> Candidate:
    defaults = baseline.get("preferences", {}).get("food_defaults", [])
    default_text = list_text(defaults)
    action = "Choose a protein/fiber breakfast default"
    if default_text != "None recorded":
        action = f"Eat one approved breakfast default: {default_text}"
    return Candidate(
        name="Breakfast Anchor",
        duration="10 min",
        energy="Low",
        location="Home",
        deadline="Morning",
        benefit="Stabilizes hunger and reduces sweet-trigger exposure.",
        deferral="Higher chance of reactive snacking or low-energy food decisions.",
        dependencies="Approved food default available.",
        stop="Stop if it conflicts with medical advice, nausea, allergy, or protected time.",
    )


def movement_candidate(baseline: dict) -> Candidate:
    availability = baseline.get("availability", {})
    preferences = baseline.get("preferences", {})
    morning = minutes(availability.get("morning_minutes"))
    midday = minutes(availability.get("midday_minutes"))
    evening = minutes(availability.get("evening_minutes"))
    available = max([morning, midday, evening, 10])
    duration = min(20, max(10, available))
    outside_ok = bool(availability.get("outside_ok", True))
    movement_preferences = list_text(preferences.get("movement_preferences", []))
    if movement_preferences != "None recorded":
        name = "Minimum Viable Movement"
        dependency = f"Use preferred low-friction movement if available: {movement_preferences}."
    elif outside_ok:
        name = "Walk Outside"
        dependency = "Weather and safe walking conditions."
    else:
        name = "Indoor Movement Block"
        dependency = "Clear indoor space."
    return Candidate(
        name=name,
        duration=f"{duration} min",
        energy="Low",
        location="Outside" if outside_ok else "Home",
        deadline="Before evening",
        benefit="Preserves physical capacity with low friction.",
        deferral="Movement remains at zero baseline and health momentum decays.",
        dependencies=dependency,
        stop="Stop if pain, injury risk, unsafe weather, or medical constraint appears.",
    )


def sweets_candidate(baseline: dict) -> Candidate:
    triggers = list_text(baseline.get("preferences", {}).get("sweet_triggers", []))
    return Candidate(
        name="Sweet Trigger Control",
        duration="5 min",
        energy="Low",
        location="Home",
        deadline="Before first snack window",
        benefit="Reduces automatic sweet consumption without relying on willpower.",
        deferral="Sweet-trigger loop remains unmanaged today.",
        dependencies=f"Known triggers: {triggers}.",
        stop="Stop if the rule becomes punitive or disrupts normal meals.",
    )


def sleep_candidate(baseline: dict) -> Candidate:
    return Candidate(
        name="Sleep Protection Check",
        duration="5 min",
        energy="Low",
        location="Home",
        deadline="Evening",
        benefit="Protects recovery and next-day execution capacity.",
        deferral="Late-day drift may reduce sleep quality and tomorrow's directive capacity.",
        dependencies="Known evening obligations.",
        stop="Stop if it conflicts with protected relationship time; reschedule instead.",
    )


def normalize_energy(value: str) -> str:
    normalized = value.strip().lower()
    if "high" in normalized:
        return "high"
    if "medium" in normalized:
        return "medium"
    return "low"


def normalize_location(value: str) -> str:
    normalized = value.strip().lower()
    if "outside" in normalized:
        return "outside"
    if "computer" in normalized:
        return "computer"
    if "phone" in normalized:
        return "phone"
    if "office" in normalized:
        return "office"
    if "errand" in normalized:
        return "errand"
    if "home" in normalized:
        return "home"
    return "other"


def build_candidates(baseline: dict) -> tuple[list[Candidate], list[str]]:
    candidates = [breakfast_candidate(baseline), movement_candidate(baseline), sweets_candidate(baseline), sleep_candidate(baseline)]
    escalations: list[str] = []
    if has_medical_escalation(baseline):
        escalations.append("Medical constraints or injuries are present; keep candidates Level 1 and avoid intensity increases without review.")
    metric_groups = metric_groups_with_values(baseline)
    if metric_groups:
        escalations.append("Health metrics present: use as context only unless clinician guidance exists. Groups: " + ", ".join(metric_groups) + ".")
    forbidden = baseline.get("constraints", {}).get("forbidden_directives", [])
    for forbidden_item in forbidden:
        escalations.append(f"Forbidden directive constraint recorded: {forbidden_item}")
    return candidates, escalations


def build_json_candidates(baseline: dict) -> list[dict]:
    candidates, _ = build_candidates(baseline)
    return [
        {
            "artifact_type": "directive_candidate",
            "schema_version": 1,
            "candidate": candidate.name,
            "domain": "health",
            "altitude": "directive",
            "proposed_action": candidate.name,
            "duration": candidate.duration,
            "timing": candidate.deadline,
            "energy_required": normalize_energy(candidate.energy),
            "location_required": normalize_location(candidate.location),
            "dependencies": [candidate.dependencies],
            "expected_benefit": candidate.benefit,
            "consequence_of_deferral": candidate.deferral,
            "protected_time_impact": "none",
            "authority_level": "level_1_recommend",
            "governance_status": "draft",
            "conflicts": [],
            "stop_condition": candidate.stop,
        }
        for candidate in candidates
    ]


def build_markdown(baseline: dict, output_date: str) -> str:
    candidates, escalations = build_candidates(baseline)
    metric_groups = metric_groups_with_values(baseline)
    evidence_summary = "Minimal reported baseline only."
    if metric_groups:
        evidence_summary = "Optional health metrics available: " + ", ".join(metric_groups) + "."
    rows = [
        f"| {candidate.name} | Health | {candidate.duration} | {candidate.energy} | {candidate.location} | {candidate.deadline} | Level 1 | Draft | {candidate.benefit} | {candidate.deferral} | None |"
        for candidate in candidates
    ]
    escalation_lines = [f"- {item}" for item in escalations] or ["- None."]
    stop_lines = [f"- {candidate.name}: {candidate.stop}" for candidate in candidates]
    dependency_lines = [f"- {candidate.name}: {candidate.dependencies}" for candidate in candidates]
    rule = measurement_rule(baseline)
    return "\n".join(
        [
            f"# Health Directive Candidates: {output_date}",
            "",
            "## Privacy Status",
            "",
            "Protected private instance.",
            "",
            "## Source",
            "",
            "private/health/baseline.json",
            "",
            "## Evidence Inputs",
            "",
            evidence_summary,
            "",
            "## Measurement Rule",
            "",
            rule,
            "",
            "## Candidate Table",
            "",
            "| Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Governance Status | Expected Benefit | Consequence of Deferral | Protected-Time Impact |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Dependencies",
            "",
            *dependency_lines,
            "",
            "## Stop Conditions",
            "",
            *stop_lines,
            "",
            "## Escalation Notes",
            "",
            *escalation_lines,
            "",
            "## Next Step",
            "",
            "Pass this file into directive synthesis. Do not treat candidates as medical advice or execution approval.",
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.input.is_file():
        raise SystemExit(f"missing health baseline: {args.input}")
    baseline = json.loads(args.input.read_text())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {args.output}")
    args.output.write_text(build_markdown(baseline, args.date))
    print(f"wrote: {args.output}")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        if args.json_output.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {args.json_output}")
        args.json_output.write_text(json.dumps(build_json_candidates(baseline), indent=2) + "\n")
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
