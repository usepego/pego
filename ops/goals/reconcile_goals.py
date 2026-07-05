#!/usr/bin/env python3
"""Build a protected PEGO goal reconciliation from existing private state."""

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


@dataclass(frozen=True)
class SourceGroup:
    domain: str
    label: str
    paths: tuple[str, ...]


SOURCE_GROUPS = [
    SourceGroup(
        "governance",
        "Constitution and governance constraints",
        (
            "constitution/constitution.md",
            "governance/constraints.md",
            "governance/reviews",
            "goals/progress/governance.json",
        ),
    ),
    SourceGroup(
        "happiness",
        "Happiness model and proxy-goal traps",
        (
            "happiness/model.md",
            "person/happiness-model.md",
            "goals/life-aim.md",
            "goals/progress/happiness.json",
        ),
    ),
    SourceGroup(
        "finance",
        "Finance baseline and freedom strategy",
        (
            "finance/financial-position.md",
            "finance/burn-model-notes.md",
            "finance/capital-buckets.md",
            "finance/scenarios.json",
            "goals/financial-freedom.md",
            "goals/progress/finance.json",
        ),
    ),
    SourceGroup(
        "career",
        "Career baseline and income dependency",
        (
            "career/baseline.md",
            "career/career-capital.md",
            "goals/strategy.md",
            "goals/progress/career.json",
        ),
    ),
    SourceGroup(
        "venture",
        "Venture and independent-income strategy",
        (
            "venture",
            "goals/strategy.md",
            "writing/positioning.md",
            "goals/progress/venture.json",
        ),
    ),
    SourceGroup(
        "health",
        "Health baseline and recovery constraints",
        (
            "health/baseline.json",
            "health/baseline.md",
            "health/check-ins",
            "goals/progress/health.json",
        ),
    ),
    SourceGroup(
        "home_environment",
        "Home environment and maintenance baseline",
        (
            "goals/home-serenity.md",
            "home/maintenance-system.md",
            "operator/operating-register.md",
            "goals/progress/home_environment.json",
            "goals/progress/home.json",
        ),
    ),
    SourceGroup(
        "relationships",
        "Protected relationships and stakeholder constraints",
        (
            "time/protected-time.md",
            "current-state/current-state.md",
            "operator/operating-register.md",
            "goals/progress/relationships.json",
        ),
    ),
    SourceGroup(
        "exploration",
        "Exploration and renewal baseline",
        (
            "goals/lifestyle-and-taste.md",
            "person/voice-and-taste.md",
            "operator/operating-register.md",
            "goals/progress/exploration.json",
        ),
    ),
    SourceGroup(
        "operations",
        "Recent outcomes and operating evidence",
        (
            "outcomes/directives",
            "reviews/outcomes",
            "reviews/sessions",
            "context/updates",
            "telemetry/signals",
            "goals/progress/operations.json",
        ),
    ),
]

DOMAIN_GOAL_TEXT = {
    "governance": "Preserve authority, privacy, reversibility, and stop conditions.",
    "happiness": "Optimize for lived fit rather than proxy goals.",
    "finance": "Protect financial downside while advancing financial freedom.",
    "career": "Protect income and career optionality.",
    "venture": "Create independent-income evidence without reckless risk.",
    "health": "Improve health through low-friction defaults and safe constraints.",
    "home_environment": "Preserve home serenity through small maintenance and environment design.",
    "relationships": "Protect important relationships, stakeholder impact, and protected time.",
    "exploration": "Keep curiosity, renewal, and life richness active within constraints.",
    "operations": "Convert goals into small directives and learn from outcomes.",
}

DOMAIN_CLASS = {
    "governance": "constitutional",
    "happiness": "constitutional",
    "finance": "strategic",
    "career": "strategic",
    "venture": "experimental",
    "health": "operational",
    "home_environment": "operational",
    "relationships": "constitutional",
    "exploration": "experimental",
    "operations": "operational",
}

PROTECTED_DOMAINS = {"governance", "happiness", "health", "relationships"}
UPSIDE_DOMAINS = {"finance", "career", "venture", "exploration", "home_environment"}
DOWNSIDE_DOMAINS = {
    "governance",
    "finance",
    "health",
    "home_environment",
    "relationships",
    "career",
}


