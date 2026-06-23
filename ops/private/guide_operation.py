#!/usr/bin/env python3
"""Generate a safe PEGO operating guide without printing private contents."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))
sys.path.insert(0, str(ROOT / "ops" / "private"))

import check_readiness  # noqa: E402
import check_storage  # noqa: E402
import private_root as private_root_config  # noqa: E402


CORE_STATE_CHECKS = {
    "constitution",
    "current_state",
    "person_profile",
    "protected_time",
    "operating_register",
}


def command_prefix(private_root: Path) -> str:
    display = private_root_config.display_private_root(private_root)
    if display == "private/":
        return "python3 pegoctl"
    return "python3 pegoctl --private-root <protected-private-root>"


def choose_next_step(private_root: Path, readiness: dict, storage: dict) -> dict:
    prefix = command_prefix(private_root)
    missing = set(readiness["missing_checks"])

    if storage["decision"] == "missing_private_root":
        return {
            "label": "Create private instance skeleton",
            "command": f"{prefix} bootstrap",
            "reason": "The protected private instance root does not exist yet.",
        }

    if storage["decision"] == "backup_not_confirmed":
        return {
            "label": "Confirm private storage backup",
            "command": f"{prefix} storage --confirm-backup",
            "reason": "PEGO can see private storage, but backup coverage is not confirmed.",
        }

    if missing & CORE_STATE_CHECKS:
        phase = "boundary" if "constitution" in missing else "current-state"
        return {
            "label": "Generate first-run intake packet",
            "command": f"{prefix} intake --phase {phase}",
            "reason": "PEGO needs core private state before it can govern USER-mode directives.",
        }

    if missing:
        return {
            "label": "Refresh private operating skeleton",
            "command": f"{prefix} bootstrap",
            "reason": "PEGO is missing generated operating paths or derived private artifacts.",
        }

    return {
        "label": "Start USER-mode operation",
        "command": f'{prefix} check-in "Available: 30 minutes. What is next?"',
        "reason": "Private readiness and storage checks are ready for governed operation.",
    }


def follow_up_commands(private_root: Path) -> list[str]:
    prefix = command_prefix(private_root)
    return [
        f"{prefix} readiness",
        f"{prefix} storage",
        f"{prefix} brief",
        f'{prefix} check-in "Done: prior directive. Available: 30 minutes. What is next?"',
    ]


def assess(private_root: Path, backup_confirmed: bool) -> dict:
    readiness = check_readiness.assess(private_root)
    storage = check_storage.assess(private_root, backup_confirmed, reveal_path=False)
    next_step = choose_next_step(private_root, readiness, storage)

    return {
        "artifact_type": "operating_guide",
        "schema_version": 1,
        "private_root": private_root_config.display_private_root(private_root),
        "readiness_decision": readiness["decision"],
        "storage_decision": storage["decision"],
        "missing_check_count": len(readiness["missing_checks"]),
        "next_step": next_step,
        "follow_up_commands": follow_up_commands(private_root),
        "privacy": {
            "prints_private_contents": False,
            "safe_to_commit": False,
            "absolute_path_revealed": False,
            "note": "Guide output contains status, counts, and command suggestions only; keep generated reports under the protected private root.",
        },
    }


def render_text(result: dict) -> str:
    lines = [
        "PEGO operating guide",
        f"readiness: {result['readiness_decision']}",
        f"storage: {result['storage_decision']}",
        f"missing checks: {result['missing_check_count']}",
        "",
        f"next: {result['next_step']['label']}",
        f"command: {result['next_step']['command']}",
        f"reason: {result['next_step']['reason']}",
        "",
        "follow-up commands:",
    ]
    lines.extend(f"- {command}" for command in result["follow_up_commands"])
    lines.extend(
        [
            "",
            "privacy: status only; private contents and absolute private paths are not printed.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--print-json", action="store_true", help="print safe guide JSON")
    parser.add_argument(
        "--backup-confirmed",
        action="store_true",
        help="assert that the private root is covered by a trusted backup system",
    )
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    backup_confirmed = args.backup_confirmed or os.environ.get(
        "PEGO_PRIVATE_BACKUP_CONFIRMED"
    ) == "1"
    root = private_root_config.resolve_private_root(args.private_root)
    result = assess(root, backup_confirmed)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote: {args.output}")
    elif args.print_json:
        print(json.dumps(result, indent=2))
    else:
        print(render_text(result), end="")
    return result


if __name__ == "__main__":
    main_with_args()
