#!/usr/bin/env python3
"""Promote session-review context candidates into protected context updates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))
sys.path.insert(0, str(ROOT / "ops" / "context"))

import private_root as private_root_config  # noqa: E402
import record_context_update  # noqa: E402


VALID_SOURCES = record_context_update.SOURCES
VALID_UPDATE_CLASSES = record_context_update.UPDATE_CLASSES
VALID_EVIDENCE_STRENGTHS = record_context_update.EVIDENCE_STRENGTHS
VALID_STABILITY = record_context_update.STABILITY
VALID_ACTIONS = record_context_update.ACTIONS


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "context-update"


def load_session_review(path: Path) -> dict:
    data = json.loads(path.read_text())
    if data.get("artifact_type") != "session_review":
        raise SystemExit(f"expected session_review artifact: {path}")
    return data


def clean_choice(value: object, valid: set[str], fallback: str) -> str:
    text = str(value or "").strip()
    if text in valid:
        return text
    return fallback


def candidate_args(
    candidate: dict,
    review: dict,
    index: int,
    args: argparse.Namespace,
) -> list[str]:
    proposed_update = str(candidate.get("proposed_update", "")).strip()
    title = str(candidate.get("title") or proposed_update or f"Session context {index}").strip()
    output = args.output_dir / f"{args.date}-session-{index:02d}-{slugify(title)}.md"
    raw_observation = (
        f"Session review {review.get('source_session', 'unknown session')} proposed "
        f"context update: {proposed_update or 'Not supplied.'}"
    )
    return [
        "--date",
        args.date,
        "--private-root",
        str(args.private_root_resolved),
        "--title",
        title[:80],
        "--source",
        clean_choice(candidate.get("source"), VALID_SOURCES, "Outcome"),
        "--raw-observation",
        raw_observation,
        "--update-class",
        clean_choice(candidate.get("update_class"), VALID_UPDATE_CLASSES, "Pattern"),
        "--evidence-strength",
        clean_choice(candidate.get("evidence_strength"), VALID_EVIDENCE_STRENGTHS, "Directive outcome"),
        "--stability",
        clean_choice(candidate.get("stability"), VALID_STABILITY, "Provisional"),
        "--proposed-update",
        proposed_update or "Session review produced an unspecified context update candidate.",
        "--affected-agents",
        str(candidate.get("affected_agents") or "Operations"),
        "--action",
        clean_choice(candidate.get("action"), VALID_ACTIONS, "Record only"),
        "--review-date",
        str(review.get("next_review") or "Next weekly review."),
        "--output",
        str(output),
        "--force",
    ]


def build_summary(review: dict, outputs: list[Path], args: argparse.Namespace) -> dict:
    return {
        "artifact_type": "session_context_promotion",
        "schema_version": 1,
        "date": args.date,
        "source_review": str(args.review),
        "candidate_count": len(review.get("context_update_candidates", [])),
        "promoted_count": len(outputs),
        "outputs": [str(path) for path in outputs],
        "privacy": "protected-private-instance",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.private_root_resolved = private
    args.review = args.review or private / "reviews" / "sessions" / f"{args.date}-session-review.json"
    args.output_dir = args.output_dir or private / "context" / "updates"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    review = load_session_review(args.review)
    outputs: list[Path] = []
    for index, candidate in enumerate(review.get("context_update_candidates", []), start=1):
        if not isinstance(candidate, dict):
            continue
        output = record_context_update.main_with_args(candidate_args(candidate, review, index, args))
        outputs.append(output)

    summary = build_summary(review, outputs, args)
    summary_output = args.summary_output or (
        private / "context" / "promotions" / f"{args.date}-session-context-promotion.json"
    )
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    if summary_output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {summary_output}")
    summary_output.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"wrote: {summary_output}")
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main_with_args()
