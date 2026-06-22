#!/usr/bin/env python3
"""Select one next PEGO directive from a private queue.

The runner reads protected private files under private/ and writes the response
back under private/directives/command-responses/. It is deliberately simple:
it does not grant authority, execute actions, or treat markdown parsing as a
source of truth beyond selecting a low-risk next directive candidate.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


@dataclass(frozen=True)
class Candidate:
    rank: int
    name: str
    domain: str
    duration: str
    energy: str
    location: str
    deadline: str
    authority: str
    status: str


@dataclass(frozen=True)
class CommandResponse:
    date: str
    state_update: str
    next_directive: str
    duration: str
    start_condition: str
    why_this_now: str
    fallback: str
    deferred: str
    stop_condition: str
    next_check_in: str
    candidate_rank: int | None
    authority: str
    governance_status: str
    targeted_question: str = ""


def read_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text()
    return ""


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_active_candidates(queue_text: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    in_table = False

    for line in queue_text.splitlines():
        if line.startswith("## Active Candidates"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        if "---" in line or "Rank" in line:
            continue

        cells = parse_table_cells(line)
        if len(cells) < 9:
            continue
        try:
            rank = int(cells[0])
        except ValueError:
            continue
        candidates.append(
            Candidate(
                rank=rank,
                name=cells[1],
                domain=cells[2],
                duration=cells[3],
                energy=cells[4],
                location=cells[5],
                deadline=cells[6],
                authority=cells[7],
                status=cells[8],
            )
        )

    return candidates


def parse_completed_inputs(values: list[str]) -> set[str]:
    return {value.strip().lower() for value in values if value.strip()}


def minutes_from_duration(duration: str) -> int | None:
    numbers = [int(match) for match in re.findall(r"\d+", duration)]
    if not numbers:
        return None
    return min(numbers)


def fits_time(candidate: Candidate, available: int | None) -> bool:
    if available is None:
        return True
    minutes = minutes_from_duration(candidate.duration)
    if minutes is None:
        return True
    return minutes <= available


def fits_energy(candidate: Candidate, energy: str | None) -> bool:
    if not energy:
        return True
    normalized = energy.lower()
    required = candidate.energy.lower()
    if normalized == "low" and "medium" in required and "low" not in required:
        return False
    return True


def fits_location(candidate: Candidate, location: str | None) -> bool:
    if not location:
        return True
    normalized = location.lower()
    required = candidate.location.lower()
    if "home" in required and normalized in {"home", "computer", "outside"}:
        return True
    if "outside" in required and normalized == "outside":
        return True
    if "computer" in required and normalized == "computer":
        return True
    if "phone" in required and normalized in {"phone", "computer", "home"}:
        return True
    if "inside" in required and normalized in {"home", "inside"}:
        return True
    return normalized in required


def is_completed(candidate: Candidate, completed: set[str]) -> bool:
    name = candidate.name.lower()
    return any(done in name or name in done for done in completed)


def status_score(status: str) -> int:
    normalized = status.lower()
    if "ready" in normalized:
        return 0
    if "conditional" in normalized:
        return 1
    if "optional" in normalized:
        return 2
    return 3


def choose_candidate(
    candidates: list[Candidate],
    completed: set[str],
    available: int | None,
    energy: str | None,
    location: str | None,
) -> Candidate | None:
    viable = []
    for candidate in candidates:
        if is_completed(candidate, completed):
            continue
        if not fits_energy(candidate, energy) or not fits_location(candidate, location):
            continue
        if fits_time(candidate, available):
            viable.append(candidate)
            continue
        adapted = reduced_candidate(candidate, available)
        if adapted:
            viable.append(adapted)
    if not viable:
        return None
    return sorted(viable, key=lambda candidate: (status_score(candidate.status), candidate.rank))[0]


def reduced_candidate(candidate: Candidate, available: int | None) -> Candidate | None:
    if available is None:
        return None
    if available < 30:
        return None
    if "venture" not in candidate.name.lower():
        return None
    return replace(candidate, name=f"Reduced {candidate.name}", duration=f"{available} min")


def first_register_question(register_text: str) -> str | None:
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
        cells = parse_table_cells(line)
        if cells and cells[0] and cells[0] != "TBD":
            return cells[0]
    return None


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


def normalize_governance_status(value: str) -> str:
    normalized = value.strip().lower()
    if "blocked" in normalized:
        return "blocked"
    if "reject" in normalized:
        return "rejected"
    if "formal" in normalized or "escalat" in normalized or "level 4" in normalized:
        return "needs_formal_review"
    if "standard" in normalized or "needs review" in normalized:
        return "needs_standard_review"
    if "light" in normalized:
        return "needs_light_review"
    if "ready" in normalized or "conditional" in normalized or "optional" in normalized:
        return "ready"
    return "draft"


def build_response_model(
    candidate: Candidate | None,
    register_question: str | None,
    args: argparse.Namespace,
) -> CommandResponse:
    state_parts = []
    if args.done:
        state_parts.append("completed: " + ", ".join(args.done))
    if args.blocked:
        state_parts.append("blocked: " + args.blocked)
    if args.available is not None:
        state_parts.append(f"available: {args.available} minutes")
    if args.energy:
        state_parts.append(f"energy: {args.energy}")
    if args.location:
        state_parts.append(f"location: {args.location}")
    state_update = "; ".join(state_parts) if state_parts else "No status update supplied."

    if candidate:
        return CommandResponse(
            date=args.date,
            state_update=state_update,
            next_directive=candidate.name,
            duration=candidate.duration,
            start_condition="Start if the stated time, location, energy, authority, and protected-time constraints still hold.",
            why_this_now=f"Selected from the active queue because it fits the supplied constraints and has queue rank {candidate.rank}.",
            fallback="If blocked, report the blocker and available time rather than expanding the plan.",
            deferred="Other queue candidates remain deferred until the next check-in.",
            stop_condition="Stop if the directive conflicts with protected time, requires higher authority, or no longer fits the available time.",
            next_check_in="Return after completion, blockage, or material change.",
            candidate_rank=candidate.rank,
            authority=normalize_authority(candidate.authority),
            governance_status=normalize_governance_status(candidate.status),
        )

    question = register_question or "What changed that PEGO should account for before selecting the next directive?"
    return CommandResponse(
        date=args.date,
        state_update=state_update,
        next_directive="Answer one targeted operating question.",
        duration="5 minutes.",
        start_condition="Use this when no active queue candidate cleanly fits the supplied constraints.",
        why_this_now="No viable directive was selected from the active queue. PEGO needs one decision-grade fact before resynthesis.",
        fallback="If the question is not relevant, report current time, location, energy, and one constraint.",
        deferred="All active directives remain deferred until PEGO can select one that fits.",
        stop_condition="Stop if answering would expose unnecessary private information or affect protected time.",
        next_check_in="Return with the answer and available time.",
        candidate_rank=None,
        authority="level_1_recommend",
        governance_status="ready",
        targeted_question=question,
    )


def build_markdown_response(response: CommandResponse) -> str:
    lines = [
        f"# Command Response: {response.date}",
        "",
        "## State Update",
        "",
        response.state_update,
        "",
        "## Next Directive",
        "",
        response.next_directive,
        "",
        "## Duration",
        "",
        response.duration,
        "",
        "## Start Condition",
        "",
        response.start_condition,
        "",
        "## Why This Now",
        "",
        response.why_this_now,
        "",
    ]
    if response.targeted_question:
        lines.extend(["## Targeted Question", "", response.targeted_question, ""])
    lines.extend(
        [
            "## Fallback",
            "",
            response.fallback,
            "",
            "## Deferred",
            "",
            response.deferred,
            "",
            "## Stop Condition",
            "",
            response.stop_condition,
            "",
            "## Next Check-In",
            "",
            response.next_check_in,
            "",
        ]
    )
    return "\n".join(lines)


def build_json_response(response: CommandResponse) -> dict:
    data = {
        "artifact_type": "command_response",
        "schema_version": 1,
        "date": response.date,
        "state_update": response.state_update,
        "next_directive": {
            "directive": response.next_directive,
            "candidate_rank": response.candidate_rank,
            "authority_level": response.authority,
            "governance_status": response.governance_status,
        },
        "duration": response.duration,
        "start_condition": response.start_condition,
        "why_this_now": response.why_this_now,
        "fallback": response.fallback,
        "deferred": response.deferred,
        "stop_condition": response.stop_condition,
        "next_check_in": response.next_check_in,
    }
    if response.targeted_question:
        data["targeted_question"] = response.targeted_question
    return data


def build_response(
    candidate: Candidate | None,
    register_question: str | None,
    args: argparse.Namespace,
) -> str:
    return build_markdown_response(build_response_model(candidate, register_question, args))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--register", type=Path, default=PRIVATE / "operator" / "operating-register.md")
    parser.add_argument("--done", action="append", default=[])
    parser.add_argument("--blocked", default="")
    parser.add_argument("--available", type=int)
    parser.add_argument("--energy", choices=["low", "medium", "high"])
    parser.add_argument("--location")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    queue = args.queue or PRIVATE / "directives" / "queues" / f"{args.date}-queue.md"
    output = args.output or PRIVATE / "directives" / "command-responses" / f"{args.date}-next.md"

    queue_text = read_if_exists(queue)
    register_text = read_if_exists(args.register)
    completed = parse_completed_inputs(args.done)
    candidates = parse_active_candidates(queue_text)
    candidate = choose_candidate(candidates, completed, args.available, args.energy, args.location)
    response = build_response_model(candidate, first_register_question(register_text), args)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_markdown_response(response))

    print(f"wrote: {output}")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        if args.json_output.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {args.json_output}")
        args.json_output.write_text(json.dumps(build_json_response(response), indent=2) + "\n")
        print(f"wrote: {args.json_output}")


if __name__ == "__main__":
    main_with_args()
