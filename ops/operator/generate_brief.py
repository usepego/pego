#!/usr/bin/env python3
"""Generate a protected PEGO operating brief.

The brief is the USER-mode entry artifact for "brief me" interactions. It
summarizes the current operating frame, active queue, recent session state,
first directive, and governance posture into protected private output.

The runner does not print private brief content.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


@dataclass(frozen=True)
class QueueCandidate:
    rank: int
    candidate: str
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


def parse_section(text: str, heading: str) -> str:
    lines: list[str] = []
    in_section = False
    target = f"## {heading}"
    for line in text.splitlines():
        if line.startswith("## "):
            if in_section:
                break
            in_section = line.strip() == target
            continue
        if in_section:
            lines.append(line)
    return "\n".join(lines).strip()


def parse_active_candidates(queue_text: str) -> list[QueueCandidate]:
    candidates: list[QueueCandidate] = []
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
            QueueCandidate(
                rank=rank,
                candidate=cells[1],
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


def parse_session_event_count(session_json: Path) -> int:
    if not session_json.exists():
        return 0
    try:
        data = json.loads(session_json.read_text())
    except json.JSONDecodeError:
        return 0
    events = data.get("events", [])
    return len(events) if isinstance(events, list) else 0


def build_brief_model(args: argparse.Namespace) -> dict:
    queue_text = read_if_exists(args.queue)
    brief_text = read_if_exists(args.active_operating_brief)
    candidates = parse_active_candidates(queue_text)
    first = candidates[0] if candidates else None
    protected_time = parse_section(queue_text, "Protected Time") or "Use private protected-time rules if available."
    current_state = parse_section(queue_text, "Current State") or "No current queue state available."

    return {
        "artifact_type": "operating_brief",
        "schema_version": 1,
        "date": args.date,
        "mode": args.mode,
        "active_objective": args.objective or parse_section(brief_text, "Active Objective") or "Operate PEGO from current private state.",
        "active_queue": str(args.queue),
        "active_session": str(args.session_json),
        "session_events": parse_session_event_count(args.session_json),
        "protected_time": protected_time,
        "current_state": current_state,
        "first_directive": asdict(first) if first else None,
        "active_candidates": [asdict(candidate) for candidate in candidates[: args.limit]],
        "governance_notes": args.governance or "Level 1 unless an existing private constitution or preflight requires more review.",
        "next_action": "Run USER-mode check-in after completion, blockage, or material state change.",
    }


def build_markdown(model: dict) -> str:
    first = model["first_directive"]
    if first:
        first_text = "\n".join(
            [
                f"- Directive: {first['candidate']}",
                f"- Domain: {first['domain']}",
                f"- Duration: {first['duration']}",
                f"- Energy: {first['energy']}",
                f"- Location: {first['location']}",
                f"- Authority: {first['authority']}",
                f"- Status: {first['status']}",
            ]
        )
    else:
        first_text = "No active queue candidate found. Ask one targeted operating question or synthesize the directive queue."

    rows = [
        f"| {candidate['rank']} | {candidate['candidate']} | {candidate['domain']} | {candidate['duration']} | {candidate['energy']} | {candidate['location']} | {candidate['status']} |"
        for candidate in model["active_candidates"]
    ] or ["| None | None | None | None | None | None | None |"]

    return "\n".join(
        [
            f"# Operating Brief: {model['date']}",
            "",
            "## Current Operating Mode",
            "",
            model["mode"],
            "",
            "## Active Objective",
            "",
            model["active_objective"],
            "",
            "## Active Files",
            "",
            f"- Queue: {model['active_queue']}",
            f"- Session: {model['active_session']}",
            f"- Session events: {model['session_events']}",
            "",
            "## Protected Time",
            "",
            model["protected_time"],
            "",
            "## Current State",
            "",
            model["current_state"],
            "",
            "## First Directive",
            "",
            first_text,
            "",
            "## Active Candidates",
            "",
            "| Rank | Candidate | Domain | Duration | Energy | Location | Status |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Governance Notes",
            "",
            model["governance_notes"],
            "",
            "## Next Action",
            "",
            model["next_action"],
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--mode", default="USER mode")
    parser.add_argument("--objective", default="")
    parser.add_argument("--governance", default="")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--active-operating-brief", type=Path, default=PRIVATE / "active-operating-brief.md")
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--session-json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.queue = args.queue or PRIVATE / "directives" / "queues" / f"{args.date}-queue.md"
    args.session_json = args.session_json or PRIVATE / "operator" / "sessions" / f"{args.date}-user-mode.json"
    output = args.output or PRIVATE / "operator" / "briefs" / f"{args.date}-brief.md"
    json_output = args.json_output or PRIVATE / "operator" / "briefs" / f"{args.date}-brief.json"

    model = build_brief_model(args)

    for path, content in [
        (output, build_markdown(model)),
        (json_output, json.dumps(model, indent=2) + "\n"),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {path}")
        path.write_text(content)
        print(f"wrote: {path}")

    result = {
        "output": str(output),
        "json_output": str(json_output),
        "active_candidates": len(model["active_candidates"]),
        "has_first_directive": bool(model["first_directive"]),
        "session_events": model["session_events"],
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main_with_args()
