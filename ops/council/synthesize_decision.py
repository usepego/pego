#!/usr/bin/env python3
"""Synthesize PEGO agent recommendations into a council decision."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402
RISK_WORDS = {
    "financial",
    "health",
    "relationship",
    "career",
    "legal",
    "tax",
    "privacy",
    "reputation",
    "time",
    "energy",
    "psychological",
    "opportunity_cost",
}


@dataclass(frozen=True)
class Recommendation:
    source: str
    agent: str
    recommendation_type: str
    proposed_directive: str
    authority_level: str
    expected_benefit: str
    risks: list[str]
    required_handoffs: list[str]
    dissent: str
    stop_conditions: list[str]
    review: str


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.removeprefix("## ").strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def first_line(value: str, fallback: str = "") -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return fallback


def split_values(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if not value:
        return []
    return [part.strip() for part in str(value).replace("\n", ";").split(";") if part.strip()]


def normalize_risks(values: object) -> list[str]:
    risks = []
    for value in split_values(values):
        normalized = value.strip().lower().replace(" ", "_").replace("-", "_")
        if normalized in RISK_WORDS and normalized not in risks:
            risks.append(normalized)
    return risks


def read_recommendation(path: Path) -> Recommendation:
    text = path.read_text()
    if path.suffix == ".json":
        data = json.loads(text)
        if data.get("artifact_type") != "agent_recommendation":
            raise SystemExit(f"not an agent recommendation: {path}")
        review = data.get("review", {})
        return Recommendation(
            source=str(path),
            agent=str(data.get("agent", "Unknown")),
            recommendation_type=str(data.get("recommendation_type", "recommend")),
            proposed_directive=str(data.get("proposed_directive", "")),
            authority_level=str(data.get("authority_level", "level_1_recommend")),
            expected_benefit=str(data.get("expected_benefit", "")),
            risks=normalize_risks(data.get("risks", [])),
            required_handoffs=split_values(data.get("required_handoffs", [])),
            dissent=str(data.get("dissent", "")),
            stop_conditions=split_values(data.get("stop_conditions", [])),
            review=str(review.get("review_date_or_success_criteria", "")),
        )

    sections = parse_sections(text)
    return Recommendation(
        source=str(path),
        agent=first_line(sections.get("Agent", ""), "Unknown"),
        recommendation_type=first_line(sections.get("Recommendation Type", ""), "Recommend").lower().replace(" ", "_"),
        proposed_directive=first_line(sections.get("Proposed Directive", ""), path.stem),
        authority_level=first_line(sections.get("Authority Level", ""), "Level 1"),
        expected_benefit=first_line(sections.get("Expected Benefit", ""), ""),
        risks=normalize_risks(sections.get("Risks", "")),
        required_handoffs=split_values(sections.get("Required Handoffs", "")),
        dissent=sections.get("Dissent", ""),
        stop_conditions=split_values(sections.get("Stop Conditions", "")),
        review=first_line(sections.get("Review Date or Success Criteria", ""), "Next review."),
    )


def outcome(recommendations: list[Recommendation]) -> str:
    if any(item.recommendation_type == "dissent" for item in recommendations):
        return "revise"
    if any(item.recommendation_type == "request_more_information" for item in recommendations):
        return "request_more_information"
    if any(item.recommendation_type == "escalate" for item in recommendations):
        return "escalate"
    if any("level_4" in item.authority_level.lower() or "level 4" in item.authority_level.lower() for item in recommendations):
        return "escalate"
    high_risks = {"financial", "health", "relationship", "career", "legal", "tax", "privacy"}
    if any(high_risks.intersection(item.risks) for item in recommendations):
        return "escalate"
    return "adopt"


def choose_directive(recommendations: list[Recommendation]) -> str:
    for item in recommendations:
        if item.recommendation_type in {"recommend", "direct"} and item.proposed_directive:
            return item.proposed_directive
    return recommendations[0].proposed_directive or "Request more information."


def build_artifact(recommendations: list[Recommendation], decision_date: str, frame: str) -> dict[str, object]:
    if not recommendations:
        raise SystemExit("at least one recommendation is required")
    council_outcome = outcome(recommendations)
    directive = choose_directive(recommendations)
    risks = sorted({risk for item in recommendations for risk in item.risks})
    dissent = [
        f"{item.agent}: {item.dissent}"
        for item in recommendations
        if item.dissent or item.recommendation_type == "dissent"
    ]
    handoffs = sorted({handoff for item in recommendations for handoff in item.required_handoffs})
    stops = sorted({stop for item in recommendations for stop in item.stop_conditions})
    if council_outcome == "adopt":
        governance = "Level 1 council synthesis; no authority increase approved."
        next_action = directive
    elif council_outcome == "revise":
        governance = "Council dissent preserved; revise before directive synthesis."
        next_action = "Revise the directive and rerun council synthesis."
    elif council_outcome == "request_more_information":
        governance = "Insufficient decision-grade evidence."
        next_action = "Ask the targeted information request before directive synthesis."
    else:
        governance = "Governance review required before adoption or execution."
        next_action = "Create or update a decision packet before adoption."

    return {
        "artifact_type": "council_decision",
        "schema_version": 1,
        "date": decision_date,
        "decision_frame": frame,
        "source_recommendations": [item.source for item in recommendations],
        "proposed_directive": directive,
        "council_outcome": council_outcome,
        "rationale": "Synthesized from agent recommendations while preserving dissent, risks, handoffs, and authority constraints.",
        "expected_benefit": " | ".join(item.expected_benefit for item in recommendations if item.expected_benefit),
        "key_risks": risks,
        "dissent": dissent,
        "required_handoffs": handoffs,
        "governance_status": governance,
        "stop_conditions": stops,
        "next_action": next_action,
        "review": "; ".join(item.review for item in recommendations if item.review) or "Next council review.",
    }


def build_markdown(artifact: dict[str, object]) -> str:
    def bullets(values: object) -> list[str]:
        items = values if isinstance(values, list) else []
        return [f"- {item}" for item in items] or ["- None."]

    return "\n".join(
        [
            f"# Council Decision: {artifact['date']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Decision Frame",
            "",
            str(artifact["decision_frame"]),
            "",
            "## Source Recommendations",
            "",
            *bullets(artifact["source_recommendations"]),
            "",
            "## Proposed Directive",
            "",
            str(artifact["proposed_directive"]),
            "",
            "## Council Outcome",
            "",
            str(artifact["council_outcome"]),
            "",
            "## Rationale",
            "",
            str(artifact["rationale"]),
            "",
            "## Expected Benefit",
            "",
            str(artifact["expected_benefit"]),
            "",
            "## Key Risks",
            "",
            *bullets(artifact["key_risks"]),
            "",
            "## Dissent",
            "",
            *bullets(artifact["dissent"]),
            "",
            "## Required Handoffs",
            "",
            *bullets(artifact["required_handoffs"]),
            "",
            "## Governance Status",
            "",
            str(artifact["governance_status"]),
            "",
            "## Stop Conditions",
            "",
            *bullets(artifact["stop_conditions"]),
            "",
            "## Next Action",
            "",
            str(artifact["next_action"]),
            "",
            "## Review",
            "",
            str(artifact["review"]),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--frame", default="Council synthesis of current agent recommendations.")
    parser.add_argument("--recommendation", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.output = args.output or private / "council" / "decisions" / "council-decision.md"
    if not args.recommendation:
        raise SystemExit("at least one --recommendation file is required")
    recommendations = [read_recommendation(path) for path in args.recommendation]
    artifact = build_artifact(recommendations, args.date, args.frame)
    write_output(args.output, build_markdown(artifact), args.force)
    print(f"wrote: {args.output}")
    if args.json_output:
        write_output(args.json_output, json.dumps(artifact, indent=2, sort_keys=True) + "\n", args.force)
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
