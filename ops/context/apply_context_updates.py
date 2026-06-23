#!/usr/bin/env python3
"""Review and optionally apply protected context updates to private memory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402

HIGH_IMPACT_CLASSES = {"Goal", "Strategy", "Governance rule"}
STRONG_EVIDENCE = {
    "Direct statement",
    "Repeated statement",
    "Observed behavior",
    "Directive outcome",
    "Telemetry",
    "Professional input",
}
APPLY_STABILITY = {"Stable", "Current but changeable"}
def default_destinations(private_root: Path) -> dict[str, Path]:
    return {
        "Fact": private_root / "person" / "observations.md",
        "Preference": private_root / "person" / "preferences.md",
        "Constraint": private_root / "current-state" / "current-state.md",
        "Pattern": private_root / "person" / "observations.md",
        "Tone rule": private_root / "person" / "voice-and-taste.md",
        "Voice rule": private_root / "person" / "voice-and-taste.md",
        "Taste signal": private_root / "person" / "voice-and-taste.md",
        "Influence": private_root / "person" / "voice-and-taste.md",
        "Public positioning": private_root / "writing" / "positioning.md",
    }


@dataclass(frozen=True)
class ContextUpdate:
    path: Path
    title: str
    date: str
    source: str
    raw_observation: str
    update_class: str
    evidence_strength: str
    stability: str
    destination_file: str
    proposed_update: str
    affected_agents: str
    governance_impact: str
    action: str
    review_date: str


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "memory-application"


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("# Context Update:"):
            sections["Title"] = [line.removeprefix("# Context Update:").strip()]
            continue
        if line.startswith("## "):
            current = line.removeprefix("## ").strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def read_update(path: Path) -> ContextUpdate:
    sections = parse_sections(path.read_text())
    return ContextUpdate(
        path=path,
        title=sections.get("Title", path.stem),
        date=sections.get("Date", ""),
        source=sections.get("Source", ""),
        raw_observation=sections.get("Raw Observation", ""),
        update_class=sections.get("Update Class", ""),
        evidence_strength=sections.get("Evidence Strength", ""),
        stability=sections.get("Stability", ""),
        destination_file=sections.get("Destination File", ""),
        proposed_update=sections.get("Proposed Update", ""),
        affected_agents=sections.get("Affected Agents", ""),
        governance_impact=sections.get("Governance Impact", ""),
        action=sections.get("Action", ""),
        review_date=sections.get("Review Date", ""),
    )


def validate_private_destination(path: Path, private_root: Path) -> None:
    try:
        resolved = path.resolve()
    except FileNotFoundError:
        resolved = path.parent.resolve() / path.name
    resolved_private_root = private_root.resolve()
    if resolved_private_root not in resolved.parents and resolved != resolved_private_root:
        raise SystemExit(f"destination must be under configured private root: {path}")


def destination_for(update: ContextUpdate, args: argparse.Namespace) -> Path | None:
    explicit = update.destination_file.strip()
    if explicit and explicit != "None.":
        return Path(explicit)
    if args.default_destinations:
        return default_destinations(args.private_root_resolved).get(update.update_class)
    return None


def has_governance_impact(update: ContextUpdate) -> bool:
    text = update.governance_impact.strip().lower()
    if update.update_class in HIGH_IMPACT_CLASSES:
        return True
    return bool(text and text not in {"none", "none recorded.", "no governance issue recorded."})


def review_update(update: ContextUpdate, args: argparse.Namespace) -> dict:
    destination = destination_for(update, args)
    reasons: list[str] = []
    if update.action not in {"Update destination", "Record only"}:
        reasons.append(f"unsupported action: {update.action}")
    if update.action == "Record only" and not args.allow_record_only:
        reasons.append("record-only update requires explicit --allow-record-only")
    if update.evidence_strength not in STRONG_EVIDENCE:
        reasons.append(f"weak evidence: {update.evidence_strength}")
    if update.stability not in APPLY_STABILITY:
        reasons.append(f"stability not durable enough: {update.stability}")
    if has_governance_impact(update):
        reasons.append("governance-impacting update requires separate review")
    if not destination:
        reasons.append("no private destination selected")

    decision = "eligible" if not reasons else "defer"
    return {
        "source_update": str(update.path),
        "title": update.title,
        "update_class": update.update_class,
        "evidence_strength": update.evidence_strength,
        "stability": update.stability,
        "action": update.action,
        "destination": str(destination) if destination else "",
        "decision": decision,
        "reasons": reasons,
        "affected_agents": update.affected_agents,
    }


def apply_update(update: ContextUpdate, item: dict, private_root: Path) -> Path:
    destination = Path(str(item["destination"]))
    validate_private_destination(destination, private_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a") as handle:
        handle.write(
            "\n".join(
                [
                    "",
                    f"## Context Update: {update.date or date.today().isoformat()} - {update.title}",
                    "",
                    update.proposed_update,
                    "",
                    f"Source: `{update.path}`",
                    "",
                ]
            )
        )
    return destination


def discover_updates(args: argparse.Namespace) -> list[Path]:
    if args.update:
        return args.update
    if not args.input_dir.exists():
        return []
    return sorted(args.input_dir.glob("*.md"))


def build_review(updates: list[ContextUpdate], items: list[dict], applied: list[Path], args: argparse.Namespace) -> dict:
    return {
        "artifact_type": "memory_application_review",
        "schema_version": 1,
        "date": args.date,
        "source_updates": [str(update.path) for update in updates],
        "eligible_count": sum(1 for item in items if item["decision"] == "eligible"),
        "deferred_count": sum(1 for item in items if item["decision"] != "eligible"),
        "applied_count": len(applied),
        "items": items,
        "applied_destinations": [str(path) for path in applied],
        "apply_requested": args.apply,
        "governance_status": "applied eligible updates" if applied else "review only",
    }


def build_markdown(review: dict) -> str:
    rows = [
        f"| {item['decision']} | {item['title']} | {item['update_class']} | {item['destination'] or 'None'} | {'; '.join(item['reasons']) or 'Eligible'} |"
        for item in review["items"]
    ] or ["| None | None | None | None | No context updates found |"]
    return "\n".join(
        [
            f"# Memory Application Review: {review['date']}",
            "",
            "## Counts",
            "",
            f"- Eligible: {review['eligible_count']}",
            f"- Deferred: {review['deferred_count']}",
            f"- Applied: {review['applied_count']}",
            "",
            "## Updates",
            "",
            "| Decision | Title | Class | Destination | Reason |",
            "| --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Governance Status",
            "",
            review["governance_status"],
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--update", type=Path, action="append", default=[])
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--allow-record-only", action="store_true")
    parser.add_argument("--default-destinations", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.private_root_resolved = private
    args.input_dir = args.input_dir or private / "context" / "updates"
    update_paths = discover_updates(args)
    updates = [read_update(path) for path in update_paths]
    items = [review_update(update, args) for update in updates]
    applied: list[Path] = []
    if args.apply:
        for update, item in zip(updates, items):
            if item["decision"] == "eligible":
                applied.append(apply_update(update, item, private))

    review = build_review(updates, items, applied, args)
    output = args.output or private / "context" / "application-reviews" / f"{args.date}-memory-application.md"
    json_output = args.json_output or private / "context" / "application-reviews" / f"{args.date}-memory-application.json"
    for path, content in [
        (output, build_markdown(review)),
        (json_output, json.dumps(review, indent=2) + "\n"),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {path}")
        path.write_text(content)
        print(f"wrote: {path}")
    print(json.dumps(review, indent=2))
    return review


if __name__ == "__main__":
    main_with_args()
