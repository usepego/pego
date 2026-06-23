#!/usr/bin/env python3
"""Close a PEGO USER-mode session into a protected learning review.

This runner reads an intra-day session log JSON and writes a protected
session-review artifact. It does not print private session content.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "session"


def load_session(path: Path) -> dict:
    data = json.loads(path.read_text())
    if data.get("artifact_type") != "intra_day_session_log":
        raise SystemExit(f"expected intra_day_session_log artifact: {path}")
    return data


def classify_blockers(session: dict) -> list[dict]:
    blockers = []
    for item in session.get("blocked_or_partial_directives", []):
        reason = str(item.get("reason", "")).strip()
        blockers.append(
            {
                "directive": str(item.get("directive", "current or prior directive")),
                "reason": reason,
                "next_handling": str(item.get("next_handling", "Resynthesize before repeating.")),
                "context_update_candidate": bool(reason),
            }
        )
    return blockers


def completed_directives(session: dict) -> list[dict]:
    return [
        {
            "directive": str(item.get("directive", "")),
            "evidence": str(item.get("evidence", "")),
            "notes": str(item.get("notes", "")),
        }
        for item in session.get("completed_directives", [])
        if str(item.get("directive", "")).strip()
    ]


def governance_notes(session: dict) -> list[dict]:
    return [
        {
            "note": str(item.get("note", "")),
            "review_level": str(item.get("review_level", "")),
        }
        for item in session.get("governance_notes", [])
    ]


def next_day_inputs(completed: list[dict], blockers: list[dict], governance: list[dict]) -> list[str]:
    inputs: list[str] = []
    if completed:
        inputs.append("Remove completed directives from the active queue unless recurrence is intentional.")
    if blockers:
        inputs.append("Move blocked directives to blocked/deferred until dependency changes or scope is reduced.")
    if governance:
        inputs.append("Route governance notes before increasing authority or repeating constrained directives.")
    if not inputs:
        inputs.append("Ask one targeted operating question before synthesizing the next queue.")
    return inputs


def context_candidates(completed: list[dict], blockers: list[dict]) -> list[dict]:
    candidates: list[dict] = []
    for blocker in blockers:
        if blocker["context_update_candidate"]:
            candidates.append(
                {
                    "source": "Outcome",
                    "update_class": "Pattern",
                    "evidence_strength": "Directive outcome",
                    "stability": "Provisional",
                    "proposed_update": f"Directive blocker observed: {blocker['reason']}",
                    "affected_agents": "Operations",
                    "action": "Record only",
                }
            )
    if len(completed) >= 2:
        candidates.append(
            {
                "source": "Outcome",
                "update_class": "Pattern",
                "evidence_strength": "Directive outcome",
                "stability": "Provisional",
                "proposed_update": "Multiple directives were reported complete in one USER-mode session.",
                "affected_agents": "Operations",
                "action": "Record only",
            }
        )
    return candidates


def build_review(session_path: Path, args: argparse.Namespace) -> dict:
    session = load_session(session_path)
    completed = completed_directives(session)
    blockers = classify_blockers(session)
    governance = governance_notes(session)
    events = session.get("events", [])
    event_count = len(events) if isinstance(events, list) else 0
    completed_count = len(completed)
    blocker_count = len(blockers)

    if governance:
        learning_decision = "governance_review"
    elif blocker_count:
        learning_decision = "resynthesize_with_blockers"
    elif completed_count:
        learning_decision = "carry_forward_completed_evidence"
    else:
        learning_decision = "ask_targeted_question"

    return {
        "artifact_type": "session_review",
        "schema_version": 1,
        "date": args.date,
        "source_session": str(session_path),
        "event_count": event_count,
        "completed_count": completed_count,
        "blocked_or_partial_count": blocker_count,
        "completed_directives": completed,
        "blockers": blockers,
        "governance_notes": governance,
        "learning_decision": learning_decision,
        "context_update_candidates": context_candidates(completed, blockers),
        "next_day_inputs": next_day_inputs(completed, blockers, governance),
        "next_review": args.next_review or "Next daily planning cycle.",
    }


def build_markdown(review: dict) -> str:
    completed_rows = [
        f"| {item['directive']} | {item['evidence']} | {item['notes']} |"
        for item in review["completed_directives"]
    ] or ["| None | None | None |"]
    blocker_rows = [
        f"| {item['directive']} | {item['reason']} | {item['next_handling']} |"
        for item in review["blockers"]
    ] or ["| None | None | None |"]
    context_rows = [
        f"| {item['update_class']} | {item['proposed_update']} | {item['affected_agents']} | {item['action']} |"
        for item in review["context_update_candidates"]
    ] or ["| None | None | None | None |"]
    governance_rows = [
        f"| {item['review_level']} | {item['note']} |" for item in review["governance_notes"]
    ] or ["| None | None |"]
    next_inputs = [f"- {item}" for item in review["next_day_inputs"]]

    return "\n".join(
        [
            f"# Session Review: {review['date']}",
            "",
            "## Source Session",
            "",
            review["source_session"],
            "",
            "## Counts",
            "",
            f"- Events: {review['event_count']}",
            f"- Completed directives: {review['completed_count']}",
            f"- Blocked or partial directives: {review['blocked_or_partial_count']}",
            "",
            "## Learning Decision",
            "",
            review["learning_decision"],
            "",
            "## Completed Directives",
            "",
            "| Directive | Evidence | Notes |",
            "| --- | --- | --- |",
            *completed_rows,
            "",
            "## Blockers",
            "",
            "| Directive | Reason | Next Handling |",
            "| --- | --- | --- |",
            *blocker_rows,
            "",
            "## Governance Notes",
            "",
            "| Review Level | Note |",
            "| --- | --- |",
            *governance_rows,
            "",
            "## Context Update Candidates",
            "",
            "| Class | Proposed Update | Affected Agents | Action |",
            "| --- | --- | --- | --- |",
            *context_rows,
            "",
            "## Next-Day Inputs",
            "",
            *next_inputs,
            "",
            "## Next Review",
            "",
            review["next_review"],
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--session-json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--next-review", default="")
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    session_json = args.session_json or PRIVATE / "operator" / "sessions" / f"{args.date}-user-mode.json"
    output = args.output or PRIVATE / "reviews" / "sessions" / f"{args.date}-session-review.md"
    json_output = args.json_output or PRIVATE / "reviews" / "sessions" / f"{args.date}-session-review.json"
    review = build_review(session_json, args)

    for path, content in [
        (output, build_markdown(review)),
        (json_output, json.dumps(review, indent=2) + "\n"),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {path}")
        path.write_text(content)
        print(f"wrote: {path}")

    result = {
        "output": str(output),
        "json_output": str(json_output),
        "event_count": review["event_count"],
        "completed_count": review["completed_count"],
        "blocked_or_partial_count": review["blocked_or_partial_count"],
        "learning_decision": review["learning_decision"],
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main_with_args()
