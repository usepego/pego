#!/usr/bin/env python3
"""Update protected PEGO goal progress from normalized state signals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any


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
CONFIDENCE = {"high", "medium", "low"}
TRAJECTORIES = {"improving", "stable", "worsening", "mixed", "unknown"}
PROGRESS_STATUSES = {"on_track", "at_risk", "stalled", "unknown"}

LEADING_SIGNAL_TYPES = {
    "behavior_observed",
    "activity",
    "sleep",
    "recovery",
    "nutrition",
    "transaction_pattern",
    "calendar_availability",
    "location_context",
    "environment",
    "mood",
    "energy",
    "risk",
    "blocker",
}
LAGGING_SIGNAL_TYPES = {
    "current_state",
    "spending",
    "income",
    "account_balance",
    "goal_progress",
}
LAGGING_SOURCE_TYPES = {
    "directive_outcome",
    "bank_account_activity",
}
LEADING_SOURCE_TYPES = {
    "wearable_activity",
    "calendar",
    "device_sensor",
    "app_usage",
}
NEGATIVE_SIGNAL_TYPES = {"risk", "blocker"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "goal-progress"


def normalize_domain(value: object) -> str:
    normalized = str(value or "").strip()
    return DOMAIN_ALIASES.get(normalized, normalized)


def read_state_signal(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"signal is not valid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("artifact_type") != "state_signal":
        raise SystemExit(f"signal must declare artifact_type state_signal: {path}")
    return data


def normalize_confidence(value: object, default: str = "medium") -> str:
    normalized = str(value or default).lower().strip()
    if normalized not in CONFIDENCE:
        raise SystemExit(f"invalid confidence: {value}")
    return normalized


def parse_date(value: object) -> date | None:
    if value in ("", None):
        return None
    text = str(value).strip()
    if len(text) >= 10:
        text = text[:10]
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def display_source(private: Path, path: Path) -> str:
    try:
        relative = path.expanduser().resolve().relative_to(private.expanduser().resolve())
    except ValueError:
        return str(path)
    return private_root_config.framework_relative_private_path(private, str(relative))


def unique_ordered(values: list[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value and value not in seen:
            output.append(value)
            seen.add(value)
    return output


def parse_compact_indicator(value: str) -> dict[str, object]:
    pairs: dict[str, object] = {}
    for part in value.split(";"):
        if not part.strip():
            continue
        if "=" not in part:
            raise SystemExit(
                "manual indicator must be JSON or semicolon-delimited key=value fields"
            )
        key, item = part.split("=", 1)
        pairs[key.strip()] = item.strip()
    if "name" not in pairs and "value" not in pairs and len(pairs) == 1:
        name, item = next(iter(pairs.items()))
        pairs = {"name": name, "value": item}
    return pairs


def parse_manual_indicator(raw: str, indicator_type: str, default_date: str) -> dict[str, str]:
    if raw.strip().startswith("{"):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"manual indicator is not valid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise SystemExit("manual indicator JSON must be an object")
        data = parsed
    else:
        data = parse_compact_indicator(raw)

    name = str(data.get("name", "")).strip()
    value = str(data.get("value", "")).strip()
    if not name or not value:
        raise SystemExit("manual indicator requires name and value")

    return {
        "name": name,
        "value": value,
        "unit": str(data.get("unit", "")),
        "indicator_type": indicator_type,
        "source_signal": str(data.get("source_signal") or data.get("source") or "manual"),
        "confidence": normalize_confidence(data.get("confidence", "medium")),
        "updated_at": str(data.get("updated_at") or default_date),
    }


def indicator_type_for_signal(signal: dict[str, Any]) -> str:
    signal_type = str(signal.get("signal_type", "other"))
    source_type = str(signal.get("source_type", "other"))
    if signal_type in LEADING_SIGNAL_TYPES:
        return "leading"
    if signal_type in LAGGING_SIGNAL_TYPES:
        return "lagging"
    if source_type in LAGGING_SOURCE_TYPES:
        return "lagging"
    if source_type in LEADING_SOURCE_TYPES:
        return "leading"
    return "leading"


def indicators_from_signal(
    signal: dict[str, Any],
    source_signal: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    leading: list[dict[str, str]] = []
    lagging: list[dict[str, str]] = []
    default_type = indicator_type_for_signal(signal)
    updated_at = str(signal.get("observed_at") or signal.get("date") or "")
    confidence = normalize_confidence(signal.get("confidence", "low"), default="low")

    measurements = signal.get("measurements", [])
    if not isinstance(measurements, list):
        raise SystemExit(f"signal measurements must be a list: {source_signal}")

    for measurement in measurements:
        if not isinstance(measurement, dict):
            raise SystemExit(f"signal measurement must be an object: {source_signal}")
        name = str(measurement.get("name", "")).strip()
        value = str(measurement.get("value", "")).strip()
        if not name or not value:
            continue
        indicator_type = str(measurement.get("indicator_type") or default_type).strip()
        if indicator_type not in {"leading", "lagging"}:
            indicator_type = default_type
        indicator = {
            "name": name,
            "value": value,
            "unit": str(measurement.get("unit", "")),
            "indicator_type": indicator_type,
            "source_signal": source_signal,
            "confidence": confidence,
            "updated_at": updated_at,
        }
        if indicator_type == "lagging":
            lagging.append(indicator)
        else:
            leading.append(indicator)
    return leading, lagging


def infer_domain(domain: str | None, signals: list[dict[str, Any]]) -> str:
    signal_domains = unique_ordered(
        [normalize_domain(signal.get("domain", "")) for signal in signals]
    )
    invalid = [value for value in signal_domains if value not in DOMAINS]
    if invalid:
        raise SystemExit(f"signal has invalid domain: {invalid[0]}")
    if domain:
        normalized_domain = normalize_domain(domain)
        if normalized_domain not in DOMAINS:
            raise SystemExit(f"invalid domain: {domain}")
        mismatched = [value for value in signal_domains if value and value != normalized_domain]
        if mismatched:
            raise SystemExit(
                f"signal domain {mismatched[0]} does not match requested domain {normalized_domain}"
            )
        return normalized_domain
    if len(signal_domains) == 1:
        return signal_domains[0]
    if not signal_domains:
        raise SystemExit("domain is required when no state signals are supplied")
    raise SystemExit("signals must belong to one domain unless --domain selects it")


def infer_owning_agent(
    owning_agent: str | None,
    domain: str,
    signals: list[dict[str, Any]],
) -> str:
    if owning_agent:
        return owning_agent
    agents = unique_ordered([str(signal.get("owning_agent", "")) for signal in signals])
    if len(agents) == 1:
        return agents[0]
    return AGENT_BY_DOMAIN[domain]


def infer_goal(goal: str | None, domain: str, signals: list[dict[str, Any]]) -> str:
    if goal:
        return goal
    affected_goals: list[str] = []
    for signal in signals:
        values = signal.get("affected_goals", [])
        if isinstance(values, list):
            affected_goals.extend(str(value) for value in values if value)
    unique_goals = unique_ordered(affected_goals)
    if len(unique_goals) == 1:
        return unique_goals[0]
    return f"{domain.replace('_', ' ').title()} goal progress"


def latest_evidence_date(
    review_date: date,
    signals: list[dict[str, Any]],
    indicators: list[dict[str, str]],
) -> date | None:
    dates = []
    for signal in signals:
        dates.append(parse_date(signal.get("observed_at")) or parse_date(signal.get("date")))
    for indicator in indicators:
        dates.append(parse_date(indicator.get("updated_at")))
    usable = [value for value in dates if value is not None and value <= review_date]
    return max(usable) if usable else None


def compute_confidence(
    signals: list[dict[str, Any]],
    indicators: list[dict[str, str]],
    stale: bool,
    has_leading: bool,
    has_lagging: bool,
) -> str:
    if stale or not indicators:
        return "low"
    values = [normalize_confidence(signal.get("confidence", "low"), default="low") for signal in signals]
    values.extend(indicator["confidence"] for indicator in indicators)
    if "low" in values:
        base = "low"
    elif "medium" in values:
        base = "medium"
    else:
        base = "high"
    if not has_leading or not has_lagging:
        return "medium" if base == "high" else base
    return base


def infer_trajectory(
    signals: list[dict[str, Any]],
    has_leading: bool,
    has_lagging: bool,
) -> str:
    if not has_leading and not has_lagging:
        return "unknown"
    negative = any(str(signal.get("signal_type", "")) in NEGATIVE_SIGNAL_TYPES for signal in signals)
    positive = any(str(signal.get("signal_type", "")) not in NEGATIVE_SIGNAL_TYPES for signal in signals)
    if negative and positive:
        return "mixed"
    if negative:
        return "worsening"
    if has_leading and has_lagging:
        return "improving"
    return "stable"


def infer_progress_status(
    signals: list[dict[str, Any]],
    confidence: str,
    trajectory: str,
    has_leading: bool,
    has_lagging: bool,
) -> str:
    signal_types = {str(signal.get("signal_type", "")) for signal in signals}
    if "blocker" in signal_types:
        return "stalled"
    if "risk" in signal_types or trajectory == "worsening":
        return "at_risk"
    if confidence == "low":
        return "unknown"
    if has_leading and has_lagging:
        return "on_track"
    return "unknown"


def next_measurement_need(
    supplied: str | None,
    domain: str,
    stale: bool,
    stale_after_days: int,
    has_leading: bool,
    has_lagging: bool,
) -> str:
    if supplied:
        return supplied
    if stale:
        return (
            f"Refresh {domain} state signals before directive selection; latest usable "
            f"evidence is older than {stale_after_days} days or missing."
        )
    if not has_leading and not has_lagging:
        return f"Add one leading and one lagging {domain} indicator before relying on this model."
    if not has_leading:
        return f"Add a leading behavior or input indicator for {domain}."
    if not has_lagging:
        return f"Add a lagging outcome indicator for {domain}."
    return "Review after the next directive outcome or scheduled domain check-in."


def collect_governance_notes(
    signals: list[dict[str, Any]],
    explicit_notes: list[str],
) -> list[str]:
    notes = list(explicit_notes)
    for signal in signals:
        signal_notes = signal.get("governance_notes", [])
        if isinstance(signal_notes, list):
            notes.extend(str(note) for note in signal_notes if note)
        privacy_class = str(signal.get("privacy_class", ""))
        if privacy_class == "sensitive_health":
            notes.append("Sensitive health signal; keep raw telemetry in protected private storage.")
        elif privacy_class == "sensitive_financial":
            notes.append("Sensitive financial signal; keep raw account activity in protected private storage.")
        elif privacy_class == "protected_private":
            notes.append("Protected private signal; do not export raw operating memory.")
    notes.append("Goal progress is private operating memory and does not approve high-impact action.")
    return unique_ordered(notes)


def collect_directive_attribution(
    signals_and_sources: list[tuple[dict[str, Any], str]],
    explicit_directives: list[str],
) -> list[str]:
    attributions = list(explicit_directives)
    for signal, source_signal in signals_and_sources:
        if signal.get("source_type") == "directive_outcome":
            attribution = str(signal.get("raw_source_reference") or source_signal)
            attributions.append(attribution)
    return unique_ordered(attributions)


def current_state_summary(domain: str, signals: list[dict[str, Any]]) -> str:
    if not signals:
        return f"No normalized {domain} state signal was supplied; this model depends on manual indicators."
    summaries = []
    for signal in signals:
        observed = str(signal.get("observed_at") or signal.get("date") or "unknown date")
        source = str(signal.get("source_type") or "unknown source").replace("_", " ")
        signal_type = str(signal.get("signal_type") or "unknown signal").replace("_", " ")
        summary = str(signal.get("summary") or "No summary supplied.")
        summaries.append(f"{observed} {source}/{signal_type}: {summary}")
    return " ".join(summaries)


def build_artifact(
    *,
    private: Path,
    output_date: str,
    domain: str | None,
    owning_agent: str | None,
    goal: str | None,
    goal_id: str | None,
    signal_paths: list[Path],
    manual_leading: list[str],
    manual_lagging: list[str],
    explicit_directives: list[str],
    explicit_governance_notes: list[str],
    supplied_trajectory: str | None,
    supplied_confidence: str | None,
    supplied_progress_status: str | None,
    supplied_next_measurement_need: str | None,
    review_after: str | None,
    stale_after_days: int,
) -> dict[str, object]:
    signals_and_sources: list[tuple[dict[str, Any], str]] = []
    signals = []
    for path in signal_paths:
        signal = read_state_signal(path)
        source_signal = display_source(private, path)
        signals_and_sources.append((signal, source_signal))
        signals.append(signal)

    resolved_domain = infer_domain(domain, signals)
    resolved_goal = infer_goal(goal, resolved_domain, signals)
    resolved_goal_id = goal_id or slugify(resolved_goal)
    resolved_agent = infer_owning_agent(owning_agent, resolved_domain, signals)

    leading: list[dict[str, str]] = []
    lagging: list[dict[str, str]] = []
    for signal, source_signal in signals_and_sources:
        signal_leading, signal_lagging = indicators_from_signal(signal, source_signal)
        leading.extend(signal_leading)
        lagging.extend(signal_lagging)

    leading.extend(
        parse_manual_indicator(value, "leading", output_date)
        for value in manual_leading
    )
    lagging.extend(
        parse_manual_indicator(value, "lagging", output_date)
        for value in manual_lagging
    )

    all_indicators = leading + lagging
    review_day = date.fromisoformat(output_date)
    latest = latest_evidence_date(review_day, signals, all_indicators)
    stale = latest is None or (review_day - latest).days > stale_after_days
    has_leading = bool(leading)
    has_lagging = bool(lagging)

    computed_confidence = compute_confidence(
        signals,
        all_indicators,
        stale,
        has_leading,
        has_lagging,
    )
    confidence = supplied_confidence or computed_confidence
    if confidence not in CONFIDENCE:
        raise SystemExit(f"invalid confidence: {confidence}")

    trajectory = supplied_trajectory or infer_trajectory(signals, has_leading, has_lagging)
    if trajectory not in TRAJECTORIES:
        raise SystemExit(f"invalid trajectory: {trajectory}")

    progress_status = supplied_progress_status or infer_progress_status(
        signals,
        confidence,
        trajectory,
        has_leading,
        has_lagging,
    )
    if progress_status not in PROGRESS_STATUSES:
        raise SystemExit(f"invalid progress_status: {progress_status}")

    next_need = next_measurement_need(
        supplied_next_measurement_need,
        resolved_domain,
        stale,
        stale_after_days,
        has_leading,
        has_lagging,
    )
    resolved_review_after = review_after or (review_day + timedelta(days=7)).isoformat()

    return {
        "artifact_type": "goal_progress",
        "schema_version": 1,
        "date": output_date,
        "domain": resolved_domain,
        "owning_agent": resolved_agent,
        "goal": resolved_goal,
        "goal_id": resolved_goal_id,
        "source_signals": [source for _, source in signals_and_sources],
        "current_state_summary": current_state_summary(resolved_domain, signals),
        "leading_indicators": leading,
        "lagging_indicators": lagging,
        "trajectory": trajectory,
        "confidence": confidence,
        "progress_status": progress_status,
        "directive_attribution": collect_directive_attribution(
            signals_and_sources,
            explicit_directives,
        ),
        "next_measurement_need": next_need,
        "governance_notes": collect_governance_notes(signals, explicit_governance_notes),
        "review_after": resolved_review_after,
    }


def clean_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/").strip()


def bullet_rows(values: object) -> list[str]:
    items = values if isinstance(values, list) else []
    return [f"- {clean_cell(item)}" for item in items] or ["- None."]


def indicator_rows(indicators: object) -> list[str]:
    rows = []
    for indicator in indicators if isinstance(indicators, list) else []:
        if not isinstance(indicator, dict):
            continue
        rows.append(
            "| {name} | {value} | {unit} | {source} | {confidence} | {updated_at} |".format(
                name=clean_cell(indicator.get("name", "")),
                value=clean_cell(indicator.get("value", "")),
                unit=clean_cell(indicator.get("unit", "")),
                source=clean_cell(indicator.get("source_signal", "")),
                confidence=clean_cell(indicator.get("confidence", "")),
                updated_at=clean_cell(indicator.get("updated_at", "")),
            )
        )
    return rows or ["| None | n/a | n/a | n/a | n/a | n/a |"]


def build_markdown(artifact: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Goal Progress: {artifact['domain']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Domain",
            "",
            str(artifact["domain"]).title(),
            "",
            "## Owning Agent",
            "",
            str(artifact["owning_agent"]),
            "",
            "## Goal",
            "",
            str(artifact["goal"]),
            "",
            "## Goal ID",
            "",
            str(artifact["goal_id"]),
            "",
            "## Source Signals",
            "",
            *bullet_rows(artifact["source_signals"]),
            "",
            "## Current State Summary",
            "",
            str(artifact["current_state_summary"]),
            "",
            "## Leading Indicators",
            "",
            "| Name | Value | Unit | Source Signal | Confidence | Updated At |",
            "| --- | --- | --- | --- | --- | --- |",
            *indicator_rows(artifact["leading_indicators"]),
            "",
            "## Lagging Indicators",
            "",
            "| Name | Value | Unit | Source Signal | Confidence | Updated At |",
            "| --- | --- | --- | --- | --- | --- |",
            *indicator_rows(artifact["lagging_indicators"]),
            "",
            "## Trajectory",
            "",
            str(artifact["trajectory"]).replace("_", " ").title(),
            "",
            "## Confidence",
            "",
            str(artifact["confidence"]).title(),
            "",
            "## Progress Status",
            "",
            str(artifact["progress_status"]).replace("_", " ").title(),
            "",
            "## Directive Attribution",
            "",
            *bullet_rows(artifact["directive_attribution"]),
            "",
            "## Next Measurement Need",
            "",
            str(artifact["next_measurement_need"]),
            "",
            "## Governance Notes",
            "",
            *bullet_rows(artifact["governance_notes"]),
            "",
            "## Review After",
            "",
            str(artifact["review_after"]),
            "",
        ]
    )


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def output_path(private: Path, path: Path) -> str:
    try:
        relative = path.expanduser().resolve().relative_to(private.expanduser().resolve())
    except ValueError:
        return str(path)
    return private_root_config.framework_relative_private_path(private, str(relative))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--domain", choices=DOMAIN_CHOICES)
    parser.add_argument("--owning-agent")
    parser.add_argument("--goal")
    parser.add_argument("--goal-id")
    parser.add_argument("--signal", action="append", type=Path, default=[])
    parser.add_argument(
        "--leading-indicator",
        action="append",
        default=[],
        help="JSON object or semicolon-delimited name=value fields.",
    )
    parser.add_argument(
        "--lagging-indicator",
        action="append",
        default=[],
        help="JSON object or semicolon-delimited name=value fields.",
    )
    parser.add_argument("--directive", action="append", default=[])
    parser.add_argument("--governance-note", action="append", default=[])
    parser.add_argument("--trajectory", choices=sorted(TRAJECTORIES))
    parser.add_argument("--confidence", choices=sorted(CONFIDENCE))
    parser.add_argument("--progress-status", choices=sorted(PROGRESS_STATUSES))
    parser.add_argument("--next-measurement-need")
    parser.add_argument("--review-after")
    parser.add_argument("--stale-after-days", type=int, default=14)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    artifact = build_artifact(
        private=private,
        output_date=args.date,
        domain=args.domain,
        owning_agent=args.owning_agent,
        goal=args.goal,
        goal_id=args.goal_id,
        signal_paths=args.signal,
        manual_leading=args.leading_indicator,
        manual_lagging=args.lagging_indicator,
        explicit_directives=args.directive,
        explicit_governance_notes=args.governance_note,
        supplied_trajectory=args.trajectory,
        supplied_confidence=args.confidence,
        supplied_progress_status=args.progress_status,
        supplied_next_measurement_need=args.next_measurement_need,
        review_after=args.review_after,
        stale_after_days=args.stale_after_days,
    )
    domain = str(artifact["domain"])
    args.output = args.output or private / "goals" / "progress" / f"{domain}.md"
    args.json_output = args.json_output or private / "goals" / "progress" / f"{domain}.json"

    write_output(args.output, build_markdown(artifact), args.force)
    write_output(
        args.json_output,
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        args.force,
    )
    print(f"wrote: {output_path(private, args.output)}")
    print(f"wrote: {output_path(private, args.json_output)}")
    return args.output


if __name__ == "__main__":
    main_with_args()
