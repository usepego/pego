#!/usr/bin/env python3
"""Check protected private PEGO instance readiness without printing private contents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PRIVATE_ROOT = ROOT / "private"

REQUIRED_PATHS = {
    "private_readme": "README.md",
    "active_operating_brief": "active-operating-brief.md",
    "constitution": "constitution/constitution.md",
    "current_state": "current-state/current-state.md",
    "person_profile": "person/profile.md",
    "voice_and_taste": "person/voice-and-taste.md",
    "protected_time": "time/protected-time.md",
    "operating_register": "operator/operating-register.md",
    "writing_dir": "writing",
    "writing_samples_dir": "writing/samples",
    "writing_drafts_dir": "writing/drafts",
    "writing_briefs_dir": "writing/briefs",
    "health_food_options_dir": "health/food-options",
    "health_meal_decisions_dir": "health/meal-decisions",
    "attention_decisions_dir": "attention/decisions",
    "directive_candidates_dir": "directives/candidates",
    "directive_queues_dir": "directives/queues",
    "command_responses_dir": "directives/command-responses",
    "operator_briefs_dir": "operator/briefs",
    "operator_sessions_dir": "operator/sessions",
    "directive_outcomes_dir": "outcomes/directives",
    "session_reviews_dir": "reviews/sessions",
    "context_updates_dir": "context/updates",
    "context_promotions_dir": "context/promotions",
    "governance_preflight_dir": "governance/preflight",
    "governance_reviews_dir": "governance/reviews",
}


def path_status(private_root: Path, relative: str) -> dict:
    path = private_root / relative
    return {
        "relative_path": f"private/{relative}",
        "exists": path.exists(),
        "kind": "directory" if path.is_dir() else "file" if path.is_file() else "missing",
    }


def assess(private_root: Path) -> dict:
    checks = {
        name: path_status(private_root, relative)
        for name, relative in REQUIRED_PATHS.items()
    }
    missing = [
        name
        for name, check in checks.items()
        if not check["exists"]
    ]

    if not private_root.exists():
        decision = "not_ready_missing_state"
    elif missing:
        decision = "ready_with_assumptions"
    else:
        decision = "ready"

    return {
        "artifact_type": "private_instance_readiness",
        "schema_version": 1,
        "decision": decision,
        "private_root": "private/",
        "missing_checks": missing,
        "checks": checks,
        "privacy": {
            "prints_private_contents": False,
            "safe_to_commit": False,
            "note": "Readiness output describes presence of private paths only; keep generated reports under private/.",
        },
        "ready_next_action": ready_next_action(decision, missing),
    }


def ready_next_action(decision: str, missing: list[str]) -> str:
    if decision == "ready":
        return "Proceed to operating-readiness review before issuing a directive."
    if not missing:
        return "Run private instance bootstrap."
    if "active_operating_brief" in missing:
        return "Create or refresh private/active-operating-brief.md."
    if "directive_queues_dir" in missing:
        return "Create private/directives/queues/ or synthesize the first queue."
    if "operator_sessions_dir" in missing:
        return "Create private/operator/sessions/ before USER mode operation."
    return "Run bootstrap or create the missing private operating paths."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-root", type=Path, default=DEFAULT_PRIVATE_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--print", action="store_true", help="print safe readiness JSON")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = assess(args.private_root)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote: {args.output}")
    elif args.print:
        print(json.dumps(result, indent=2))
    else:
        print(f"readiness: {result['decision']}")
        if result["missing_checks"]:
            print(f"missing checks: {len(result['missing_checks'])}")
        print(f"ready next action: {result['ready_next_action']}")
    return result


if __name__ == "__main__":
    main_with_args()
