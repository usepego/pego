#!/usr/bin/env python3
"""Check protected private instance storage and backup readiness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402

BACKUP_MARKERS = [
    ("icloud", "Library/Mobile Documents/com~apple~CloudDocs"),
    ("icloud", "iCloud Drive"),
    ("dropbox", "Dropbox"),
    ("onedrive", "OneDrive"),
    ("google_drive", "Google Drive"),
    ("syncthing", "Syncthing"),
    ("proton_drive", "Proton Drive"),
]

CONFIRMATION_RELATIVE_PATH = "governance/preflight/storage-confirmation.json"


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


def confirmation_path(private_root: Path) -> Path:
    return private_root / CONFIRMATION_RELATIVE_PATH


def persisted_backup_confirmed(private_root: Path) -> bool:
    path = confirmation_path(private_root)
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return False
    return (
        data.get("artifact_type") == "private_storage_confirmation"
        and data.get("backup_confirmed") is True
    )


def write_backup_confirmation(private_root: Path, confirmed_at: str) -> Path:
    path = confirmation_path(private_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "artifact_type": "private_storage_confirmation",
                "schema_version": 1,
                "backup_confirmed": True,
                "confirmed_at": confirmed_at,
                "private_root": display_private_root(private_root, reveal_path=False),
                "privacy": {
                    "prints_private_contents": False,
                    "safe_to_commit": False,
                    "absolute_path_revealed": False,
                },
            },
            indent=2,
        )
        + "\n"
    )
    return path


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
    return private_root_config.display_private_root(private_root, reveal_path)


def recommended_next_action(decision: str) -> str:
    if decision in {"backup_ready", "backup_ready_manual"}:
        return "Proceed with private readiness checks before USER-mode operation."
    if decision == "missing_private_root":
        return "Bootstrap the private instance or choose a backed-up private root."
    return "Move the private root to a backed-up location or persist manual backup confirmation."


def assess(private_root: Path, manual_backup_confirmed: bool, reveal_path: bool) -> dict:
    mode = storage_mode(private_root)
    signal = "missing" if mode == "missing" else backup_signal(private_root)
    persisted_confirmation = persisted_backup_confirmed(private_root)
    confirmed = manual_backup_confirmed or persisted_confirmation

    if mode == "missing":
        decision = "missing_private_root"
    elif signal != "unknown":
        decision = "backup_ready"
    elif confirmed:
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
        "manual_backup_confirmed": confirmed,
        "persisted_backup_confirmation": persisted_confirmation,
        "confirmation_path": private_root_config.framework_relative_private_path(
            private_root, CONFIRMATION_RELATIVE_PATH
        ),
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
    parser.add_argument("--private-root", type=Path)
    parser.add_argument(
        "--backup-confirmed",
        action="store_true",
        help="assert backup coverage for this check without writing confirmation",
    )
    parser.add_argument(
        "--confirm-backup",
        action="store_true",
        help="persist manual backup confirmation under the protected private root",
    )
    parser.add_argument(
        "--confirmed-at",
        default=date.today().isoformat(),
        help="confirmation date for --confirm-backup, in YYYY-MM-DD format",
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
    root = private_root_config.resolve_private_root(args.private_root)
    if args.confirm_backup:
        write_backup_confirmation(root, args.confirmed_at)
        print(
            f"wrote: {private_root_config.framework_relative_private_path(root, CONFIRMATION_RELATIVE_PATH)}"
        )
    result = assess(root, manual_backup_confirmed, args.reveal_path)

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