def text_exists(path: Path) -> bool:
    if path.is_file():
        try:
            return bool(path.read_text().strip())
        except UnicodeDecodeError:
            return True
    if path.is_dir():
        return any(child.is_file() for child in path.rglob("*"))
    return False


def existing_sources(private: Path, group: SourceGroup) -> list[str]:
    found = []
    for relative in group.paths:
        if text_exists(private / relative):
            found.append(private_root_config.framework_relative_private_path(private, relative))
    return found


def assess_sources(private: Path) -> dict[str, list[str]]:
    return {
        group.domain: existing_sources(private, group)
        for group in SOURCE_GROUPS
    }


def read_goal_progress(private: Path, domain: str) -> dict[str, str]:
    paths = [private / "goals" / "progress" / f"{domain}.json"]
    if domain == "home_environment":
        paths.append(private / "goals" / "progress" / "home.json")
    path = next((candidate for candidate in paths if candidate.is_file()), None)
    if path is None:
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}
    if data.get("artifact_type") != "goal_progress":
        return {}
    return {
        "trajectory": str(data.get("trajectory", "unknown")),
        "confidence": str(data.get("confidence", "low")),
        "progress_status": str(data.get("progress_status", "unknown")),
        "current_state_summary": str(data.get("current_state_summary", "")),
    }


def progress_by_domain(private: Path) -> dict[str, dict[str, str]]:
    return {
        group.domain: read_goal_progress(private, group.domain)
        for group in SOURCE_GROUPS
    }


def priority_for(domain: str, sources: list[str]) -> str:
    if not sources:
        return "low"
    if domain in {"governance", "happiness", "relationships"}:
        return "high"
    if domain in {"finance", "health", "career"}:
        return "high"
    return "medium"


