#!/usr/bin/env python3
"""Review protected PEGO finance scenario output into governance-ready guidance."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


DEFAULT_INPUT = Path("private/_local/finance/scenario-output.json")
DEFAULT_OUTPUT = Path("private/finance/reviews/scenario-review.md")


def validation_status(output: dict) -> str:
    return output.get("validation", {}).get("status", "unknown")


def flagged_scenarios(output: dict) -> list[dict]:
    return output.get("summary", {}).get("flagged_scenarios", [])


def risk_posture(output: dict) -> str:
    if validation_status(output) != "ok":
        return "Blocked"
    flags = flagged_scenarios(output)
    if not flags:
        return "Low"
    flag_count = sum(len(item.get("risk_flags", [])) for item in flags)
    if flag_count >= 4:
        return "High"
    return "Medium"


def primary_risks(output: dict) -> list[str]:
    risks: list[str] = []
    if validation_status(output) != "ok":
        missing = output.get("validation", {}).get("missing_required_scenarios", [])
        risks.append("Missing required scenarios: " + (", ".join(missing) or "unknown"))
    for scenario in flagged_scenarios(output):
        flags = ", ".join(scenario.get("risk_flags", [])) or "unknown"
        risks.append(f"{scenario.get('name', 'unknown')}: {flags}")
    return risks or ["No scenario risk flags recorded."]


def strategy_implication(posture: str) -> str:
    if posture == "Blocked":
        return "Do not use the model for financial directives until required scenarios are present."
    if posture == "High":
        return "Treat finance strategy as unstable; prioritize assumptions, runway, and governance review before major actions."
    if posture == "Medium":
        return "Use the model for low-risk planning, but escalate job, investment, housing, or lifestyle changes before execution."
    return "Use the model for low-risk planning and routine review; still escalate execution decisions."


def directive_candidates(posture: str) -> list[str]:
    if posture == "Blocked":
        return [
            "Add missing required scenarios.",
            "Verify current position inputs are current.",
            "Rerun scenario engine before finance directives.",
        ]
    candidates = [
        "Review risk-flagged scenarios with Finance and Governance agents.",
        "Update assumptions that materially affect target date or runway.",
        "Convert any lifestyle upgrade into a separate candidate scenario before adopting it.",
    ]
    if posture == "High":
        candidates.insert(0, "Create a decision packet before any job, investment, housing, or major spending change.")
    return candidates


def governance_gates() -> list[str]:
    return [
        "No trade, transfer, account change, job change, major purchase, debt action, or housing decision is approved by this review.",
        "Financial execution remains Level 4 unless the private constitution explicitly grants narrower authority.",
        "Any decision relying on speculative equity, Social Security, sale proceeds, aggressive returns, or reduced runway requires governance review.",
        "Any output intended for public or third-party sharing must be sanitized.",
    ]


def data_gaps(output: dict) -> list[str]:
    gaps: list[str] = []
    validation = output.get("validation", {})
    missing = validation.get("missing_required_scenarios", [])
    if missing:
        gaps.append("Missing required scenarios: " + ", ".join(missing))
    if not output.get("results"):
        gaps.append("No scenario results present.")
    for result in output.get("results", []):
        if result.get("months_to_target") is None:
            gaps.append(f"{result.get('name', 'unknown')}: target not reached within model window.")
    return gaps or ["No structural data gaps detected by the review runner."]


def bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def build_review(output: dict, source: Path, review_date: str) -> str:
    posture = risk_posture(output)
    return "\n".join(
        [
            f"# Finance Scenario Review: {review_date}",
            "",
            "## Date",
            "",
            review_date,
            "",
            "## Source Output",
            "",
            str(source),
            "",
            "## Validation Status",
            "",
            validation_status(output),
            "",
            "## Scenario Coverage",
            "",
            f"- Required scenarios: {', '.join(output.get('validation', {}).get('required_scenarios', [])) or 'unknown'}",
            f"- Present scenarios: {', '.join(output.get('validation', {}).get('present_scenarios', [])) or 'unknown'}",
            f"- Missing scenarios: {', '.join(output.get('validation', {}).get('missing_required_scenarios', [])) or 'none'}",
            "",
            "## Risk Posture",
            "",
            posture,
            "",
            "## Primary Risks",
            "",
            *bullets(primary_risks(output)),
            "",
            "## Strategy Implication",
            "",
            strategy_implication(posture),
            "",
            "## Directive Candidates",
            "",
            *bullets(directive_candidates(posture)),
            "",
            "## Governance Gates",
            "",
            *bullets(governance_gates()),
            "",
            "## Data Gaps",
            "",
            *bullets(data_gaps(output)),
            "",
            "## Agent Routing",
            "",
            "Finance, Governance, Career, Venture, Operations, Happiness.",
            "",
            "## Next Review",
            "",
            "Next finance review, material assumption change, or before any high-impact financial directive.",
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.input.is_file():
        raise SystemExit(f"missing scenario output: {args.input}")
    output = json.loads(args.input.read_text())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {args.output}")
    args.output.write_text(build_review(output, args.input, args.date))
    print(f"wrote: {args.output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
