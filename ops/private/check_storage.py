#!/usr/bin/env python3
"""Check protected private instance storage and backup readiness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PRIVATE_ROOT = ROOT / "private"

BACKUP_MARKERS = [
    ("icloud", "Library/Mobile Documents/com~apple~CloudDocs"),
    ("icloud", "iCloud Drive"),
    ("dropbox", "Dropbox"),
    ("onedrive", "OneDrive"),
    ("google_drive", "Google Drive"),
    ("syncthing", "Syncthing"),
    ("proton_drive", "Proton Drive"),
]


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def storage_mode(private_root: Path) -> str:
    if not private_root.exists():
        return "missing"
    if private_root.is_symlink():
        return "symlink"
    resolved = private_root.resolve()
    if is_relative_to(resolved, ROOT.resolve()):
        return "in_framework_checkout"
    return "external"


def backup_signal(private_root: Path) -> str:
    path_text = str(private_root.expanduser().resolve()).lower()
    for label, marker in BACKUP_MARKERS:
        if marker.lower() in path_text:
            return label
    return "unknown"


def tracked_private_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "private"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return sorted(line for line in completed.stdout.splitlines() if line)


def display_private_root(private_root: Path, reveal_path: bool) -> str:
    if reveal_path:
        return str(private_root.expanduser().resolve())
    if is_relative_to(private_root.expanduser().resolve(), ROOT.resolve()):
        return "private/"
    return "external_private_root"


def recommended_next_action(decision: str) -> str:
    if decision in {"backup_ready", "backup_ready_manual"}:
        return "Proceed with private readiness checks before USER-mode operation."
    if decision == "missing_private_root":
        return "Bootstrap the private instance or choose a backed-up private root."
    return "Move the private root to a backed-up location or rerun with manual backup confirmation."


def assess(private_root: Path, manual_backup_confirmed: bool, reveal_path: bool) -> dict:
    mode = storage_mode(private_root)
    signal = "missing" if mode == "missing" else backup_signal(private_root)

    if mode == "missing":
        decision = "missing_private_root"
    elif signal != "unknown":
        decision = "backup_ready"
    elif manual_backup_confirmed:
        decision = "backup_ready_manual"
    else:
        decision = "backup_not_confirmed"

    tracked = tracked_private_paths()
    return {
        "artifact_type": "private_storage_readiness",
        "schema_version": 1,
        "decision": decision,
        "private_root": display_private_root(private_root, reveal_path),
        "storage_mode": mode,
        "backup_signal": signal,
        "manual_backup_confirmed": manual_backup_confirmed,
        "git_tracking": {
            "checked": True,
            "tracked_private_paths": tracked,
            "passes_boundary": tracked == ["private/README.md"],
        },
        "privacy": {
            "prints_private_contents": False,
            "safe_to_commit": False,
            "absolute_path_revealed": reveal_path,
        },
        "recommended_next_action": recommended_next_action(decision),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-root", type=Path, default=DEFAULT_PRIVATE_ROOT)
    parser.add_argument(
        "--backup-confirmed",
        action="store_true",
        help="assert that the private root is covered by a trusted backup system",
    )
    parser.add_argument(
        "--reveal-path",
        action="store_true",
        help="include the absolute private root path in output",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--print", action="store_true", help="print safe storage JSON")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    manual_backup_confirmed = args.backup_confirmed or os.environ.get(
        "PEGO_PRIVATE_BACKUP_CONFIRMED"
    ) == "1"
    result = assess(args.private_root, manual_backup_confirmed, args.reveal_path)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote: {args.output}")
    elif args.print:
        print(json.dumps(result, indent=2))
    else:
        print(f"storage readiness: {result['decision']}")
        print(f"storage mode: {result['storage_mode']}")
        print(f"backup signal: {result['backup_signal']}")
        print(f"recommended next action: {result['recommended_next_action']}")
    return result


if __name__ == "__main__":
    main_with_args()
