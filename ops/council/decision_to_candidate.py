#!/usr/bin/env python3
"""Convert a PEGO council decision into a directive candidate."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


DEFAULT_OUTPUT = Path("private/directives/candidates/council-candidate.md")


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


def first_line(value: str, fallback: str = "") -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return fallback


def bullet_values(value: str) -> list[str]:
    values = []
    for line in value.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if stripped and stripped.lower() != "none.":
            values.append(stripped)
    return values


def read_decision(path: Path) -> dict[str, object]:
    text = path.read_text()
    if path.suffix == ".json":
        data = json.loads(text)
        if data.get("artifact_type") != "council_decision":
            raise SystemExit(f"not a council decision: {path}")
        return data

    sections = parse_sections(text)
    return {
        "artifact_type": "council_decision",
        "schema_version": 1,
        "date": first_line(sections.get("Date", ""), date.today().isoformat()),
        "decision_frame": first_line(sections.get("Decision Frame", ""), "Council decision."),
        "source_recommendations": bullet_values(sections.get("Source Recommendations", "")),
        "proposed_directive": first_line(sections.get("Proposed Directive", ""), ""),
        "council_outcome": first_line(sections.get("Council Outcome", ""), "request_more_information"),
        "rationale": sections.get("Rationale", ""),
        "expected_benefit": sections.get("Expected Benefit", ""),
        "key_risks": bullet_values(sections.get("Key Risks", "")),
        "dissent": bullet_values(sections.get("Dissent", "")),
        "required_handoffs": bullet_values(sections.get("Required Handoffs", "")),
        "governance_status": sections.get("Governance Status", ""),
        "stop_conditions": bullet_values(sections.get("Stop Conditions", "")),
        "next_action": first_line(sections.get("Next Action", ""), ""),
        "review": sections.get("Review", ""),
    }


def normalize_outcome(value: object) -> str:
    return str(value or "request_more_information").strip().lower().replace(" ", "_")


def candidate_for_decision(decision: dict[str, object], _source: Path) -> dict[str, object]:
    outcome = normalize_outcome(decision.get("council_outcome"))
    proposed = str(decision.get("proposed_directive") or "").strip()
    next_action = str(decision.get("next_action") or "").strip()
    risks = [str(item) for item in decision.get("key_risks", []) if str(item).strip()]
    handoffs = [str(item) for item in decision.get("required_handoffs", []) if str(item).strip()]
    stops = [str(item) for item in decision.get("stop_conditions", []) if str(item).strip()]

    if outcome == "adopt":
        action = proposed or next_action or "Execute adopted council directive."
        return {
            "artifact_type": "directive_candidate",
            "schema_version": 1,
            "candidate": action,
            "domain": "operations",
            "altitude": "directive",
            "proposed_action": action,
            "duration": "30 min",
            "timing": "Next feasible operating window",
            "energy_required": "medium",
            "location_required": "home",
            "dependencies": handoffs,
            "expected_benefit": str(decision.get("expected_benefit") or decision.get("rationale") or "Executes a council-approved directive."),
            "consequence_of_deferral": "Delays the council-approved next action.",
            "protected_time_impact": "none",
            "authority_level": "level_1_recommend",
            "governance_status": "reviewed",
            "conflicts": risks,
            "stop_condition": "; ".join(stops) or "Stop if new risk, dissent, or protected-time conflict appears.",
        }

    if outcome in {"revise", "request_more_information"}:
        action = next_action or "Resolve council decision before directive synthesis."
        label = "Revise council directive" if outcome == "revise" else "Answer council information request"
        return {
            "artifact_type": "directive_candidate",
            "schema_version": 1,
            "candidate": label,
            "domain": "governance",
            "altitude": "directive",
            "proposed_action": action,
            "duration": "15 min",
            "timing": "Before adopting the proposed directive",
            "energy_required": "medium",
            "location_required": "home",
            "dependencies": handoffs,
            "expected_benefit": str(decision.get("rationale") or "Clears council uncertainty before execution."),
            "consequence_of_deferral": "Prevents PEGO from safely converting the decision into an executable directive.",
            "protected_time_impact": "none",
            "authority_level": "level_1_recommend",
            "governance_status": "reviewed",
            "conflicts": risks,
            "stop_condition": "; ".join(stops) or "Stop if the answer reveals higher authority or privacy risk.",
        }

    action = next_action or "Escalate council decision for governance review."
    return {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": "Escalate council decision",
        "domain": "governance",
        "altitude": "directive",
        "proposed_action": action,
        "duration": "30 min",
        "timing": "Before execution",
        "energy_required": "medium",
        "location_required": "home",
        "dependencies": handoffs,
        "expected_benefit": str(decision.get("rationale") or "Prevents execution without required authority."),
        "consequence_of_deferral": "The underlying proposed directive remains blocked.",
        "protected_time_impact": "none",
        "authority_level": "level_4_escalate",
        "governance_status": "escalated",
        "conflicts": risks,
        "stop_condition": "; ".join(stops) or "Stop until governance explicitly clears the decision.",
    }


def display_domain(value: str) -> str:
    return {
        "operations": "Operations",
        "governance": "Governance",
    }.get(value, value)


def display_choice(value: str) -> str:
    return value.replace("_", " ").title()


def build_markdown(candidate: dict[str, object]) -> str:
    dependencies = [str(item) for item in candidate.get("dependencies", [])]
    conflicts = [str(item) for item in candidate.get("conflicts", [])]
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
            display_domain(str(candidate["domain"])),
            "",
            "## Altitude",
            "",
            display_choice(str(candidate["altitude"])),
            "",
            "## Proposed Action",
            "",
            str(candidate["proposed_action"]),
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
            display_choice(str(candidate["energy_required"])),
            "",
            "## Location Required",
            "",
            display_choice(str(candidate["location_required"])),
            "",
            "## Dependencies",
            "",
            *([f"- {item}" for item in dependencies] or ["- None."]),
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
            display_choice(str(candidate["protected_time_impact"])),
            "",
            "## Authority Level",
            "",
            display_choice(str(candidate["authority_level"])),
            "",
            "## Governance Status",
            "",
            display_choice(str(candidate["governance_status"])),
            "",
            "## Conflicts",
            "",
            *([f"- {item}" for item in conflicts] or ["- None."]),
            "",
            "## Stop Condition",
            "",
            str(candidate["stop_condition"]),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
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
    decision = read_decision(args.decision)
    candidate = candidate_for_decision(decision, args.decision)
    write_output(args.output, build_markdown(candidate), args.force)
    print(f"wrote: {args.output}")
    if args.json_output:
        write_output(args.json_output, json.dumps(candidate, indent=2, sort_keys=True) + "\n", args.force)
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
