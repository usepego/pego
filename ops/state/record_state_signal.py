#!/usr/bin/env python3
"""Record a protected PEGO state signal.

State signals normalize human state inputs from text, outcomes, wearable
activity, bank account activity, sensors, and future adapters. The runner writes
protected private artifacts and prints only paths by default.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


DOMAINS = {
    "finance",
    "health",
    "career",
    "venture",
    "home_environment",
    "relationships",
    "exploration",
    "happiness",
    "operations",
    "governance",
    "communications",
}
DOMAIN_ALIASES = {"home": "home_environment"}
DOMAIN_CHOICES = sorted(DOMAINS | set(DOMAIN_ALIASES))

SOURCE_TYPES = {
    "manual_text",
    "directive_outcome",
    "wearable_activity",
    "calendar",
    "bank_account_activity",
    "device_sensor",
    "app_usage",
    "location",
    "document",
    "agent_observation",
    "external_api",
    "other",
}

INGESTION_MODES = {"manual", "import", "polling", "webhook", "adapter", "agent_inference"}

SIGNAL_TYPES = {
    "current_state",
    "behavior_observed",
    "activity",
    "sleep",
    "recovery",
    "nutrition",
    "spending",
    "income",
    "account_balance",
    "transaction_pattern",
    "calendar_availability",
    "location_context",
    "environment",
    "mood",
    "energy",
    "goal_progress",
    "risk",
    "blocker",
    "other",
}

EVIDENCE_STRENGTHS = {
    "direct_telemetry",
    "bank_account_activity",
    "human_report",
    "observed_behavior",
    "directive_outcome",
    "external_api",
    "agent_inference",
    "speculation",
}

PRIVACY_CLASSES = {
    "protected_private",
    "sensitive_financial",
    "sensitive_health",
    "safe_to_summarize",
}

RAW_DATA_RETENTION = {"not_stored", "private_local", "external_provider", "unknown"}
DIRECTIONALITY = {"higher_is_better", "lower_is_better", "target_range", "context_only", "unknown"}

AGENT_BY_DOMAIN = {
    "finance": "Finance Agent",
    "health": "Health Agent",
    "career": "Career Agent",
    "venture": "Venture Agent",
    "home_environment": "Home and Environment Agent",
    "relationships": "Relationships Agent",
    "exploration": "Exploration Agent",
    "happiness": "Happiness Agent",
    "operations": "Operations Agent",
    "governance": "Governance Agent",
    "communications": "Communications Agent",
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "state-signal"


def normalize_domain(value: str) -> str:
    normalized = str(value).strip()
    return DOMAIN_ALIASES.get(normalized, normalized)


def split_values(values: list[str]) -> list[str]:
    result = []
    for value in values:
        for part in str(value).replace("\n", ";").split(";"):
            stripped = part.strip()
            if stripped:
                result.append(stripped)
    return result


def parse_measurement(value: str) -> dict[str, str]:
    """Parse name=value[,unit[,window[,directionality]]]."""
    if "=" not in value:
        raise SystemExit(f"measurement must use name=value form: {value}")
    name, rest = value.split("=", 1)
    parts = [part.strip() for part in rest.split(",")]
    direction = parts[3] if len(parts) > 3 and parts[3] else "unknown"
    if direction not in DIRECTIONALITY:
        raise SystemExit(f"invalid measurement directionality: {direction}")
    return {
        "name": name.strip(),
        "value": parts[0],
        "unit": parts[1] if len(parts) > 1 else "",
        "window": parts[2] if len(parts) > 2 else "",
        "directionality": direction,
    }


def default_privacy_class(source_type: str, requested: str) -> str:
    if requested:
        return requested
    if source_type == "bank_account_activity":
        return "sensitive_financial"
    if source_type in {"wearable_activity", "device_sensor"}:
        return "sensitive_health"
    return "protected_private"


def default_evidence_strength(source_type: str, requested: str) -> str:
    if requested:
        return requested
    if source_type == "bank_account_activity":
        return "bank_account_activity"
    if source_type in {"wearable_activity", "device_sensor"}:
        return "direct_telemetry"
    if source_type == "directive_outcome":
        return "directive_outcome"
    return "human_report"


def default_governance_notes(args: argparse.Namespace) -> list[str]:
    notes = split_values(args.governance_notes)
    if args.source_type == "bank_account_activity":
        notes.append(
            "Bank account activity is read-only protected financial evidence; it does not authorize transfers, trades, purchases, debt actions, account changes, or disclosure."
        )
    if args.source_type in {"wearable_activity", "device_sensor"}:
        notes.append(
            "Wearable or sensor telemetry is protected private evidence and should be summarized into directives without creating constant monitoring obligations."
        )
    return notes


def build_artifact(args: argparse.Namespace) -> dict[str, object]:
    privacy_class = default_privacy_class(args.source_type, args.privacy_class)
    evidence_strength = default_evidence_strength(args.source_type, args.evidence_strength)
    domain = normalize_domain(args.domain)
    return {
        "artifact_type": "state_signal",
        "schema_version": 1,
        "date": args.date,
        "observed_at": args.observed_at,
        "source_type": args.source_type,
        "ingestion_mode": args.ingestion_mode,
        "domain": domain,
        "owning_agent": args.owning_agent or AGENT_BY_DOMAIN[domain],
        "signal_type": args.signal_type,
        "summary": args.summary,
        "measurements": [parse_measurement(item) for item in args.measurement],
        "affected_goals": split_values(args.affected_goal),
        "evidence_strength": evidence_strength,
        "confidence": args.confidence,
        "privacy_class": privacy_class,
        "raw_source_reference": args.raw_source_reference,
        "raw_data_retention": args.raw_data_retention,
        "governance_notes": default_governance_notes(args),
        "review_after": args.review_after,
        "expires_after": args.expires_after,
    }


def build_markdown(artifact: dict[str, object]) -> str:
    def bullets(values: object) -> list[str]:
        items = values if isinstance(values, list) else []
        return [f"- {item}" for item in items] or ["- None."]

    measurements = artifact.get("measurements", [])
    rows = []
    for item in measurements if isinstance(measurements, list) else []:
        if not isinstance(item, dict):
            continue
        rows.append(
            "| {name} | {value} | {unit} | {window} | {directionality} |".format(
                name=item.get("name", ""),
                value=item.get("value", ""),
                unit=item.get("unit", ""),
                window=item.get("window", ""),
                directionality=item.get("directionality", ""),
            )
        )
    if not rows:
        rows = ["| None | None | None | None | None |"]

    return "\n".join(
        [
            f"# State Signal: {artifact['date']} - {artifact['domain']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Observed At",
            "",
            str(artifact["observed_at"]),
            "",
            "## Source Type",
            "",
            str(artifact["source_type"]),
            "",
            "## Ingestion Mode",
            "",
            str(artifact["ingestion_mode"]),
            "",
            "## Domain",
            "",
            str(artifact["domain"]),
            "",
            "## Owning Agent",
            "",
            str(artifact["owning_agent"]),
            "",
            "## Signal Type",
            "",
            str(artifact["signal_type"]),
            "",
            "## Summary",
            "",
            str(artifact["summary"]),
            "",
            "## Measurements",
            "",
            "| Name | Value | Unit | Window | Directionality |",
            "| --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Affected Goals",
            "",
            *bullets(artifact["affected_goals"]),
            "",
            "## Evidence Strength",
            "",
            str(artifact["evidence_strength"]),
            "",
            "## Confidence",
            "",
            str(artifact["confidence"]),
            "",
            "## Privacy Class",
            "",
            str(artifact["privacy_class"]),
            "",
            "## Raw Source Reference",
            "",
            str(artifact["raw_source_reference"]),
            "",
            "## Raw Data Retention",
            "",
            str(artifact["raw_data_retention"]),
            "",
            "## Governance Notes",
            "",
            *bullets(artifact["governance_notes"]),
            "",
            "## Review After",
            "",
            str(artifact["review_after"]),
            "",
            "## Expires After",
            "",
            str(artifact["expires_after"]),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--observed-at", default=datetime.now().isoformat(timespec="minutes"))
    parser.add_argument("--source-type", choices=sorted(SOURCE_TYPES), required=True)
    parser.add_argument("--ingestion-mode", choices=sorted(INGESTION_MODES), default="manual")
    parser.add_argument("--domain", choices=DOMAIN_CHOICES, required=True)
    parser.add_argument("--owning-agent", default="")
    parser.add_argument("--signal-type", choices=sorted(SIGNAL_TYPES), required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--measurement", action="append", default=[])
    parser.add_argument("--affected-goal", action="append", default=[])
    parser.add_argument("--evidence-strength", choices=sorted(EVIDENCE_STRENGTHS), default="")
    parser.add_argument("--confidence", choices=["high", "medium", "low"], default="medium")
    parser.add_argument("--privacy-class", choices=sorted(PRIVACY_CLASSES), default="")
    parser.add_argument("--raw-source-reference", default="")
    parser.add_argument("--raw-data-retention", choices=sorted(RAW_DATA_RETENTION), default="not_stored")
    parser.add_argument("--governance-notes", action="append", default=[])
    parser.add_argument("--review-after", default="Next weekly review.")
    parser.add_argument("--expires-after", default="When stale for directive selection.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def display_output(private: Path, path: Path) -> str:
    try:
        return private_root_config.framework_relative_private_path(private, str(path.relative_to(private)))
    except ValueError:
        return str(path)


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.domain = normalize_domain(args.domain)
    slug = slugify(f"{args.domain}-{args.signal_type}-{args.summary}")[:100]
    output = args.output or private / "telemetry" / "signals" / f"{args.date}-{slug}.json"
    artifact = build_artifact(args)
    write_output(output, json.dumps(artifact, indent=2, sort_keys=True) + "\n", args.force)
    print(f"wrote: {display_output(private, output)}")
    if args.markdown_output:
        write_output(args.markdown_output, build_markdown(artifact), args.force)
        print(f"wrote: {display_output(private, args.markdown_output)}")
    return output


if __name__ == "__main__":
    main_with_args()
