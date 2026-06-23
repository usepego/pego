#!/usr/bin/env python3
"""Generate a protected PEGO public-writing brief and directive candidate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "public-writing"


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


def read_voice_constraints(path: Path) -> dict[str, str]:
    if not path.exists():
        return {
            "status": "missing",
            "summary": "No private voice model found. Treat style assumptions as provisional.",
        }
    sections = parse_sections(path.read_text())
    useful = []
    for name in ["Writing Voice", "Humor", "Intellectual Posture", "Vocabulary", "Public Positioning", "Drafting Preferences"]:
        value = sections.get(name, "").strip()
        if value:
            useful.append(f"{name}: {value}")
    summary = "\n\n".join(useful).strip() or "Voice model exists but has no extracted constraints."
    return {"status": "available", "summary": summary}


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def build_brief(args: argparse.Namespace, voice: dict[str, str]) -> str:
    sources = split_values(args.private_source_material) or ["private/person/voice-and-taste.md"]
    public_safe = split_values(args.public_safe_material) or [
        "PEGO can be described as a runtime-neutral governance framework.",
        "The essay may discuss the category and architecture without exposing protected private facts.",
    ]
    supporting_claims = split_values(args.supporting_claims) or [
        "Existing personal operating systems often assist or track; PEGO governs within delegated authority.",
        "A council, authority levels, dissent, privacy rules, directives, outcomes, and reviews make the system more serious than a chatbot.",
        "The smallest useful output is a concrete next directive, not another dashboard.",
    ]
    outline = split_values(args.structure) or [
        "Open with the problem: decision burden and life tradeoffs are not solved by more dashboards.",
        "Define PEGO as Personal Executive Governance OS.",
        "Explain agents, council, authority, directives, and review.",
        "Contrast with assistants, habit trackers, and quantified-self systems.",
        "Close with what is being built and why serious people may care.",
    ]
    voice_constraints = voice["summary"]
    return "\n".join(
        [
            f"# Public Writing Brief: {args.artifact}",
            "",
            "## Date",
            "",
            args.date,
            "",
            "## Artifact",
            "",
            args.artifact,
            "",
            "## Public Purpose",
            "",
            args.public_purpose,
            "",
            "## Opportunity Thesis",
            "",
            args.opportunity_thesis,
            "",
            "## Audience",
            "",
            args.audience,
            "",
            "## Reader Reaction",
            "",
            args.reader_reaction,
            "",
            "## Core Claim",
            "",
            args.core_claim,
            "",
            "## Supporting Claims",
            "",
            *[f"- {claim}" for claim in supporting_claims],
            "",
            "## Private Source Material",
            "",
            *[f"- {source}" for source in sources],
            "",
            "## Public-Safe Material",
            "",
            *[f"- {item}" for item in public_safe],
            "",
            "## Voice Constraints",
            "",
            voice_constraints,
            "",
            "## Structure",
            "",
            *[f"- {item}" for item in outline],
            "",
            "## Dissent",
            "",
            args.dissent,
            "",
            "## Governance Review",
            "",
            "- Privacy review before publishing.",
            "- Employer/client confidentiality review before publishing.",
            "- Third-party privacy review before publishing.",
            "- Claims requiring evidence must be supported or softened.",
            "- Publishing is Level 4 until explicitly cleared.",
            "",
            "## Draft Directive",
            "",
            args.next_action,
            "",
            "## Review Rule",
            "",
            args.review_rule,
            "",
        ]
    )


def build_candidate(args: argparse.Namespace, brief_output: Path, voice: dict[str, str]) -> dict[str, object]:
    dependencies = [str(brief_output)]
    if voice["status"] == "missing":
        dependencies.append("Create or update private/person/voice-and-taste.md")
    return {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": f"Draft: {args.artifact}",
        "domain": "communications",
        "altitude": "directive",
        "proposed_action": args.next_action,
        "duration": args.duration,
        "timing": args.timing,
        "energy_required": args.energy,
        "location_required": "computer",
        "dependencies": dependencies,
        "expected_benefit": args.opportunity_thesis,
        "consequence_of_deferral": "The public opportunity surface remains undeveloped and PEGO loses a chance to clarify positioning.",
        "protected_time_impact": "none",
        "authority_level": "level_1_recommend",
        "governance_status": "reviewed",
        "conflicts": ["Publishing requires Level 4 governance review."],
        "stop_condition": "Stop before publishing, sharing employer/private details, or making claims that require evidence.",
    }


def candidate_markdown(candidate: dict[str, object]) -> str:
    dependencies = [str(item) for item in candidate["dependencies"]]
    conflicts = [str(item) for item in candidate["conflicts"]]
    return "\n".join(
        [
            f"# Communications Candidate: {candidate['candidate']}",
            "",
            "## Candidate",
            "",
            str(candidate["candidate"]),
            "",
            "## Domain",
            "",
            "Communications",
            "",
            "## Altitude",
            "",
            "Directive",
            "",
            "## Proposed Action",
            "",
            str(candidate["proposed_action"]),
            "",
            "## Duration",
            "",
            str(candidate["duration"]),
            "",
            "## Timing",
            "",
            str(candidate["timing"]),
            "",
            "## Energy Required",
            "",
            str(candidate["energy_required"]).title(),
            "",
            "## Location Required",
            "",
            "Computer",
            "",
            "## Dependencies",
            "",
            *[f"- {item}" for item in dependencies],
            "",
            "## Expected Benefit",
            "",
            str(candidate["expected_benefit"]),
            "",
            "## Consequence of Deferral",
            "",
            str(candidate["consequence_of_deferral"]),
            "",
            "## Protected-Time Impact",
            "",
            "None",
            "",
            "## Authority Level",
            "",
            "Level 1",
            "",
            "## Governance Status",
            "",
            "Reviewed",
            "",
            "## Conflicts",
            "",
            *[f"- {item}" for item in conflicts],
            "",
            "## Stop Condition",
            "",
            str(candidate["stop_condition"]),
            "",
        ]
    )


def default_path(root: Path, folder: str, output_date: str, artifact: str, suffix: str) -> Path:
    return root / folder / f"{output_date}-{slugify(artifact)}{suffix}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--artifact", default="PEGO introduction essay")
    parser.add_argument("--public-purpose", default="Introduce PEGO as a serious new category of personal executive governance software.")
    parser.add_argument("--opportunity-thesis", default="Attract serious technical, career, collaborator, customer, or business conversations around PEGO.")
    parser.add_argument("--audience", default="Technically literate readers, operators, founders, AI builders, and people interested in governed personal agency.")
    parser.add_argument("--reader-reaction", default="This is not another life assistant; this is a serious governance architecture for human action.")
    parser.add_argument("--core-claim", default="PEGO is a Personal Executive Governance OS: a governed agent system that turns goals, constraints, and feedback into directives.")
    parser.add_argument("--supporting-claims", default="")
    parser.add_argument("--private-source-material", default="")
    parser.add_argument("--public-safe-material", default="")
    parser.add_argument("--structure", default="")
    parser.add_argument("--dissent", default="The piece could sound like self-help, academic theory, or AI hype if it does not stay concrete, serious, and implementation-aware.")
    parser.add_argument("--next-action", default="Draft the first 600-900 words privately, using the brief and voice model, without publishing.")
    parser.add_argument("--review-rule", default="Review after the first private draft and before any public release.")
    parser.add_argument("--duration", default="45 min")
    parser.add_argument("--timing", default="Next focused writing block")
    parser.add_argument("--energy", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--voice-model", type=Path)
    parser.add_argument("--brief-output", type=Path)
    parser.add_argument("--candidate-output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)
    print(f"wrote: {path}")


def main_with_args(argv: list[str] | None = None) -> tuple[Path, Path]:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.voice_model = args.voice_model or private / "person" / "voice-and-taste.md"
    brief_output = args.brief_output or default_path(private, "writing/briefs", args.date, args.artifact, ".md")
    candidate_output = args.candidate_output or private / "directives" / "candidates" / "communications-candidates.md"
    voice = read_voice_constraints(args.voice_model)
    candidate = build_candidate(args, brief_output, voice)

    write_output(brief_output, build_brief(args, voice), args.force)
    write_output(candidate_output, candidate_markdown(candidate), args.force)
    if args.json_output:
        write_output(args.json_output, json.dumps(candidate, indent=2, sort_keys=True) + "\n", args.force)
    return brief_output, candidate_output


if __name__ == "__main__":
    main_with_args()
