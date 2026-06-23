#!/usr/bin/env python3
"""Run one PEGO USER-mode check-in.

This is the private operating loop for "what is next?" interactions. It
records the human's status update, delegates directive selection to the
existing next-step runner, runs governance preflight through that runner, and
updates a protected intra-day session log.

The runner does not print private directive content.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))
sys.path.insert(0, str(ROOT / "ops" / "operator"))

import next_step  # noqa: E402
import private_root as private_root_config  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--time", default="")
    parser.add_argument("--input", required=True, help="human status update or request")
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--register", type=Path)
    parser.add_argument("--done", action="append", default=[])
    parser.add_argument("--blocked", default="")
    parser.add_argument("--available", type=int)
    parser.add_argument("--energy", choices=["low", "medium", "high"])
    parser.add_argument("--location")
    parser.add_argument("--session-output", type=Path)
    parser.add_argument("--session-json-output", type=Path)
    parser.add_argument("--response-output", type=Path)
    parser.add_argument("--response-json-output", type=Path)
    parser.add_argument("--preflight-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def read_json_if_exists(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def now_time() -> str:
    return datetime.now().strftime("%H:%M")


def infer_location_from_input(value: str) -> str:
    normalized = value.lower()
    location_markers = [
        ("grocery_store", [r"\bgrocery\b", r"\bsupermarket\b", r"\bmarket\b"]),
        ("restaurant", [r"\brestaurant\b", r"\bcafe\b", r"\bdiner\b", r"\blunch\b", r"\bdinner\b"]),
        ("airport", [r"\bairport\b", r"\bterminal\b", r"\bgate\b"]),
        ("car", [r"\bcar\b", r"\bdriving\b", r"\bparking\b"]),
        ("office", [r"\boffice\b", r"\bworkplace\b"]),
        ("outside", [r"\boutside\b", r"\bgarden\b", r"\byard\b", r"\bwalk\b"]),
        ("home", [r"\bhome\b", r"\bhouse\b", r"\bkitchen\b"]),
        ("phone", [r"\bphone\b"]),
        ("computer", [r"\bcomputer\b", r"\blaptop\b", r"\bdesk\b"]),
    ]
    for location, patterns in location_markers:
        if any(re.search(pattern, normalized) for pattern in patterns):
            return location
    return ""


def detect_circumstance_type(value: str, location: str) -> str:
    normalized = value.lower()
    if location:
        return "location_change"
    if any(word in normalized for word in ["hungry", "tired", "low energy", "raining", "weather"]):
        return "state_or_environment_change"
    if any(word in normalized for word in ["before", "minutes", "appointment", "meeting"]):
        return "time_window_change"
    return ""


def state_update(args: argparse.Namespace) -> dict:
    location = args.location or infer_location_from_input(args.input)
    circumstance_type = detect_circumstance_type(args.input, location)
    return {
        "available_minutes": args.available,
        "energy": args.energy or "",
        "location": location,
        "circumstance_type": circumstance_type,
        "circumstance_summary": args.input if circumstance_type else "",
        "completed": args.done,
        "blocked": args.blocked,
    }


def build_event(args: argparse.Namespace, summary: dict) -> dict:
    return {
        "time": args.time or now_time(),
        "human_input": args.input,
        "state_update": state_update(args),
        "command_response_path": summary["response_output"],
        "command_response_json_path": summary.get("response_json_output", ""),
        "preflight_path": summary["preflight_output"],
        "preflight_outcome": summary["preflight_outcome"],
        "review_level": summary["review_level"],
        "required_next_step": summary["required_next_step"],
    }


def empty_session(args: argparse.Namespace) -> dict:
    return {
        "artifact_type": "intra_day_session_log",
        "schema_version": 1,
        "date": args.date,
        "active_queue": str(args.queue) if args.queue else "",
        "operating_frame": "USER mode check-in loop.",
        "events": [],
        "completed_directives": [],
        "blocked_or_partial_directives": [],
        "queue_adjustments": [],
        "deferrals": [],
        "governance_notes": [],
        "end_of_day_transfer": [],
    }


def update_session(args: argparse.Namespace, event: dict, private: Path) -> dict:
    output = args.session_json_output or (
        private / "operator" / "sessions" / f"{args.date}-user-mode.json"
    )
    session = read_json_if_exists(output)
    if session is None:
        session = empty_session(args)
    if session.get("artifact_type") != "intra_day_session_log":
        raise SystemExit(f"unexpected session artifact type in {output}")

    session["events"].append(event)

    for directive in args.done:
        session["completed_directives"].append(
            {
                "time": event["time"],
                "directive": directive,
                "evidence": "reported by human",
                "notes": args.input,
            }
        )
    if args.blocked:
        session["blocked_or_partial_directives"].append(
            {
                "time": event["time"],
                "directive": "current or prior directive",
                "status": "blocked",
                "reason": args.blocked,
                "next_handling": "resynthesize or choose fallback through next check-in",
            }
        )
    if event["preflight_outcome"] != "pass":
        session["governance_notes"].append(
            {
                "time": event["time"],
                "note": event["required_next_step"],
                "review_level": event["review_level"],
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(session, indent=2) + "\n")
    return session


def build_markdown_session(session: dict) -> str:
    event_rows = []
    for event in session["events"]:
        state = event["state_update"]
        state_text = "; ".join(
            part
            for part in [
                f"available={state['available_minutes']}" if state["available_minutes"] is not None else "",
                f"energy={state['energy']}" if state["energy"] else "",
                f"location={state['location']}" if state["location"] else "",
                f"circumstance={state['circumstance_type']}" if state.get("circumstance_type") else "",
                "completed=" + ", ".join(state["completed"]) if state["completed"] else "",
                f"blocked={state['blocked']}" if state["blocked"] else "",
            ]
            if part
        )
        event_rows.append(
            f"| {event['time']} | {event['human_input']} | {state_text or 'No structured state supplied.'} | {event['command_response_path']} | {event['preflight_outcome']} |"
        )
    if not event_rows:
        event_rows.append("| TBD | TBD | TBD | TBD | TBD |")

    completed_rows = [
        f"| {item['time']} | {item['directive']} | {item['evidence']} | {item['notes']} |"
        for item in session["completed_directives"]
    ] or ["| None | None | None | None |"]

    blocked_rows = [
        f"| {item['time']} | {item['directive']} | {item['status']} | {item['reason']} | {item['next_handling']} |"
        for item in session["blocked_or_partial_directives"]
    ] or ["| None | None | None | None | None |"]

    governance_rows = [
        f"- {item['time']}: {item['note']} ({item['review_level']})"
        for item in session["governance_notes"]
    ] or ["- None."]

    return "\n".join(
        [
            f"# Intra-Day Session Log: {session['date']}",
            "",
            "## Date or Session",
            "",
            session["date"],
            "",
            "## Active Queue",
            "",
            session["active_queue"] or "Default private queue for the date.",
            "",
            "## Operating Frame",
            "",
            session["operating_frame"],
            "",
            "## Session Events",
            "",
            "| Time | Human Input | State Change | PEGO Response | Outcome |",
            "| --- | --- | --- | --- | --- |",
            *event_rows,
            "",
            "## Completed Directives",
            "",
            "| Time | Directive | Evidence | Notes |",
            "| --- | --- | --- | --- |",
            *completed_rows,
            "",
            "## Partial, Blocked, or Canceled Directives",
            "",
            "| Time | Directive | Status | Reason | Next Handling |",
            "| --- | --- | --- | --- | --- |",
            *blocked_rows,
            "",
            "## Queue Adjustments",
            "",
            "- None recorded by this check-in.",
            "",
            "## Deferrals",
            "",
            "- See the command response for current deferrals.",
            "",
            "## Governance Notes",
            "",
            *governance_rows,
            "",
            "## End-of-Day Transfer",
            "",
            "- Promote completed directives, blockers, and useful context into outcome or context records.",
            "",
        ]
    )


def run_next_step(args: argparse.Namespace) -> dict:
    private = private_root_config.resolve_private_root(args.private_root)
    response_output = args.response_output or (
        private / "directives" / "command-responses" / f"{args.date}-next.md"
    )
    response_json_output = args.response_json_output or (
        private / "directives" / "command-responses" / f"{args.date}-next.json"
    )
    preflight_output = args.preflight_output or (
        private / "governance" / "preflight" / f"{args.date}-next.json"
    )

    forwarded = [
        "--date",
        args.date,
        "--response-output",
        str(response_output),
        "--response-json-output",
        str(response_json_output),
        "--preflight-output",
        str(preflight_output),
    ]
    if args.private_root:
        forwarded.extend(["--private-root", str(args.private_root)])
    if args.queue:
        forwarded.extend(["--queue", str(args.queue)])
    if args.register:
        forwarded.extend(["--register", str(args.register)])
    for done in args.done:
        forwarded.extend(["--done", done])
    if args.blocked:
        forwarded.extend(["--blocked", args.blocked])
    if args.available is not None:
        forwarded.extend(["--available", str(args.available)])
    if args.energy:
        forwarded.extend(["--energy", args.energy])
    location = args.location or infer_location_from_input(args.input)
    if location:
        forwarded.extend(["--location", location])
    if args.force:
        forwarded.append("--force")

    return next_step.main_with_args(forwarded)


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)

    summary = run_next_step(args)
    event = build_event(args, summary)
    session = update_session(args, event, private)

    session_output = args.session_output or (
        private / "operator" / "sessions" / f"{args.date}-user-mode.md"
    )
    session_output.parent.mkdir(parents=True, exist_ok=True)
    session_output.write_text(build_markdown_session(session))

    result = {
        "session_output": str(session_output),
        "session_json_output": str(
            args.session_json_output
            or private / "operator" / "sessions" / f"{args.date}-user-mode.json"
        ),
        "response_output": summary["response_output"],
        "response_json_output": summary.get("response_json_output", ""),
        "preflight_output": summary["preflight_output"],
        "preflight_outcome": summary["preflight_outcome"],
        "events": len(session["events"]),
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main_with_args()