def active_goals(
    source_map: dict[str, list[str]],
    progress_map: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    goals = []
    for domain in [group.domain for group in SOURCE_GROUPS]:
        sources = source_map[domain]
        progress = progress_map.get(domain, {})
        status = "active" if sources else "needs_baseline"
        goal = {
            "goal": DOMAIN_GOAL_TEXT[domain],
            "domain": domain,
            "class": DOMAIN_CLASS[domain],
            "current_priority": priority_for(domain, sources),
            "why_it_matters": (
                progress.get("current_state_summary")
                or (
                    "Existing protected private state is available for this domain."
                    if sources
                    else "Council lacks enough private baseline evidence for this domain."
                )
            ),
            "status": status,
        }
        if progress:
            goal["trajectory"] = progress.get("trajectory", "unknown")
            goal["confidence"] = progress.get("confidence", "low")
            goal["progress_status"] = progress.get("progress_status", "unknown")
        goals.append(goal)
    return goals


def missing_domains(source_map: dict[str, list[str]]) -> list[str]:
    return [domain for domain, sources in source_map.items() if not sources]


def targeted_questions(missing: list[str]) -> list[dict[str, str]]:
    if not missing:
        return [
            {
                "question": "Which active goal conflict has felt most costly recently?",
                "decision_use": "Sharpens conflict rules before the next council decision.",
            }
        ]
    domain = missing[0]
    return [
        {
            "question": f"What is the minimum {domain} context PEGO needs before trading it off against another goal?",
            "decision_use": f"Creates the first decision-grade {domain} baseline for council priority rules.",
        }
    ]


def build_artifact(private: Path, reconciliation_date: str) -> dict[str, object]:
    source_map = assess_sources(private)
    progress_map = progress_by_domain(private)
    missing = missing_domains(source_map)
    goals = active_goals(source_map, progress_map)
    source_inputs = sorted(source for sources in source_map.values() for source in sources)

    return {
        "artifact_type": "goal_reconciliation",
        "schema_version": 1,
        "date": reconciliation_date,
        "source_inputs": source_inputs,
        "active_goals": goals,
        "protected_goals": [
            DOMAIN_GOAL_TEXT[goal["domain"]]
            for goal in goals
            if goal["domain"] in PROTECTED_DOMAINS
        ],
        "upside_goals": [
            DOMAIN_GOAL_TEXT[goal["domain"]]
            for goal in goals
            if goal["domain"] in UPSIDE_DOMAINS
        ],
        "downside_protection_goals": [
            DOMAIN_GOAL_TEXT[goal["domain"]]
            for goal in goals
            if goal["domain"] in DOWNSIDE_DOMAINS
        ],
        "current_priority_thesis": priority_thesis(missing),
        "conflict_rules": conflict_rules(),
        "directive_selection_rules": directive_selection_rules(missing),
        "information_gaps": [f"Missing or thin {domain} baseline." for domain in missing],
        "targeted_questions": targeted_questions(missing),
        "temporary_assumptions": temporary_assumptions(missing),
        "governance_notes": [
            "This reconciliation is generated from protected private state presence and should be reviewed by an agent before high-impact decisions.",
            "Financial, medical, legal, tax, career-risking, relationship-impacting, privacy-impacting, housing, or hard-to-reverse actions still require governance review.",
        ],
        "review_cadence": "Review during onboarding, monthly, after repeated directive friction, or whenever the human says PEGO is optimizing the wrong thing.",
        "stop_conditions": [
            "Stop using this reconciliation for high-impact decisions if a protected domain is missing baseline evidence.",
            "Stop and ask a targeted priority question if two high-priority goals conflict and no conflict rule applies.",
            "Stop and escalate if a directive would trade away protected relationships, privacy, health, income security, housing stability, or explicit authority boundaries.",
        ],
    }


def priority_thesis(missing: list[str]) -> str:
    if missing:
        return (
            "Use a conservative council model: protect constitutional goals and downside risks first, "
            "advance upside through low-risk reversible directives, and ask the highest-value missing "
            "baseline question before making high-impact tradeoffs."
        )
    return (
        "Use a balanced council model: protect constitutional goals first, keep finance, health, "
        "career, relationships, and home/environment constraints visible, and select the smallest directive that "
        "creates progress or evidence without increasing anxiety."
    )


def conflict_rules() -> list[dict[str, str]]:
    return [
        {
            "conflict": "Protected relationships, health, privacy, or authority boundary vs. optional productivity or venture work.",
            "default_priority": "Protected goal wins.",
            "why": "PEGO must not create progress by damaging the life conditions it is meant to protect.",
            "exception": "A reversible, explicitly approved action may proceed if it does not disturb the protected condition.",
            "review_or_escalation": "Governance review required for relationship-impacting, health-risking, privacy-impacting, or authority-expanding actions.",
        },
        {
            "conflict": "Income protection vs. independent-income exploration.",
            "default_priority": "Income protection wins by default; exploration gets bounded evidence blocks.",
            "why": "Career and finance downside can dominate optionality if handled recklessly.",
            "exception": "A low-risk evidence directive may proceed when it fits available time and does not harm current work obligations.",
            "review_or_escalation": "Escalate before job-risking, public, financial, or irreversible venture actions.",
        },
        {
            "conflict": "Home, health, or operating maintenance vs. strategic work.",
            "default_priority": "Small maintenance wins when deferral would create visible deterioration, health drift, or future scrambling.",
            "why": "Small preventive directives can reduce anxiety and protect future execution capacity.",
            "exception": "Strategic work may win when maintenance can be safely deferred and the strategic window is time-sensitive.",
            "review_or_escalation": "Ask a targeted question if the maintenance issue may disturb another person, require spending, or affect safety.",
        },
    ]


def directive_selection_rules(missing: list[str]) -> list[str]:
    rules = [
        "Select one directive, one targeted question, one deferral, or one escalation.",
        "Prefer low-risk reversible directives when evidence is incomplete.",
        "Protect relationships, health, sleep, privacy, income security, and explicit authority boundaries before optional upside.",
        "Ask only the missing question that would change the next directive or council priority.",
        "Preserve dissent when an agent recommendation serves an active goal that is deferred.",
    ]
    if missing:
        rules.append("Do not claim best cross-domain selection for missing domains; use a temporary assumption or ask a baseline question.")
    return rules


def temporary_assumptions(missing: list[str]) -> list[str]:
    assumptions = [
        "Missing evidence means PEGO should choose reversible actions or information gathering, not high-impact tradeoffs.",
        "Proxy goals such as money, productivity, fitness, or status may not silently override happiness, relationships, health, privacy, or authority.",
    ]
    if missing:
        assumptions.append("Domains without baseline evidence are protected from being traded away by default.")
    return assumptions


def build_markdown(artifact: dict[str, object]) -> str:
    def bullets(values: object) -> list[str]:
        items = values if isinstance(values, list) else []
        return [f"- {item}" for item in items] or ["- None."]

    def goal_rows(goals: object) -> list[str]:
        rows = []
        for goal in goals if isinstance(goals, list) else []:
            if not isinstance(goal, dict):
                continue
            rows.append(
                "| {goal} | {domain} | {klass} | {priority} | {trajectory} | {confidence} | {progress_status} | {why} | {status} |".format(
                    goal=goal.get("goal", ""),
                    domain=goal.get("domain", ""),
                    klass=goal.get("class", ""),
                    priority=goal.get("current_priority", ""),
                    trajectory=goal.get("trajectory", "unknown"),
                    confidence=goal.get("confidence", "low"),
                    progress_status=goal.get("progress_status", "unknown"),
                    why=goal.get("why_it_matters", ""),
                    status=goal.get("status", ""),
                )
            )
        return rows or ["| None | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"]

    def conflict_rows(rules: object) -> list[str]:
        rows = []
        for rule in rules if isinstance(rules, list) else []:
            if not isinstance(rule, dict):
                continue
            rows.append(
                "| {conflict} | {priority} | {why} | {exception} | {review} |".format(
                    conflict=rule.get("conflict", ""),
                    priority=rule.get("default_priority", ""),
                    why=rule.get("why", ""),
                    exception=rule.get("exception", ""),
                    review=rule.get("review_or_escalation", ""),
                )
            )
        return rows or ["| None | n/a | n/a | n/a | n/a |"]

    def question_rows(questions: object) -> list[str]:
        rows = []
        for question in questions if isinstance(questions, list) else []:
            if not isinstance(question, dict):
                continue
            rows.append(f"| {question.get('question', '')} | {question.get('decision_use', '')} |")
        return rows or ["| None | n/a |"]

    return "\n".join(
        [
            f"# Goal Reconciliation: {artifact['date']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Source Inputs",
            "",
            *bullets(artifact["source_inputs"]),
            "",
            "## Active Goals",
            "",
            "| Goal | Domain | Class | Current Priority | Trajectory | Confidence | Progress Status | Why It Matters | Status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *goal_rows(artifact["active_goals"]),
            "",
            "## Protected Goals",
            "",
            *bullets(artifact["protected_goals"]),
            "",
            "## Upside Goals",
            "",
            *bullets(artifact["upside_goals"]),
            "",
            "## Downside Protection Goals",
            "",
            *bullets(artifact["downside_protection_goals"]),
            "",
            "## Current Priority Thesis",
            "",
            str(artifact["current_priority_thesis"]),
            "",
            "## Conflict Rules",
            "",
            "| Conflict | Default Priority | Why | Exception | Review / Escalation |",
            "| --- | --- | --- | --- | --- |",
            *conflict_rows(artifact["conflict_rules"]),
            "",
            "## Directive Selection Rules",
            "",
            *bullets(artifact["directive_selection_rules"]),
            "",
            "## Information Gaps",
            "",
            *bullets(artifact["information_gaps"]),
            "",
            "## Targeted Questions",
            "",
            "| Question | Decision Use |",
            "| --- | --- |",
            *question_rows(artifact["targeted_questions"]),
            "",
            "## Temporary Assumptions",
            "",
            *bullets(artifact["temporary_assumptions"]),
            "",
            "## Governance Notes",
            "",
            *bullets(artifact["governance_notes"]),
            "",
            "## Review Cadence",
            "",
            str(artifact["review_cadence"]),
            "",
            "## Stop Conditions",
            "",
            *bullets(artifact["stop_conditions"]),
            "",
        ]
    )


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.output = args.output or private / "goals" / "goal-reconciliation.md"
    args.json_output = args.json_output or private / "goals" / "goal-reconciliation.json"
    artifact = build_artifact(private, args.date)
    write_output(args.output, build_markdown(artifact), args.force)
    write_output(args.json_output, json.dumps(artifact, indent=2, sort_keys=True) + "\n", args.force)
    print(f"wrote: {display_output(private, args.output)}")
    print(f"wrote: {display_output(private, args.json_output)}")
    return args.output


if __name__ == "__main__":
    main_with_args()
