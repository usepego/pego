"""Installable PEGO command wrapper.

The packaged command delegates to operation scripts in a PEGO framework checkout.
For now, this is intentionally a thin adapter: it makes `pegoctl` installable
without turning the framework into a Python runtime.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def source_root() -> Path:
    return Path(__file__).resolve().parents[2]


def candidate_roots() -> list[Path]:
    roots: list[Path] = []
    env_root = os.environ.get("PEGO_FRAMEWORK_ROOT")
    if env_root:
        roots.append(Path(env_root).expanduser())
    roots.append(Path.cwd())
    roots.append(source_root())
    return roots


def is_framework_root(path: Path) -> bool:
    return (
        (path / "pego" / "system" / "registry.json").is_file()
        and (path / "ops" / "pego_doctor.py").is_file()
    )


def framework_root() -> Path:
    for root in candidate_roots():
        if is_framework_root(root):
            return root
    raise SystemExit(
        "Unable to find a PEGO framework root. Run from a PEGO checkout or set PEGO_FRAMEWORK_ROOT."
    )


def run_script(relative: str, args: list[str]) -> int:
    root = framework_root()
    command = [sys.executable, str(root / relative), *args]
    completed = subprocess.run(command, cwd=root)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pegoctl",
        description="Local PEGO operation wrapper for framework checks and USER-mode operation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="verify repository hygiene and framework contracts")
    subparsers.add_parser("readiness", help="check protected private instance readiness")
    subparsers.add_parser("storage", help="check protected private storage and backup readiness")
    subparsers.add_parser("bootstrap", help="create or refresh private instance skeleton")
    subparsers.add_parser("brief", help="generate a protected operating brief")
    subparsers.add_parser("close-session", help="close a USER-mode session into a review")
    subparsers.add_parser(
        "promote-context",
        help="promote session-review candidates into protected context updates",
    )
    subparsers.add_parser(
        "apply-context",
        help="review and optionally apply protected context updates to durable private memory",
    )
    subparsers.add_parser("next", help="select one next directive and run preflight")
    check_in = subparsers.add_parser(
        "check-in",
        help="record a USER-mode check-in and select one next directive",
    )
    check_in.add_argument("input", help="human status update or next-directive request")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, forwarded = parser.parse_known_args(argv)

    if args.command == "doctor":
        if forwarded:
            parser.error("doctor does not accept forwarded arguments")
        return run_script("ops/pego_doctor.py", [])
    if args.command == "readiness":
        return run_script("ops/private/check_readiness.py", forwarded)
    if args.command == "storage":
        return run_script("ops/private/check_storage.py", forwarded)
    if args.command == "bootstrap":
        return run_script("ops/private/bootstrap_private_instance.py", forwarded)
    if args.command == "brief":
        return run_script("ops/operator/generate_brief.py", forwarded)
    if args.command == "close-session":
        return run_script("ops/operator/close_session.py", forwarded)
    if args.command == "promote-context":
        return run_script("ops/context/promote_session_review.py", forwarded)
    if args.command == "apply-context":
        return run_script("ops/context/apply_context_updates.py", forwarded)
    if args.command == "next":
        return run_script("ops/operator/next_step.py", forwarded)
    if args.command == "check-in":
        return run_script("ops/operator/user_check_in.py", ["--input", args.input, *forwarded])

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
