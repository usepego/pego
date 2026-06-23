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


def with_private_root(args: argparse.Namespace, forwarded: list[str]) -> list[str]:
    if not args.private_root:
        return forwarded
    if "--private-root" in forwarded:
        return forwarded
    return ["--private-root", str(args.private_root), *forwarded]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pegoctl",
        description="Local PEGO operation wrapper for framework checks and USER-mode operation.",
    )
    parser.add_argument(
        "--private-root",
        type=Path,
        help="protected private instance root for commands that read or write private artifacts",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="verify repository hygiene and framework contracts")
    subparsers.add_parser("readiness", help="check protected private instance readiness")
    subparsers.add_parser("storage", help="check protected private storage and backup readiness")
    subparsers.add_parser("bootstrap", help="create or refresh private instance skeleton")
    subparsers.add_parser("daily", help="run daily operating-loop subcommands")
    subparsers.add_parser("weekly", help="generate a protected weekly operating plan")
    subparsers.add_parser("monthly", help="generate a protected monthly strategy review")
    subparsers.add_parser("finance-run", help="run protected finance scenarios")
    subparsers.add_parser("finance-review", help="review protected finance scenario output")
    subparsers.add_parser("health-candidates", help="generate protected health directive candidates")
    subparsers.add_parser("meal", help="select a protected meal directive from food options")
    subparsers.add_parser("home-candidates", help="generate protected home/environment directive candidates")
    subparsers.add_parser("anticipate", help="generate a protected anticipation scan")
    subparsers.add_parser("attention", help="select a protected attention directive")
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
        if args.private_root:
            parser.error("doctor does not use --private-root")
        return run_script("ops/pego_doctor.py", [])
    if args.command == "readiness":
        return run_script("ops/private/check_readiness.py", with_private_root(args, forwarded))
    if args.command == "storage":
        return run_script("ops/private/check_storage.py", with_private_root(args, forwarded))
    if args.command == "bootstrap":
        return run_script("ops/private/bootstrap_private_instance.py", with_private_root(args, forwarded))
    if args.command == "daily":
        if not forwarded:
            parser.error("daily requires a daily-cycle subcommand, such as health-check-in, synthesize, next, outcome, review, or learn")
        return run_script("ops/cycles/daily_cycle.py", with_private_root(args, forwarded))
    if args.command == "weekly":
        return run_script("ops/cycles/weekly_cycle.py", with_private_root(args, forwarded))
    if args.command == "monthly":
        return run_script("ops/cycles/monthly_cycle.py", with_private_root(args, forwarded))
    if args.command == "finance-run":
        return run_script("ops/finance/run_scenarios.py", with_private_root(args, forwarded))
    if args.command == "finance-review":
        return run_script("ops/finance/review_scenarios.py", with_private_root(args, forwarded))
    if args.command == "health-candidates":
        return run_script("ops/health/generate_candidates.py", with_private_root(args, forwarded))
    if args.command == "meal":
        return run_script("ops/health/decide_meal.py", with_private_root(args, forwarded))
    if args.command == "home-candidates":
        return run_script("ops/home/generate_candidates.py", with_private_root(args, forwarded))
    if args.command == "anticipate":
        return run_script("ops/anticipation/generate_scan.py", with_private_root(args, forwarded))
    if args.command == "attention":
        return run_script("ops/attention/decide_attention.py", with_private_root(args, forwarded))
    if args.command == "brief":
        return run_script("ops/operator/generate_brief.py", with_private_root(args, forwarded))
    if args.command == "close-session":
        return run_script("ops/operator/close_session.py", with_private_root(args, forwarded))
    if args.command == "promote-context":
        return run_script("ops/context/promote_session_review.py", with_private_root(args, forwarded))
    if args.command == "apply-context":
        return run_script("ops/context/apply_context_updates.py", with_private_root(args, forwarded))
    if args.command == "next":
        return run_script("ops/operator/next_step.py", with_private_root(args, forwarded))
    if args.command == "check-in":
        return run_script(
            "ops/operator/user_check_in.py",
            with_private_root(args, ["--input", args.input, *forwarded]),
        )

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
