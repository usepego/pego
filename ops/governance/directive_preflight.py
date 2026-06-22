#!/usr/bin/env python3
"""Run a conservative governance preflight for a PEGO directive.

The preflight classifies a directive as:

- pass: low-risk Level 1 style recommendation.
- needs_review: requires light or standard review before adoption.
- escalate: should become a decision packet or formal review item.

It intentionally does not print directive content, because directives may be
private. It reports only derived classifications and generic reasons.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


HIGH_IMPACT_PATTERNS = {
    "financial_execution": [
        r"\btrade\b",
        r"\bbuy stock\b",
        r"\bsell stock\b",
        r"\binvest\b",
        r"\btransfer\b",
        r"\bwire\b",
        r"\bwithdraw\b",
        r"\bliquidate\b",
        r"\bexercise options?\b",
    ],
    "career": [
        r"\bquit\b",
        r"\bresign\b",
        r"\bchange jobs?\b",
        r"\bjob offer\b",
        r"\bnegotiate compensation\b",
        r"\bpublic venture\b",
    ],
    "health_medical": [
        r"\bmedication\b",
        r"\bdiagnos",
        r"\btreatment\b",
        r"\bfast for\b",
        r"\bcalorie deficit\b",
        r"\binjury\b",
        r"\bdoctor\b",
    ],
    "legal_tax": [
        r"\blegal\b",
        r"\blawyer\b",
        r"\battorney\b",
        r"\btax\b",
        r"\bcontract\b",
        r"\bliability\b",
    ],
    "housing": [
        r"\bmove\b",
        r"\bsell (the )?house\b",
        r"\bbuy (a )?house\b",
        r"\brenovation\b",
        r"\bcontractor\b",
        r"\bproperty\b",
    ],
    "privacy": [
        r"\bshare\b",
        r"\bpublic\b",
        r"\bpublish\b",
        r"\boauth\b",
        r"\bapi key\b",
        r"\btoken\b",
        r"\bthird part(y|ies)\b",
        r"\bgithub\b",
    ],
    "relationship_stakeholder": [
        r"\bspouse\b",
        r"\bpartner\b",
        r"\bfamily\b",
        r"\bhousehold\b",
    ],
}

REVIEW_PATTERNS = {
    "recurrence": [r"\bdaily\b", r"\bweekly\b", r"\brecurring\b", r"\bevery\b"],
    "spending": [r"\bbuy\b", r"\bpurchase\b", r"\border\b", r"\bsubscription\b"],
    "schedule": [r"\bcalendar\b", r"\bschedule\b", r"\bblock\b"],
    "external_tool": [r"\bconnect\b", r"\bintegration\b", r"\baccount\b", r"\blogin\b"],
    "protected_time": [
        r"\boverride protected time\b",
        r"\bconsume protected time\b",
        r"\buse protected time\b",
        r"\bduring protected time\b",
        r"\bmove protected time\b",
        r"\bchange protected time\b",
    ],
}


@dataclass(frozen=True)
class PreflightResult:
    outcome: str
    authority_level: str
    review_level: str
    risks: list[str]
    reasons: list[str]
    required_next_step: str

    def to_dict(self) -> dict:
        return {
            "outcome": self.outcome,
            "authority_level": self.authority_level,
            "review_level": self.review_level,
            "risks": self.risks,
            "reasons": self.reasons,
            "required_next_step": self.required_next_step,
        }


def read_input(path: Path | None, text: str | None) -> str:
    if text:
        return text
    if path:
        if not path.exists():
            raise SystemExit(f"missing directive: {path}")
        return path.read_text()
    raise SystemExit("provide --directive or --text")


def infer_authority(text: str) -> str:
    match = re.search(r"\bLevel\s+([0-4])\b", text, re.IGNORECASE)
    if not match:
        return "Level 1: Recommend"
    return {
        "0": "Level 0: Observe",
        "1": "Level 1: Recommend",
        "2": "Level 2: Direct",
        "3": "Level 3: Execute",
        "4": "Level 4: Escalate",
    }[match.group(1)]


def find_matches(text: str, patterns: dict[str, list[str]]) -> list[str]:
    found = []
    for risk, expressions in patterns.items():
        if any(re.search(expression, text, re.IGNORECASE) for expression in expressions):
            found.append(risk)
    return found


def preflight(text: str) -> PreflightResult:
    authority = infer_authority(text)
    high_impact = find_matches(text, HIGH_IMPACT_PATTERNS)
    review = find_matches(text, REVIEW_PATTERNS)
    reasons: list[str] = []

    if authority.startswith("Level 4") or high_impact:
        risks = sorted(set(high_impact))
        if authority.startswith("Level 4"):
            reasons.append("Directive declares Level 4 authority.")
        if risks:
            reasons.append("High-impact risk terms detected.")
        return PreflightResult(
            outcome="escalate",
            authority_level=authority,
            review_level="formal",
            risks=risks,
            reasons=reasons,
            required_next_step="Create or update a decision packet before execution.",
        )

    if authority.startswith("Level 2") or authority.startswith("Level 3") or review:
        risks = sorted(set(review))
        if authority.startswith("Level 2") or authority.startswith("Level 3"):
            reasons.append("Directive authority is above Level 1.")
        if risks:
            reasons.append("Standard-review trigger terms detected.")
        return PreflightResult(
            outcome="needs_review",
            authority_level=authority,
            review_level="standard",
            risks=risks,
            reasons=reasons,
            required_next_step="Run compliance review and confirm constraints before adoption.",
        )

    return PreflightResult(
        outcome="pass",
        authority_level=authority,
        review_level="light",
        risks=[],
        reasons=["No high-impact or standard-review triggers detected."],
        required_next_step="May proceed as a Level 1 recommendation if local constraints still fit.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directive", type=Path)
    parser.add_argument("--text")
    parser.add_argument("--json", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> PreflightResult:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = preflight(read_input(args.directive, args.text))

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"outcome: {result.outcome}")
        print(f"authority_level: {result.authority_level}")
        print(f"review_level: {result.review_level}")
        print("risks: " + (", ".join(result.risks) if result.risks else "none"))
        print("required_next_step: " + result.required_next_step)

    return result


if __name__ == "__main__":
    main_with_args()
