#!/usr/bin/env python3
"""Synthesize protected PEGO directive candidates into one active queue."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


@dataclass(frozen=True)
class Candidate:
    name: str
    domain: str
    duration: str
    energy: str
    location: str
    deadline: str
    authority: str
    status: str
    benefit: str
    deferral: str
    target_behavior: str
    environment_design: str
    protected_time: str
    source: str


@dataclass(frozen=True)
class QueueBuild:
    active: list[Candidate]
    deferred: list[tuple[Candidate, str]]
    args: argparse.Namespace


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def is_table_data(line: str) -> bool:
    return line.startswith("|") and "---" not in line


def map_row(headers: list[str], cells: list[str]) -> dict[str, str]:
    mapped: dict[str, str] = {}
    for index, header in enumerate(headers):
        mapped[normalize_header(header)] = cells[index] if index < len(cells) else ""
    return mapped


def candidate_from_mapping(mapped: dict[str, str], source: str) -> Candidate | None:
    name = (
        mapped.get("candidate")
        or mapped.get("name")
        or mapped.get("proposed-action")
        or mapped.get("directive")
        or ""
    )
    if not name or name == "TBD":
        return None
    return Candidate(
        name=name,
        domain=mapped.get("domain", "Operations") or "Operations",
        duration=mapped.get("duration", mapped.get("time", "Unknown")) or "Unknown",
        energy=mapped.get("energy", mapped.get("energy-required", "Medium")) or "Medium",
        location=mapped.get("location", mapped.get("location-required", "Home")) or "Home",
        deadline=mapped.get("deadline", mapped.get("timing", "Today")) or "Today",
        authority=mapped.get("authority", mapped.get("authority-level", "Level 1")) or "Level 1",
        status=mapped.get("status", mapped.get("governance-status", "Draft")) or "Draft",
        benefit=mapped.get("expected-benefit", mapped.get("benefit", "")),
        deferral=mapped.get("consequence-of-deferral", mapped.get("deferral", "")),
        target_behavior=mapped.get("target-behavior", ""),
        environment_design=mapped.get("environment-design", ""),
        protected_time=mapped.get("protected-time-impact", "None") or "None",
        source=source,
    )


def display_domain(value: object) -> str:
    raw = str(value or "Operations").strip()
    return {
        "finance": "Finance",
        "health": "Health",
        "career": "Career",
        "venture": "Venture",
        "home_environment": "Home and Environment",
        "relationships": "Relationships",
        "exploration": "Exploration",
        "communications": "Communications",
        "happiness": "Happiness",
        "operations": "Operations",
        "governance": "Governance",
    }.get(raw, raw or "Operations")


def display_energy(value: object) -> str:
    raw = str(value or "Medium").strip().lower()
    return {
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }.get(raw, str(value or "Medium"))


def display_location(value: object) -> str:
    raw = str(value or "Home").strip().lower()
    return {
        "home": "Home",
        "office": "Office",
        "outside": "Outside",
        "errand": "Errand",
        "phone": "Phone",
        "computer": "Computer",
        "other": "Other",
    }.get(raw, str(value or "Home"))


def display_authority(value: object) -> str:
    raw = str(value or "level_1_recommend").strip().lower()
    return {
        "level_0_observe": "Level 0",
        "level_1_recommend": "Level 1",
        "level_2_direct": "Level 2",
        "level_3_execute": "Level 3",
        "level_4_escalate": "Level 4",
    }.get(raw, str(value or "Level 1"))


def display_status(value: object) -> str:
    raw = str(value or "draft").strip().lower()
    return {
        "draft": "Draft",
        "reviewed": "Reviewed",
        "approved_with_constraints": "Approved with constraints",
        "escalated": "Escalated",
        "blocked": "Blocked",
    }.get(raw, str(value or "Draft"))


def display_impact(value: object) -> str:
    raw = str(value or "none").strip().lower()
    return {
        "none": "None",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }.get(raw, str(value or "None"))


def parse_json_candidates(text: str, source: str) -> list[Candidate]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    items = data if isinstance(data, list) else [data]
    candidates: list[Candidate] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("artifact_type") != "directive_candidate":
            continue
        name = str(item.get("candidate") or item.get("proposed_action") or "").strip()
        if not name:
            continue
        dependencies = item.get("dependencies", [])
        dependency_text = ", ".join(str(value) for value in dependencies if str(value).strip())
        candidates.append(
            Candidate(
                name=name,
                domain=display_domain(item.get("domain")),
                duration=str(item.get("duration") or "Unknown"),
                energy=display_energy(item.get("energy_required")),
                location=display_location(item.get("location_required")),
                deadline=str(item.get("timing") or "Today"),
                authority=display_authority(item.get("authority_level")),
                status=display_status(item.get("governance_status")),
                benefit=str(item.get("expected_benefit") or ""),
                deferral=str(item.get("consequence_of_deferral") or ""),
                target_behavior=str(item.get("target_behavior") or ""),
                environment_design=str(item.get("environment_design") or ""),
                protected_time=display_impact(item.get("protected_time_impact")),
                source=source + (f" dependencies: {dependency_text}" if dependency_text else ""),
            )
        )
    return candidates


def parse_candidates_table(text: str, source: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    headers: list[str] | None = None
    for line in text.splitlines():
        if not is_table_data(line):
            continue
        cells = parse_table_cells(line)
        if not cells:
            continue
        normalized = [normalize_header(cell) for cell in cells]
        if any(key in normalized for key in {"candidate", "proposed-action", "directive"}):
            headers = cells
            continue
        if headers is None:
            continue
        candidate = candidate_from_mapping(map_row(headers, cells), source)
        if candidate:
            candidates.append(candidate)
    return candidates


def parse_heading_sections(text: str) -> dict[str, str]:
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


def parse_single_candidate(text: str, source: str) -> Candidate | None:
    sections = parse_heading_sections(text)
    name = (
        sections.get("Candidate")
        or sections.get("Candidate Directive")
        or sections.get("Proposed Action")
        or ""
    ).splitlines()[0:1]
    if not name:
        return None
    status = sections.get("Governance Status", "Draft").splitlines()[0]
    return Candidate(
        name=name[0],
        domain=(sections.get("Domain", "Operations").splitlines() or ["Operations"])[0],
        duration=(sections.get("Duration", "Unknown").splitlines() or ["Unknown"])[0],
        energy=(sections.get("Energy Required", "Medium").splitlines() or ["Medium"])[0],
        location=(sections.get("Location Required", "Home").splitlines() or ["Home"])[0],
        deadline=(sections.get("Timing", sections.get("Lead Time", "Today")).splitlines() or ["Today"])[0],
        authority=(sections.get("Authority Level", "Level 1").splitlines() or ["Level 1"])[0],
        status=status,
        benefit=sections.get("Expected Benefit", ""),
        deferral=sections.get("Consequence of Deferral", ""),
        target_behavior=sections.get("Target Behavior", ""),
        environment_design=sections.get("Environment Design", ""),
        protected_time=(sections.get("Protected-Time Impact", "None").splitlines() or ["None"])[0],
        source=source,
    )


def read_candidates(paths: list[Path]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for path in paths:
        text = path.read_text()
        parsed = parse_json_candidates(text, str(path))
        if not parsed:
            parsed = parse_candidates_table(text, str(path))
        if not parsed:
            single = parse_single_candidate(text, str(path))
            parsed = [single] if single else []
        candidates.extend(parsed)
    return candidates


def minutes_from_duration(duration: str) -> int:
    numbers = [int(match) for match in re.findall(r"\d+", duration)]
    if not numbers:
        return 30
    return min(numbers)


def risk_flags(candidate: Candidate) -> list[str]:
    flags: list[str] = []
    text = " ".join(
        [
            candidate.name,
            candidate.domain,
            candidate.authority,
            candidate.status,
            candidate.protected_time,
        ]
    ).lower()
    if "level 2" in text or "level 3" in text or "level 4" in text:
        flags.append("authority")
    if "escalat" in text or "blocked" in text:
        flags.append("governance")
    if "medium" in candidate.protected_time.lower() or "high" in candidate.protected_time.lower():
        flags.append("protected time")
    if any(word in text for word in ["medical", "legal", "tax", "quit", "relocation", "housing"]):
        flags.append("high impact")
    return flags


def candidate_score(candidate: Candidate) -> tuple[int, int, int]:
    flags = risk_flags(candidate)
    if flags:
        return (9, minutes_from_duration(candidate.duration), len(flags))
    domain_order = {
        "Health": 0,
        "Relationships": 1,
        "Home and Environment": 2,
        "Home": 2,
        "Venture": 3,
        "Career": 4,
        "Finance": 5,
        "Communications": 6,
        "Operations": 7,
        "Exploration": 8,
        "Happiness": 9,
    }
    consequence = candidate.deferral.lower()
    urgency = 0 if any(word in consequence for word in ["urgent", "scrambling", "delay", "friction"]) else 1
    return (urgency, domain_order.get(candidate.domain, 6), minutes_from_duration(candidate.duration))


def is_active(candidate: Candidate, available_minutes: int | None) -> bool:
    if risk_flags(candidate):
        return False
    if available_minutes is not None and minutes_from_duration(candidate.duration) > available_minutes:
        return False
    return True


def build_queue(
    candidates: list[Candidate],
    args: argparse.Namespace,
) -> QueueBuild:
    active: list[Candidate] = []
    deferred: list[tuple[Candidate, str]] = []

    for candidate in sorted(candidates, key=candidate_score):
        flags = risk_flags(candidate)
        if flags:
            deferred.append((candidate, "Needs governance review: " + ", ".join(flags)))
            continue
        if args.available is not None and minutes_from_duration(candidate.duration) > args.available:
            deferred.append((candidate, f"Does not fit available window of {args.available} minutes"))
            continue
        active.append(candidate)

    return QueueBuild(active=active, deferred=deferred, args=args)


def build_markdown_queue(queue: QueueBuild) -> str:
    args = queue.args
    active_rows = []
    for rank, candidate in enumerate(queue.active, start=1):
        active_rows.append(
            f"| {rank} | {candidate.name} | {candidate.domain} | {candidate.duration} | {candidate.energy} | {candidate.location} | {candidate.deadline} | {candidate.authority} | Ready |"
        )
    if not active_rows:
        active_rows.append("| 1 | Answer targeted operating question | Operations | 5 min | Low | Home | Now | Level 1 | Ready |")

    deferred_rows = [
        f"| {candidate.name} | {reason} | Next synthesis |" for candidate, reason in queue.deferred
    ]
    if not deferred_rows:
        deferred_rows.append("| None | No deferred candidates | Next synthesis |")

    strategy_rows = []
    for rank, candidate in enumerate(queue.active, start=1):
        target = candidate.target_behavior or "Not specified."
        environment = candidate.environment_design or "Not specified."
        strategy_rows.append(f"| {rank} | {candidate.name} | {target} | {environment} |")
    if not strategy_rows:
        strategy_rows.append("| 1 | Answer targeted operating question | Identify the missing decision-grade fact. | Create enough context to resynthesize safely. |")

    state_lines = [
        f"- Time: {args.time or 'Unknown'}",
        f"- Location: {args.location or 'Unknown'}",
        f"- Energy: {args.energy or 'Unknown'}",
        f"- Weather/environment: {args.environment or 'Unknown'}",
        f"- Active obligations: {args.obligations or 'Unknown'}",
        f"- Known constraints: {args.constraints or 'Unknown'}",
    ]

    return "\n".join(
        [
            f"# Directive Queue: {args.date}",
            "",
            "## Date or Session",
            "",
            args.date,
            "",
            "## Operating Frame",
            "",
            args.frame,
            "",
            "## Protected Time",
            "",
            args.protected_time or "Unknown.",
            "",
            "## Current State",
            "",
            *state_lines,
            "",
            "## Completed",
            "",
            "| Time | Directive | Outcome |",
            "| --- | --- | --- |",
            "| TBD | TBD | TBD |",
            "",
            "## Active Candidates",
            "",
            "| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *active_rows,
            "",
            "## Behavioral Strategy",
            "",
            "| Rank | Candidate | Target Behavior | Environment Design |",
            "| --- | --- | --- | --- |",
            *strategy_rows,
            "",
            "## Deferred",
            "",
            "| Candidate | Reason Deferred | Next Review |",
            "| --- | --- | --- |",
            *deferred_rows,
            "",
            "## Blocked",
            "",
            "| Candidate | Blocker | Required Change |",
            "| --- | --- | --- |",
            "| None | None | None |",
            "",
            "## Next Directive",
            "",
            "Select via `ops/directives/next_directive.py` or `ops/operator/next_step.py`.",
            "",
            "## Next Check-In",
            "",
            "After completion, blockage, or material state change.",
            "",
        ]
    )


def normalize_energy(value: str) -> str:
    normalized = value.strip().lower()
    if "low" in normalized:
        return "low"
    if "medium" in normalized:
        return "medium"
    if "high" in normalized:
        return "high"
    return "unknown"


def normalize_authority(value: str) -> str:
    normalized = value.strip().lower().replace("-", " ")
    mapping = {
        "level 0": "level_0_observe",
        "level 1": "level_1_recommend",
        "level 2": "level_2_direct",
        "level 3": "level_3_execute",
        "level 4": "level_4_escalate",
    }
    for marker, authority in mapping.items():
        if marker in normalized:
            return authority
    return "level_1_recommend"


def split_arg_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def build_json_queue(queue: QueueBuild) -> dict:
    args = queue.args
    active = queue.active
    deferred = queue.deferred
    if active:
        selected = active[0]
        next_directive = {
            "candidate_id": "candidate-1",
            "directive": selected.name,
            "selection_rationale": "Selected as the highest-ranked active candidate that fits supplied constraints.",
            "authority_level": normalize_authority(selected.authority),
            "governance_status": "ready",
            "target_behavior": selected.target_behavior,
            "environment_design": selected.environment_design,
        }
    else:
        next_directive = {
            "candidate_id": "",
            "directive": "Answer targeted operating question",
            "selection_rationale": "No active candidate fit the current queue constraints.",
            "authority_level": "level_1_recommend",
            "governance_status": "ready",
            "target_behavior": "Create the missing condition for PEGO to select a directive.",
            "environment_design": "Ask one targeted operational question instead of issuing a broad reflection prompt.",
        }

    return {
        "artifact_type": "directive_queue",
        "schema_version": 1,
        "session": args.date,
        "operating_frame": args.frame,
        "protected_time": [
            {
                "label": "Protected time",
                "window": args.protected_time,
                "protection_level": "hard",
            }
        ]
        if args.protected_time
        else [],
        "current_state": {
            "time": args.time or "",
            "location": args.location or "",
            "energy": normalize_energy(args.energy or ""),
            "environment": args.environment or "",
            "active_obligations": split_arg_list(args.obligations),
            "known_constraints": split_arg_list(args.constraints),
        },
        "completed": [],
        "active_candidates": [
            {
                "rank": rank,
                "candidate_id": f"candidate-{rank}",
                "candidate": candidate.name,
                "domain": candidate.domain,
                "duration": candidate.duration,
                "energy": normalize_energy(candidate.energy),
                "location": candidate.location,
                "deadline": candidate.deadline,
                "authority_level": normalize_authority(candidate.authority),
                "governance_status": "ready",
                "target_behavior": candidate.target_behavior,
                "environment_design": candidate.environment_design,
                "source": candidate.source,
            }
            for rank, candidate in enumerate(active, start=1)
        ],
        "deferred": [
            {
                "candidate_id": f"deferred-{index}",
                "candidate": candidate.name,
                "reason_deferred": reason,
                "next_review": "Next synthesis",
                "consequence_of_deferral": candidate.deferral,
            }
            for index, (candidate, reason) in enumerate(deferred, start=1)
        ],
        "blocked": [],
        "next_directive": next_directive,
        "next_check_in": "After completion, blockage, or material state change.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--candidate", type=Path, action="append", default=[])
    parser.add_argument("--available", type=int)
    parser.add_argument("--time")
    parser.add_argument("--location")
    parser.add_argument("--energy")
    parser.add_argument("--environment")
    parser.add_argument("--obligations")
    parser.add_argument("--constraints")
    parser.add_argument("--protected-time", default="")
    parser.add_argument("--frame", default="Synthesize current candidate directives into one active queue.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    if not args.candidate:
        raise SystemExit("at least one --candidate file is required")

    candidates = read_candidates(args.candidate)
    output = args.output or private / "directives" / "queues" / f"{args.date}-queue.md"
    queue = build_queue(candidates, args)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_markdown_queue(queue))
    print(f"wrote: {output}")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        if args.json_output.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {args.json_output}")
        args.json_output.write_text(json.dumps(build_json_queue(queue), indent=2) + "\n")
        print(f"wrote: {args.json_output}")


if __name__ == "__main__":
    main_with_args()
