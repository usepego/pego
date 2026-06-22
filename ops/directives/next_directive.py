#!/usr/bin/env python3
"""Select one next PEGO directive from a private queue.

The runner reads ignored local files under private/ and writes the response
back under private/directives/command-responses/. It is deliberately simple:
it does not grant authority, execute actions, or treat markdown parsing as a
source of truth beyond selecting a low-risk next directive candidate.
"""

from __future__ import annotations

import argparse
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


def build_response(
    candidate: Candidate | None,
    register_question: str | None,
    args: argparse.Namespace,
) -> str:
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
        return "\n".join(
            [
                f"# Command Response: {args.date}",
                "",
                "## State Update",
                "",
                state_update,
                "",
                "## Next Directive",
                "",
                candidate.name,
                "",
                "## Duration",
                "",
                candidate.duration,
                "",
                "## Start Condition",
                "",
                "Start if the stated time, location, energy, authority, and protected-time constraints still hold.",
                "",
                "## Why This Now",
                "",
                f"Selected from the active queue because it fits the supplied constraints and has queue rank {candidate.rank}.",
                "",
                "## Fallback",
                "",
                "If blocked, report the blocker and available time rather than expanding the plan.",
                "",
                "## Deferred",
                "",
                "Other queue candidates remain deferred until the next check-in.",
                "",
                "## Stop Condition",
                "",
                "Stop if the directive conflicts with protected time, requires higher authority, or no longer fits the available time.",
                "",
                "## Next Check-In",
                "",
                "Return after completion, blockage, or material change.",
                "",
            ]
        )

    question = register_question or "What changed that PEGO should account for before selecting the next directive?"
    return "\n".join(
        [
            f"# Command Response: {args.date}",
            "",
            "## State Update",
            "",
            state_update,
            "",
            "## Next Directive",
            "",
            "Answer one targeted operating question.",
            "",
            "## Duration",
            "",
            "5 minutes.",
            "",
            "## Start Condition",
            "",
            "Use this when no active queue candidate cleanly fits the supplied constraints.",
            "",
            "## Why This Now",
            "",
            "No viable directive was selected from the active queue. PEGO needs one decision-grade fact before resynthesis.",
            "",
            "## Targeted Question",
            "",
            question,
            "",
            "## Fallback",
            "",
            "If the question is not relevant, report current time, location, energy, and one constraint.",
            "",
            "## Deferred",
            "",
            "All active directives remain deferred until PEGO can select one that fits.",
            "",
            "## Stop Condition",
            "",
            "Stop if answering would expose unnecessary private information or affect protected time.",
            "",
            "## Next Check-In",
            "",
            "Return with the answer and available time.",
            "",
        ]
    )


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
    response = build_response(candidate, first_register_question(register_text), args)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(response)

    print(f"wrote: {output}")


if __name__ == "__main__":
    main_with_args()
