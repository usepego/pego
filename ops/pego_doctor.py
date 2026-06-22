#!/usr/bin/env python3
"""Verify PEGO repository hygiene and required framework structure."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    ".gitignore",
    "private/README.md",
    "pego/principles.md",
    "pego/system/README.md",
    "pego/system/registry.json",
    "pego/agents/council-protocol.md",
    "pego/agents/finance-agent.md",
    "pego/agents/governance-agent.md",
    "pego/agents/health-agent.md",
    "pego/agents/career-agent.md",
    "pego/agents/venture-agent.md",
    "pego/agents/home-environment-agent.md",
    "pego/agents/relationships-agent.md",
    "pego/agents/exploration-agent.md",
    "pego/agents/happiness-agent.md",
    "pego/agents/operations-agent.md",
    "pego/governance/authority-levels.md",
    "pego/governance/compliance-review.md",
    "pego/governance/conflict-resolution.md",
    "pego/governance/repository-access-policy.md",
    "pego/operations/daily-loop.md",
    "pego/operations/weekly-loop.md",
    "pego/operations/monthly-loop.md",
    "pego/operations/directive-synthesis.md",
    "pego/operations/operator-interface.md",
    "pego/operations/runtime-agent-protocol.md",
    "pego/operations/first-run.md",
    "pego/operations/operating-readiness.md",
    "pego/operations/intra-day-command-loop.md",
    "pego/operations/outcome-review.md",
    "pego/operations/context-update.md",
    "pego/operations/anticipation-loop.md",
    "pego/operations/private-instance-workflow.md",
    "pego/templates/agent-recommendation.md",
    "pego/templates/active-operating-brief.md",
    "pego/templates/directive-candidate.md",
    "pego/templates/directive-queue.md",
    "pego/templates/intra-day-session-log.md",
    "pego/templates/command-response.md",
    "pego/templates/directive-outcome.md",
    "pego/templates/context-update.md",
    "pego/templates/anticipation-scan.md",
    "pego/templates/operating-register.md",
    "pego/templates/decision-packet.md",
    "pego/templates/synthesized-day-plan.md",
    "pego/templates/weekly-operating-plan.md",
    "pego/templates/monthly-strategy-review.md",
    "ops/private/bootstrap_private_instance.py",
    "ops/cycles/daily_cycle.py",
    "ops/cycles/test_daily_cycle.py",
    "ops/operator/next_step.py",
    "ops/operator/test_next_step.py",
    "ops/context/record_context_update.py",
    "ops/context/test_record_context_update.py",
    "ops/outcomes/record_outcome.py",
    "ops/outcomes/test_record_outcome.py",
    "ops/directives/generate_daily_directive.py",
    "ops/directives/next_directive.py",
    "ops/directives/test_next_directive.py",
    "ops/governance/directive_preflight.py",
    "ops/governance/test_directive_preflight.py",
    "ops/governance/generate_compliance_review.py",
    "ops/finance/run_scenarios.py",
    "ops/finance/test_run_scenarios.py",
    "ops/pego_registry.py",
]

LOCAL_MARKERS_FILE = ROOT / "private" / "_local" / "doctor-private-markers.txt"
REGISTRY_FILE = ROOT / "pego" / "system" / "registry.json"


def run_git(args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_private_tracking(errors: list[str]) -> None:
    tracked_private = sorted(
        line for line in run_git(["ls-files", "private"]).splitlines() if line
    )
    if tracked_private != ["private/README.md"]:
        errors.append(
            "private tracking boundary failed: expected only private/README.md, got "
            + ", ".join(tracked_private)
        )


def check_private_ignored(errors: list[str]) -> None:
    paths = [
        "private/constitution/constitution.md",
        "private/finance/financial-position.md",
        "private/person/observations.md",
        "private/directives/daily/example.md",
    ]
    for relative in paths:
        completed = subprocess.run(
            ["git", "check-ignore", relative],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            errors.append(f"private path is not ignored: {relative}")


def check_registry(errors: list[str]) -> None:
    if not REGISTRY_FILE.exists():
        errors.append("missing system registry: pego/system/registry.json")
        return

    try:
        registry = json.loads(REGISTRY_FILE.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"system registry is invalid JSON: {exc}")
        return

    verify_paths = registry.get("verify_paths")
    if not isinstance(verify_paths, list) or not verify_paths:
        errors.append("system registry must define a non-empty verify_paths list")
        return

    for relative in verify_paths:
        if not isinstance(relative, str):
            errors.append("system registry verify_paths entries must be strings")
            continue
        if relative.startswith("private/") and relative != "private/README.md":
            errors.append(f"system registry must not verify local-only private path: {relative}")
            continue
        if not (ROOT / relative).is_file():
            errors.append(f"system registry references missing file: {relative}")


def check_tracked_content_markers(errors: list[str]) -> None:
    if not LOCAL_MARKERS_FILE.exists():
        return
    markers = [
        line.strip()
        for line in LOCAL_MARKERS_FILE.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not markers:
        return

    tracked = [line for line in run_git(["ls-files"]).splitlines() if line]
    pattern = re.compile("|".join(re.escape(marker) for marker in markers))
    for relative in tracked:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        match = pattern.search(text)
        if match:
            errors.append(f"private marker '{match.group(0)}' found in tracked file: {relative}")


def check_python_syntax(errors: list[str]) -> None:
    scripts = [
        "ops/private/bootstrap_private_instance.py",
        "ops/cycles/daily_cycle.py",
        "ops/cycles/test_daily_cycle.py",
        "ops/operator/next_step.py",
        "ops/operator/test_next_step.py",
        "ops/context/record_context_update.py",
        "ops/context/test_record_context_update.py",
        "ops/outcomes/record_outcome.py",
        "ops/outcomes/test_record_outcome.py",
        "ops/directives/generate_daily_directive.py",
        "ops/directives/next_directive.py",
        "ops/directives/test_next_directive.py",
        "ops/governance/directive_preflight.py",
        "ops/governance/test_directive_preflight.py",
        "ops/governance/generate_compliance_review.py",
        "ops/finance/run_scenarios.py",
        "ops/finance/test_run_scenarios.py",
        "ops/pego_registry.py",
        "ops/pego_doctor.py",
    ]
    env = dict(os.environ)
    env["PYTHONPYCACHEPREFIX"] = "/private/tmp/pego-pycache"
    completed = subprocess.run(
        ["python3", "-m", "py_compile", *scripts],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    if completed.returncode != 0:
        errors.append("python syntax check failed:\n" + completed.stderr.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-markers", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    check_required_files(errors)
    check_private_tracking(errors)
    check_private_ignored(errors)
    check_registry(errors)
    if not args.skip_markers:
        check_tracked_content_markers(errors)
    check_python_syntax(errors)

    if errors:
        print("PEGO doctor failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PEGO doctor passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
