#!/usr/bin/env python3
"""Generate protected PEGO home/environment candidates from the operating register."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
DEFAULT_REGISTER = PRIVATE / "operator" / "operating-register.md"
DEFAULT_OUTPUT = PRIVATE / "directives" / "candidates" / "home-candidates.md"


@dataclass(frozen=True)
class Candidate:
    name: str
    target_behavior: str
    environment_design: str
    duration: str
    energy: str
    location: str
    deadline: str
    benefit: str
    deferral: str
    protected_time: str
    dependency: str
    governance: str


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_data_row(line: str) -> bool:
    return line.startswith("|") and "---" not in line


def parse_register_sections(text: str) -> dict[str, list[list[str]]]:
    sections: dict[str, list[list[str]]] = {}
    current = ""
    header: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.removeprefix("## ").strip()
            sections[current] = []
            header = None
            continue
        if not current or not is_data_row(line):
            continue
        cells = parse_table_cells(line)
        if not cells or cells[0] == "TBD":
            continue
        if header is None:
            header = cells
            continue
        if cells == header:
            continue
        sections[current].append(cells)
    return sections


def slug_name(value: str, fallback: str) -> str:
    value = value.strip()
    return value if value else fallback


def is_material_spend(action: str) -> bool:
    return bool(re.search(r"\b(buy|purchase|hire|contractor|renovat|replace|quote)\b", action.lower()))


def duration_for_action(action: str) -> str:
    if is_material_spend(action):
        return "15 min"
    if re.search(r"\bweed|clear|sweep|tidy|reset|water|prune|organize\b", action.lower()):
        return "20 min"
    return "25 min"


def governance_for(action: str) -> str:
    if is_material_spend(action):
        return "Draft; spending or contractor commitment requires governance review"
    return "Draft"


def watchlist_candidates(rows: list[list[str]]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in rows:
        area = slug_name(row[0] if len(row) > 0 else "", "Home area")
        condition = row[1] if len(row) > 1 else "Condition recorded"
        action = slug_name(row[2] if len(row) > 2 else "", f"Inspect {area}")
        dependency = row[3] if len(row) > 3 else "Weather, tool, or access if applicable"
        review = row[4] if len(row) > 4 else "This week"
        candidates.append(
            Candidate(
                name=f"{area}: {action}",
                target_behavior=f"Prompt visible maintenance before {area} becomes an avoidable irritation.",
                environment_design=f"Move attention to the specific area and condition early: {condition}.",
                duration=duration_for_action(action),
                energy="Medium-low",
                location="Outside" if any(word in area.lower() for word in ["yard", "garden", "exterior", "bed"]) else "Home",
                deadline=review,
                benefit=f"Improves or preserves home environment condition: {condition}.",
                deferral="Visible deterioration or avoidable irritation may increase.",
                protected_time="Low",
                dependency=dependency,
                governance=governance_for(action),
            )
        )
    return candidates


def annoyance_candidates(rows: list[list[str]]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in rows:
        annoyance = slug_name(row[0] if len(row) > 0 else "", "Recurring annoyance")
        domain = row[1] if len(row) > 1 else "Home and Environment"
        trigger = row[2] if len(row) > 2 else "Trigger recorded"
        action = slug_name(row[3] if len(row) > 3 else "", f"Reduce {annoyance}")
        cadence = row[4] if len(row) > 4 else "This week"
        if "home" not in domain.lower() and "environment" not in domain.lower() and "yard" not in domain.lower() and "garden" not in domain.lower():
            continue
        candidates.append(
            Candidate(
                name=f"{annoyance}: {action}",
                target_behavior=f"Interrupt the recurring annoyance loop before it becomes background stress.",
                environment_design=f"Change the trigger condition directly: {trigger}.",
                duration=duration_for_action(action),
                energy="Low",
                location="Home",
                deadline=cadence,
                benefit=f"Prevents recurring annoyance triggered by {trigger}.",
                deferral="Recurring annoyance likely returns and degrades the operating environment.",
                protected_time="Low",
                dependency="Access to affected area and any required supply.",
                governance=governance_for(action),
            )
        )
    return candidates


def supply_candidates(rows: list[list[str]]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in rows:
        supply = slug_name(row[0] if len(row) > 0 else "", "Home supply")
        domain = row[1] if len(row) > 1 else "Home"
        needed_for = row[2] if len(row) > 2 else "Home operation"
        consequence = row[3] if len(row) > 3 else "Scramble or blocked maintenance"
        action = slug_name(row[4] if len(row) > 4 else "", f"Add {supply} to purchase list")
        if "home" not in domain.lower() and "environment" not in domain.lower() and "yard" not in domain.lower() and "garden" not in domain.lower():
            continue
        candidates.append(
            Candidate(
                name=f"{supply}: {action}",
                target_behavior=f"Prevent a missing supply from blocking future home maintenance.",
                environment_design=f"Move the supply decision into the next errand or purchase-list context before the need becomes urgent.",
                duration="10 min",
                energy="Low",
                location="Phone/computer",
                deadline="Before next errand",
                benefit=f"Unblocks {needed_for}.",
                deferral=consequence,
                protected_time="None",
                dependency="Purchase list or supply source.",
                governance=governance_for(action),
            )
        )
    return candidates


def build_candidates(register_text: str) -> list[Candidate]:
    sections = parse_register_sections(register_text)
    candidates: list[Candidate] = []
    candidates.extend(watchlist_candidates(sections.get("Home and Environment Watchlist", [])))
    candidates.extend(annoyance_candidates(sections.get("Recurring Annoyances", [])))
    candidates.extend(supply_candidates(sections.get("Supply Gaps", [])))
    return candidates


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
    if "phone" in normalized:
        return "phone"
    if "computer" in normalized:
        return "computer"
    if "home" in normalized:
        return "home"
    return "other"


def normalize_impact(value: str) -> str:
    normalized = value.strip().lower()
    if "high" in normalized:
        return "high"
    if "medium" in normalized:
        return "medium"
    if "low" in normalized:
        return "low"
    return "none"


def normalize_governance(value: str) -> str:
    normalized = value.strip().lower()
    if "blocked" in normalized:
        return "blocked"
    if "escalat" in normalized:
        return "escalated"
    if "review" in normalized or "spending" in normalized or "contractor" in normalized:
        return "reviewed"
    return "draft"


def build_json_candidates(candidates: list[Candidate]) -> list[dict]:
    return [
        {
            "artifact_type": "directive_candidate",
            "schema_version": 1,
            "candidate": candidate.name,
            "domain": "home_environment",
            "altitude": "directive",
            "proposed_action": candidate.name,
            "target_behavior": candidate.target_behavior,
            "environment_design": candidate.environment_design,
            "duration": candidate.duration,
            "timing": candidate.deadline,
            "energy_required": normalize_energy(candidate.energy),
            "location_required": normalize_location(candidate.location),
            "dependencies": [candidate.dependency],
            "expected_benefit": candidate.benefit,
            "consequence_of_deferral": candidate.deferral,
            "protected_time_impact": normalize_impact(candidate.protected_time),
            "authority_level": "level_1_recommend",
            "governance_status": normalize_governance(candidate.governance),
            "conflicts": [],
            "stop_condition": "Stop if the work would disrupt protected time, another person's space, privacy, or household peace.",
        }
        for candidate in candidates
    ]


def build_markdown(candidates: list[Candidate], output_date: str, source: Path) -> str:
    rows = [
        f"| {candidate.name} | Home and Environment | {candidate.duration} | {candidate.energy} | {candidate.location} | {candidate.deadline} | Level 1 | {candidate.governance} | {candidate.benefit} | {candidate.deferral} | {candidate.protected_time} |"
        for candidate in candidates
    ]
    if not rows:
        rows = [
            "| Answer home environment question | Home and Environment | 5 min | Low | Home | Today | Level 1 | Draft | Identifies next environment friction. | PEGO may miss visible deterioration or avoidable irritation. | None |"
        ]
    dependencies = [f"- {candidate.name}: {candidate.dependency}" for candidate in candidates] or ["- No dependencies until a candidate is identified."]
    behavioral_lines = [
        f"- {candidate.name}: {candidate.target_behavior} Environment design: {candidate.environment_design}"
        for candidate in candidates
    ] or ["- No behavioral strategy until a candidate is identified."]
    return "\n".join(
        [
            f"# Home and Environment Candidates: {output_date}",
            "",
            "## Privacy Status",
            "",
            "Protected private instance.",
            "",
            "## Source",
            "",
            str(source),
            "",
            "## Candidate Table",
            "",
            "| Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Governance Status | Expected Benefit | Consequence of Deferral | Protected-Time Impact |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Behavioral Strategy",
            "",
            *behavioral_lines,
            "",
            "## Dependencies",
            "",
            *dependencies,
            "",
            "## Stop Conditions",
            "",
            "- Stop if the work would disrupt protected time, another person's space, privacy, or household peace.",
            "- Escalate major spending, contractor commitments, renovations, property decisions, or hard-to-reverse repairs.",
            "",
            "## Next Step",
            "",
            "Pass this file into directive synthesis. Do not treat candidate generation as approval for spending or disruption.",
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    register_text = args.register.read_text() if args.register.exists() else ""
    candidates = build_candidates(register_text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {args.output}")
    args.output.write_text(build_markdown(candidates, args.date, args.register))
    print(f"wrote: {args.output}")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        if args.json_output.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {args.json_output}")
        args.json_output.write_text(json.dumps(build_json_candidates(candidates), indent=2) + "\n")
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
