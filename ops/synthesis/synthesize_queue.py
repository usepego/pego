#!/usr/bin/env python3
"""Synthesize protected PEGO directive candidates into one active queue."""

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


@dataclass(frozen=True)
class Candidate:
    name: str
    domain: str
    duration: str
    energy: str
    location: str
    deadline: str
    authority: str
    status: str
    benefit: str
    deferral: str
    target_behavior: str
    environment_design: str
    protected_time: str
    source: str


@dataclass(frozen=True)
class ScoreDimension:
    dimension: str
    weight: int
    score: int
    weighted_score: int
    rationale: str


@dataclass(frozen=True)
class Scorecard:
    score_total: int
    score_dimensions: tuple[ScoreDimension, ...]
    selection_rationale: str
    tie_breaker: str


@dataclass(frozen=True)
class ScoredCandidate:
    candidate: Candidate
    scorecard: Scorecard


@dataclass(frozen=True)
class QueueBuild:
    active: list[ScoredCandidate]
    deferred: list[tuple[ScoredCandidate, str]]
    args: argparse.Namespace


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def is_table_data(line: str) -> bool:
    return line.startswith("|") and "---" not in line


def map_row(headers: list[str], cells: list[str]) -> dict[str, str]:
    mapped: dict[str, str] = {}
    for index, header in enumerate(headers):
        mapped[normalize_header(header)] = cells[index] if index < len(cells) else ""
    return mapped


def candidate_from_mapping(mapped: dict[str, str], source: str) -> Candidate | None:
    name = (
        mapped.get("candidate")
        or mapped.get("name")
        or mapped.get("proposed-action")
        or mapped.get("directive")
        or ""
    )
    if not name or name == "TBD":
        return None
    return Candidate(
        name=name,
        domain=mapped.get("domain", "Operations") or "Operations",
        duration=mapped.get("duration", mapped.get("time", "Unknown")) or "Unknown",
        energy=mapped.get("energy", mapped.get("energy-required", "Medium")) or "Medium",
        location=mapped.get("location", mapped.get("location-required", "Home")) or "Home",
        deadline=mapped.get("deadline", mapped.get("timing", "Today")) or "Today",
        authority=mapped.get("authority", mapped.get("authority-level", "Level 1")) or "Level 1",
        status=mapped.get("status", mapped.get("governance-status", "Draft")) or "Draft",
        benefit=mapped.get("expected-benefit", mapped.get("benefit", "")),
        deferral=mapped.get("consequence-of-deferral", mapped.get("deferral", "")),
        target_behavior=mapped.get("target-behavior", ""),
        environment_design=mapped.get("environment-design", ""),
        protected_time=mapped.get("protected-time-impact", "None") or "None",
        source=source,
    )


def display_domain(value: object) -> str:
    raw = str(value or "Operations").strip()
    return {
        "finance": "Finance",
        "health": "Health",
        "career": "Career",
        "venture": "Venture",
        "home_environment": "Home and Environment",
        "relationships": "Relationships",
        "exploration": "Exploration",
        "communications": "Communications",
        "happiness": "Happiness",
        "operations": "Operations",
        "governance": "Governance",
    }.get(raw, raw or "Operations")


def display_energy(value: object) -> str:
    raw = str(value or "Medium").strip().lower()
    return {
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }.get(raw, str(value or "Medium"))


def display_location(value: object) -> str:
    raw = str(value or "Home").strip().lower()
    return {
        "home": "Home",
        "office": "Office",
        "outside": "Outside",
        "errand": "Errand",
        "phone": "Phone",
        "computer": "Computer",
        "other": "Other",
    }.get(raw, str(value or "Home"))


def display_authority(value: object) -> str:
    raw = str(value or "level_1_recommend").strip().lower()
    return {
        "level_0_observe": "Level 0",
        "level_1_recommend": "Level 1",
        "level_2_direct": "Level 2",
        "level_3_execute": "Level 3",
        "level_4_escalate": "Level 4",
    }.get(raw, str(value or "Level 1"))


def display_status(value: object) -> str:
    raw = str(value or "draft").strip().lower()
    return {
        "draft": "Draft",
        "reviewed": "Reviewed",
        "approved_with_constraints": "Approved with constraints",
        "escalated": "Escalated",
        "blocked": "Blocked",
    }.get(raw, str(value or "Draft"))


def display_impact(value: object) -> str:
    raw = str(value or "none").strip().lower()
    return {
        "none": "None",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
    }.get(raw, str(value or "None"))


def parse_json_candidates(text: str, source: str) -> list[Candidate]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    items = data if isinstance(data, list) else [data]
    candidates: list[Candidate] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("artifact_type") != "directive_candidate":
            continue
        name = str(item.get("candidate") or item.get("proposed_action") or "").strip()
        if not name:
            continue
        dependencies = item.get("dependencies", [])
        dependency_text = ", ".join(str(value) for value in dependencies if str(value).strip())
        candidates.append(
            Candidate(
                name=name,
                domain=display_domain(item.get("domain")),
                duration=str(item.get("duration") or "Unknown"),
                energy=display_energy(item.get("energy_required")),
                location=display_location(item.get("location_required")),
                deadline=str(item.get("timing") or "Today"),
                authority=display_authority(item.get("authority_level")),
                status=display_status(item.get("governance_status")),
                benefit=str(item.get("expected_benefit") or ""),
                deferral=str(item.get("consequence_of_deferral") or ""),
                target_behavior=str(item.get("target_behavior") or ""),
                environment_design=str(item.get("environment_design") or ""),
                protected_time=display_impact(item.get("protected_time_impact")),
                source=source + (f" dependencies: {dependency_text}" if dependency_text else ""),
            )
        )
    return candidates


def parse_candidates_table(text: str, source: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    headers: list[str] | None = None
    for line in text.splitlines():
        if not is_table_data(line):
            continue
        cells = parse_table_cells(line)
        if not cells:
            continue
        normalized = [normalize_header(cell) for cell in cells]
        if any(key in normalized for key in {"candidate", "proposed-action", "directive"}):
            headers = cells
            continue
        if headers is None:
            continue
        candidate = candidate_from_mapping(map_row(headers, cells), source)
        if candidate:
            candidates.append(candidate)
    return candidates


def parse_heading_sections(text: str) -> dict[str, str]:
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


def parse_single_candidate(text: str, source: str) -> Candidate | None:
    sections = parse_heading_sections(text)
    name = (
        sections.get("Candidate")
        or sections.get("Candidate Directive")
        or sections.get("Proposed Action")
        or ""
    ).splitlines()[0:1]
    if not name:
        return None
    status = sections.get("Governance Status", "Draft").splitlines()[0]
    return Candidate(
        name=name[0],
        domain=(sections.get("Domain", "Operations").splitlines() or ["Operations"])[0],
        duration=(sections.get("Duration", "Unknown").splitlines() or ["Unknown"])[0],
        energy=(sections.get("Energy Required", "Medium").splitlines() or ["Medium"])[0],
        location=(sections.get("Location Required", "Home").splitlines() or ["Home"])[0],
        deadline=(sections.get("Timing", sections.get("Lead Time", "Today")).splitlines() or ["Today"])[0],
        authority=(sections.get("Authority Level", "Level 1").splitlines() or ["Level 1"])[0],
        status=status,
        benefit=sections.get("Expected Benefit", ""),
        deferral=sections.get("Consequence of Deferral", ""),
        target_behavior=sections.get("Target Behavior", ""),
        environment_design=sections.get("Environment Design", ""),
        protected_time=(sections.get("Protected-Time Impact", "None").splitlines() or ["None"])[0],
        source=source,
    )


def read_candidates(paths: list[Path]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for path in paths:
        text = path.read_text()
        parsed = parse_json_candidates(text, str(path))
        if not parsed:
            parsed = parse_candidates_table(text, str(path))
        if not parsed:
            single = parse_single_candidate(text, str(path))
            parsed = [single] if single else []
        candidates.extend(parsed)
    return candidates


def minutes_from_duration(duration: str) -> int:
    numbers = [int(match) for match in re.findall(r"\d+", duration)]
    if not numbers:
        return 30
    return min(numbers)


SCORING_MODEL = "directive-scoring-v1"
SCORE_WEIGHTS = {
    "goal_contribution": 3,
    "urgency": 3,
    "consequence_of_deferral": 3,
    "energy_fit": 1,
    "reversibility": 2,
    "downside_protection": 2,
    "anxiety_reduction": 2,
    "evidence_value": 2,
    "environment_leverage": 1,
}
SCORE_DESCRIPTIONS = {
    "goal_contribution": "Contribution to a stated domain goal, non-negotiable, or operating priority.",
    "urgency": "Timing pressure from deadline, lead time, or current operating window.",
    "consequence_of_deferral": "Expected downside if the candidate waits until a later synthesis.",
    "energy_fit": "Fit between required energy and supplied or assumed current energy.",
    "reversibility": "Preference for low-commitment, reversible actions.",
    "downside_protection": "Protection against avoidable deterioration, friction, or future interruption.",
    "anxiety_reduction": "Reduction of ambiguity, cognitive load, open loops, or future scrambling.",
    "evidence_value": "Value of producing decision-grade information when evidence is weak.",
    "environment_leverage": "Ability to reshape future behavior through context or setup.",
}


def scoring_model_dict() -> dict:
    return {
        "model": SCORING_MODEL,
        "score_range": "0-3 per dimension before weighting",
        "dimensions": [
            {
                "dimension": dimension,
                "weight": weight,
                "description": SCORE_DESCRIPTIONS[dimension],
            }
            for dimension, weight in SCORE_WEIGHTS.items()
        ],
        "selection_rule": (
            "Score all candidates, defer governance-gated or over-window candidates, "
            "rank active candidates by score_total descending, and resolve ties with "
            "the safe tie-break order."
        ),
        "safe_tie_break_order": [
            "lower authority",
            "lower protected-time impact",
            "lower required energy",
            "shorter duration",
            "information-gathering or environment-shaping work when evidence is weak",
            "candidate name",
        ],
    }


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def candidate_text(candidate: Candidate) -> str:
    return " ".join(
        [
            candidate.name,
            candidate.domain,
            candidate.deadline,
            candidate.authority,
            candidate.status,
            candidate.benefit,
            candidate.deferral,
            candidate.target_behavior,
            candidate.environment_design,
            candidate.protected_time,
        ]
    ).lower()


def authority_rank(value: str) -> int:
    normalized = value.strip().lower().replace("-", " ")
    for level in range(5):
        if f"level {level}" in normalized:
            return level
    return 1


def protected_time_rank(value: str) -> int:
    normalized = value.strip().lower()
    if "high" in normalized:
        return 3
    if "medium" in normalized:
        return 2
    if "low" in normalized:
        return 1
    return 0


def energy_rank(value: str) -> int:
    normalized = normalize_energy(value)
    return {"low": 0, "medium": 1, "high": 2, "unknown": 1}.get(normalized, 1)


def is_weak_evidence(candidate: Candidate) -> bool:
    evidence_fields = [
        candidate.benefit,
        candidate.deferral,
        candidate.target_behavior,
        candidate.environment_design,
    ]
    return sum(1 for field in evidence_fields if field.strip()) < 2


def is_information_or_environment_work(candidate: Candidate) -> bool:
    text = candidate_text(candidate)
    return contains_any(
        text,
        [
            "ask",
            "question",
            "review",
            "map",
            "list",
            "quote",
            "scan",
            "draft",
            "prepare",
            "clarify",
            "scope",
            "environment",
            "setup",
            "default",
            "route",
            "context",
        ],
    )


def clamp_score(score: int) -> int:
    return max(0, min(3, score))


def make_dimension(dimension: str, score: int, rationale: str) -> ScoreDimension:
    normalized = clamp_score(score)
    weight = SCORE_WEIGHTS[dimension]
    return ScoreDimension(
        dimension=dimension,
        weight=weight,
        score=normalized,
        weighted_score=normalized * weight,
        rationale=rationale,
    )


def score_goal_contribution(candidate: Candidate) -> ScoreDimension:
    text = candidate_text(candidate)
    if contains_any(text, ["health", "safety", "privacy", "income", "relationship"]):
        return make_dimension("goal_contribution", 3, "Protects a high-priority operating domain.")
    if contains_any(
        text,
        [
            "strategic",
            "strategy",
            "stabilize",
            "preserve",
            "clarify",
            "maintenance",
            "venture",
            "career",
            "finance",
            "home",
            "goal",
        ],
    ):
        return make_dimension("goal_contribution", 2, "Advances a named domain or strategy.")
    if candidate.benefit.strip() or candidate.target_behavior.strip():
        return make_dimension("goal_contribution", 2, "Has an explicit benefit or behavior target.")
    return make_dimension("goal_contribution", 1, "Goal contribution is present but weakly evidenced.")


def score_urgency(candidate: Candidate) -> ScoreDimension:
    text = f"{candidate.deadline} {candidate.deferral}".lower()
    if contains_any(
        text,
        ["now", "today", "morning", "before", "evening", "urgent", "scrambling", "friction"],
    ):
        return make_dimension("urgency", 3, "Timing or deferral language indicates same-window pressure.")
    if contains_any(text, ["this week", "week", "this month", "month", "days", "lead time"]):
        return make_dimension("urgency", 2, "Timing has near-term pressure but not immediate pressure.")
    if candidate.deadline.strip() and candidate.deadline.strip().lower() not in {"unknown", "tbd"}:
        return make_dimension("urgency", 1, "Timing exists but is not strongly urgent.")
    return make_dimension("urgency", 0, "No usable urgency signal.")


def score_consequence_of_deferral(candidate: Candidate) -> ScoreDimension:
    consequence = candidate.deferral.lower()
    if contains_any(
        consequence,
        [
            "visible",
            "friction",
            "deteriorat",
            "scrambling",
            "delay",
            "cost",
            "risk",
            "unsafe",
            "miss",
        ],
    ):
        return make_dimension("consequence_of_deferral", 3, "Deferral predicts concrete deterioration or cost.")
    if consequence.strip():
        return make_dimension("consequence_of_deferral", 2, "Deferral has a stated downside.")
    return make_dimension("consequence_of_deferral", 0, "No consequence of deferral supplied.")


def score_energy_fit(candidate: Candidate, args: argparse.Namespace) -> ScoreDimension:
    required = normalize_energy(candidate.energy)
    current = normalize_energy(getattr(args, "energy", "") or "")
    if current == "unknown":
        score = {"low": 3, "medium": 2, "high": 1, "unknown": 1}.get(required, 1)
        return make_dimension("energy_fit", score, f"Required energy is {required}; current energy is unknown.")
    if required == "unknown":
        return make_dimension("energy_fit", 1, "Required energy is unknown.")
    if energy_rank(candidate.energy) <= energy_rank(current):
        return make_dimension("energy_fit", 3, f"Required energy {required} fits current energy {current}.")
    if energy_rank(candidate.energy) == energy_rank(current) + 1:
        return make_dimension("energy_fit", 1, f"Required energy {required} may exceed current energy {current}.")
    return make_dimension("energy_fit", 0, f"Required energy {required} exceeds current energy {current}.")


def score_reversibility(candidate: Candidate) -> ScoreDimension:
    text = candidate_text(candidate)
    if risk_flags(candidate):
        return make_dimension("reversibility", 0, "Governance or authority flags make the action non-routine.")
    if contains_any(
        text,
        ["quit", "purchase", "buy", "hire", "fire", "sign", "submit", "send", "publish", "relocation"],
    ):
        return make_dimension("reversibility", 1, "Action language may create commitment or external impact.")
    if contains_any(text, ["quote", "review", "map", "list", "ask", "scan", "draft", "prepare", "walk"]):
        return make_dimension("reversibility", 3, "Action is information-gathering, preparatory, or easy to stop.")
    return make_dimension("reversibility", 2, "Action appears bounded and reversible.")


def score_downside_protection(candidate: Candidate) -> ScoreDimension:
    text = candidate_text(candidate)
    if risk_flags(candidate):
        return make_dimension("downside_protection", 1, "Potential downside is governed by deferral rather than rank.")
    if contains_any(
        text,
        [
            "preserve",
            "protect",
            "stabilize",
            "clarify",
            "reduce",
            "friction",
            "guardrail",
            "maintenance",
            "repair",
            "hunger",
            "baseline",
            "serenity",
            "prevent",
        ],
    ):
        return make_dimension("downside_protection", 3, "Candidate prevents avoidable friction or deterioration.")
    if candidate.benefit.strip() or candidate.deferral.strip():
        return make_dimension("downside_protection", 2, "Candidate has a stated protective benefit or downside.")
    return make_dimension("downside_protection", 1, "Downside protection is weakly evidenced.")


def score_anxiety_reduction(candidate: Candidate) -> ScoreDimension:
    text = candidate_text(candidate)
    if risk_flags(candidate):
        return make_dimension(
            "anxiety_reduction",
            1,
            "Potential anxiety reduction is gated by unresolved governance or authority risk.",
        )
    if contains_any(
        text,
        [
            "anxiety",
            "stress",
            "worry",
            "overwhelm",
            "scrambling",
            "clarify",
            "scope",
            "quote",
            "decision",
            "uncertain",
            "ambiguous",
            "friction",
            "visible",
            "open loop",
        ],
    ):
        return make_dimension(
            "anxiety_reduction",
            3,
            "Candidate reduces ambiguity, future scrambling, or a visible open loop.",
        )
    if is_information_or_environment_work(candidate):
        return make_dimension(
            "anxiety_reduction",
            2,
            "Information or environment work can lower cognitive load before the next decision.",
        )
    if candidate.deferral.strip():
        return make_dimension(
            "anxiety_reduction",
            2,
            "Deferral has a stated downside that this candidate may reduce.",
        )
    return make_dimension("anxiety_reduction", 1, "Anxiety reduction is weakly evidenced.")


def score_evidence_value(candidate: Candidate) -> ScoreDimension:
    if is_information_or_environment_work(candidate):
        return make_dimension("evidence_value", 3, "Candidate can create decision-grade information or setup.")
    if candidate.target_behavior.strip() and candidate.environment_design.strip():
        return make_dimension("evidence_value", 2, "Behavior and environment assumptions are explicit.")
    if candidate.benefit.strip() or candidate.deferral.strip():
        return make_dimension("evidence_value", 2, "Candidate has enough stated evidence for comparison.")
    return make_dimension("evidence_value", 1, "Evidence is weak; safe tie-breaks should prefer smaller reversible work.")


def score_environment_leverage(candidate: Candidate) -> ScoreDimension:
    text = candidate_text(candidate)
    if candidate.environment_design.strip():
        return make_dimension("environment_leverage", 3, "Environment design is explicit.")
    if contains_any(text, ["outside", "home", "errand", "phone", "computer", "default", "route", "setup"]):
        return make_dimension("environment_leverage", 2, "Candidate uses a concrete context or default.")
    return make_dimension("environment_leverage", 1, "Environment leverage is weakly specified.")


def safe_tie_break_key(candidate: Candidate) -> tuple:
    weak_evidence_safety = 0
    if is_weak_evidence(candidate) and not is_information_or_environment_work(candidate):
        weak_evidence_safety = 1
    return (
        authority_rank(candidate.authority),
        protected_time_rank(candidate.protected_time),
        energy_rank(candidate.energy),
        minutes_from_duration(candidate.duration),
        weak_evidence_safety,
        candidate.name.lower(),
    )


def build_scorecard(candidate: Candidate, args: argparse.Namespace) -> Scorecard:
    dimensions = (
        score_goal_contribution(candidate),
        score_urgency(candidate),
        score_consequence_of_deferral(candidate),
        score_energy_fit(candidate, args),
        score_reversibility(candidate),
        score_downside_protection(candidate),
        score_anxiety_reduction(candidate),
        score_evidence_value(candidate),
        score_environment_leverage(candidate),
    )
    total = sum(dimension.weighted_score for dimension in dimensions)
    strongest = sorted(
        dimensions,
        key=lambda dimension: (dimension.weighted_score, dimension.weight),
        reverse=True,
    )[:2]
    strongest_text = ", ".join(dimension.dimension.replace("_", " ") for dimension in strongest)
    tie_breaker = (
        "Safe tie-break prefers lower authority/protected-time impact, lower energy, "
        "shorter duration, then information or environment-shaping work when evidence is weak."
    )
    evidence_note = " Evidence is weak." if is_weak_evidence(candidate) else ""
    return Scorecard(
        score_total=total,
        score_dimensions=dimensions,
        selection_rationale=(
            f"Score {total}; strongest dimensions: {strongest_text}.{evidence_note} {tie_breaker}"
        ).strip(),
        tie_breaker=tie_breaker,
    )


def scorecard_to_dict(scorecard: Scorecard) -> dict:
    return {
        "score_total": scorecard.score_total,
        "score_dimensions": [
            {
                "dimension": dimension.dimension,
                "weight": dimension.weight,
                "score": dimension.score,
                "weighted_score": dimension.weighted_score,
                "rationale": dimension.rationale,
            }
            for dimension in scorecard.score_dimensions
        ],
        "selection_rationale": scorecard.selection_rationale,
        "tie_breaker": scorecard.tie_breaker,
    }


def scored_candidate_sort_key(scored: ScoredCandidate) -> tuple:
    return (-scored.scorecard.score_total, *safe_tie_break_key(scored.candidate))


def risk_flags(candidate: Candidate) -> list[str]:
    flags: list[str] = []
    text = " ".join(
        [
            candidate.name,
            candidate.domain,
            candidate.authority,
            candidate.status,
            candidate.protected_time,
        ]
    ).lower()
    normalized = text.replace("_", " ").replace("-", " ")
    if "level 2" in normalized or "level 3" in normalized or "level 4" in normalized:
        flags.append("authority")
    if any(
        marker in normalized
        for marker in [
            "escalat",
            "blocked",
            "needs review",
            "needs light review",
            "needs standard review",
            "needs formal review",
            "formal review",
            "review required",
            "requires review",
            "pending review",
        ]
    ):
        flags.append("governance")
    if "medium" in candidate.protected_time.lower() or "high" in candidate.protected_time.lower():
        flags.append("protected time")
    if any(word in text for word in ["medical", "legal", "tax", "quit", "relocation", "housing"]):
        flags.append("high impact")
    return flags


def candidate_score(candidate: Candidate) -> tuple:
    """Compatibility sort key for callers that compare raw candidates."""
    args = argparse.Namespace(energy=None)
    return scored_candidate_sort_key(ScoredCandidate(candidate, build_scorecard(candidate, args)))


def is_active(candidate: Candidate, available_minutes: int | None) -> bool:
    if risk_flags(candidate):
        return False
    if available_minutes is not None and minutes_from_duration(candidate.duration) > available_minutes:
        return False
    return True


def build_queue(
    candidates: list[Candidate],
    args: argparse.Namespace,
) -> QueueBuild:
    active: list[ScoredCandidate] = []
    deferred: list[tuple[ScoredCandidate, str]] = []
    scored_candidates = [
        ScoredCandidate(candidate=candidate, scorecard=build_scorecard(candidate, args))
        for candidate in candidates
    ]

    for scored in sorted(scored_candidates, key=scored_candidate_sort_key):
        candidate = scored.candidate
        flags = risk_flags(candidate)
        if flags:
            deferred.append((scored, "Needs governance review: " + ", ".join(flags)))
            continue
        if args.available is not None and minutes_from_duration(candidate.duration) > args.available:
            deferred.append((scored, f"Does not fit available window of {args.available} minutes"))
            continue
        active.append(scored)

    return QueueBuild(active=active, deferred=deferred, args=args)


def build_markdown_queue(queue: QueueBuild) -> str:
    args = queue.args
    active_rows = []
    for rank, scored in enumerate(queue.active, start=1):
        candidate = scored.candidate
        active_rows.append(
            f"| {rank} | {candidate.name} | {candidate.domain} | {candidate.duration} | {candidate.energy} | {candidate.location} | {candidate.deadline} | {candidate.authority} | Ready | {scored.scorecard.score_total} |"
        )
    if not active_rows:
        active_rows.append("| 1 | Answer targeted operating question | Operations | 5 min | Low | Home | Now | Level 1 | Ready | 0 |")

    deferred_rows = [
        f"| {scored.candidate.name} | {reason} | Next synthesis |"
        for scored, reason in queue.deferred
    ]
    if not deferred_rows:
        deferred_rows.append("| None | No deferred candidates | Next synthesis |")

    scoring_model_rows = [
        f"| {dimension.replace('_', ' ')} | {weight} | {SCORE_DESCRIPTIONS[dimension]} |"
        for dimension, weight in SCORE_WEIGHTS.items()
    ]

    scorecard_rows = []
    for scope, items in (
        ("Active", [(scored, "") for scored in queue.active]),
        ("Deferred", queue.deferred),
    ):
        for scored, deferral_reason in items:
            candidate = scored.candidate
            reason = deferral_reason or "None"
            scorecard_rows.append(
                f"| {scope} | {candidate.name} | {scored.scorecard.score_total} | {scored.scorecard.selection_rationale} | {reason} |"
            )
    if not scorecard_rows:
        scorecard_rows.append("| Fallback | Answer targeted operating question | 0 | No active candidate fit the queue constraints. | Ask one targeted operating question. |")

    strategy_rows = []
    for rank, scored in enumerate(queue.active, start=1):
        candidate = scored.candidate
        target = candidate.target_behavior or "Not specified."
        environment = candidate.environment_design or "Not specified."
        strategy_rows.append(f"| {rank} | {candidate.name} | {target} | {environment} |")
    if not strategy_rows:
        strategy_rows.append("| 1 | Answer targeted operating question | Identify the missing decision-grade fact. | Create enough context to resynthesize safely. |")

    state_lines = [
        f"- Time: {args.time or 'Unknown'}",
        f"- Location: {args.location or 'Unknown'}",
        f"- Energy: {args.energy or 'Unknown'}",
        f"- Weather/environment: {args.environment or 'Unknown'}",
        f"- Active obligations: {args.obligations or 'Unknown'}",
        f"- Known constraints: {args.constraints or 'Unknown'}",
    ]

    return "\n".join(
        [
            f"# Directive Queue: {args.date}",
            "",
            "## Date or Session",
            "",
            args.date,
            "",
            "## Operating Frame",
            "",
            args.frame,
            "",
            "## Protected Time",
            "",
            args.protected_time or "Unknown.",
            "",
            "## Current State",
            "",
            *state_lines,
            "",
            "## Completed",
            "",
            "| Time | Directive | Outcome |",
            "| --- | --- | --- |",
            "| TBD | TBD | TBD |",
            "",
            "## Active Candidates",
            "",
            "| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status | Score |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *active_rows,
            "",
            "## Scoring Model",
            "",
            f"Model: `{SCORING_MODEL}`. Score range is 0-3 per dimension before weighting. Governance deferral remains a hard gate before selection.",
            "",
            "| Dimension | Weight | Description |",
            "| --- | --- | --- |",
            *scoring_model_rows,
            "",
            "Safe tie-break order: lower authority, lower protected-time impact, lower required energy, shorter duration, then information-gathering or environment-shaping work when evidence is weak.",
            "",
            "## Scorecards",
            "",
            "| Scope | Candidate | Score | Selection Rationale | Deferral Reason |",
            "| --- | --- | --- | --- | --- |",
            *scorecard_rows,
            "",
            "## Behavioral Strategy",
            "",
            "| Rank | Candidate | Target Behavior | Environment Design |",
            "| --- | --- | --- | --- |",
            *strategy_rows,
            "",
            "## Deferred",
            "",
            "| Candidate | Reason Deferred | Next Review |",
            "| --- | --- | --- |",
            *deferred_rows,
            "",
            "## Blocked",
            "",
            "| Candidate | Blocker | Required Change |",
            "| --- | --- | --- |",
            "| None | None | None |",
            "",
            "## Next Directive",
            "",
            "Select via `ops/directives/next_directive.py` or `ops/operator/next_step.py`.",
            "",
            "## Next Check-In",
            "",
            "After completion, blockage, or material state change.",
            "",
        ]
    )


def normalize_energy(value: str) -> str:
    normalized = value.strip().lower()
    if "low" in normalized:
        return "low"
    if "medium" in normalized:
        return "medium"
    if "high" in normalized:
        return "high"
    return "unknown"


def normalize_authority(value: str) -> str:
    normalized = value.strip().lower().replace("-", " ")
    mapping = {
        "level 0": "level_0_observe",
        "level 1": "level_1_recommend",
        "level 2": "level_2_direct",
        "level 3": "level_3_execute",
        "level 4": "level_4_escalate",
    }
    for marker, authority in mapping.items():
        if marker in normalized:
            return authority
    return "level_1_recommend"


def normalize_governance_status(value: str) -> str:
    normalized = value.strip().lower()
    if "blocked" in normalized:
        return "blocked"
    if "reject" in normalized:
        return "rejected"
    if "formal" in normalized or "escalat" in normalized or "level 4" in normalized:
        return "needs_formal_review"
    if "standard" in normalized or "needs review" in normalized:
        return "needs_standard_review"
    if "light" in normalized:
        return "needs_light_review"
    if "ready" in normalized or "reviewed" in normalized or "conditional" in normalized:
        return "ready"
    return "draft"


def deferred_governance_status(candidate: Candidate, reason: str) -> str:
    normalized_reason = reason.lower()
    if "blocked" in normalized_reason or "blocked" in candidate.status.lower():
        return "blocked"
    if any(flag in normalized_reason for flag in ["authority", "governance", "high impact"]):
        return "needs_formal_review"
    if "protected time" in normalized_reason:
        return "needs_standard_review"
    return normalize_governance_status(candidate.status)


def split_arg_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def build_json_queue(queue: QueueBuild) -> dict:
    args = queue.args
    active = queue.active
    deferred = queue.deferred
    if active:
        selected = active[0]
        candidate = selected.candidate
        next_directive = {
            "candidate_id": "candidate-1",
            "directive": candidate.name,
            "selection_rationale": selected.scorecard.selection_rationale,
            "authority_level": normalize_authority(candidate.authority),
            "governance_status": "ready",
            "target_behavior": candidate.target_behavior,
            "environment_design": candidate.environment_design,
            "score_total": selected.scorecard.score_total,
            "scorecard": scorecard_to_dict(selected.scorecard),
        }
    else:
        next_directive = {
            "candidate_id": "",
            "directive": "Answer targeted operating question",
            "selection_rationale": "No active candidate fit the current queue constraints.",
            "authority_level": "level_1_recommend",
            "governance_status": "ready",
            "target_behavior": "Create the missing condition for PEGO to select a directive.",
            "environment_design": "Ask one targeted operational question instead of issuing a broad reflection prompt.",
            "score_total": 0,
            "scorecard": {
                "score_total": 0,
                "score_dimensions": [],
                "selection_rationale": "No active candidate fit the current queue constraints.",
                "tie_breaker": "Fallback asks one targeted question instead of expanding scope.",
            },
        }

    return {
        "artifact_type": "directive_queue",
        "schema_version": 1,
        "session": args.date,
        "operating_frame": args.frame,
        "scoring_model": scoring_model_dict(),
        "protected_time": [
            {
                "label": "Protected time",
                "window": args.protected_time,
                "protection_level": "hard",
            }
        ]
        if args.protected_time
        else [],
        "current_state": {
            "time": args.time or "",
            "location": args.location or "",
            "energy": normalize_energy(args.energy or ""),
            "environment": args.environment or "",
            "active_obligations": split_arg_list(args.obligations),
            "known_constraints": split_arg_list(args.constraints),
        },
        "completed": [],
        "active_candidates": [
            {
                "rank": rank,
                "candidate_id": f"candidate-{rank}",
                "candidate": scored.candidate.name,
                "domain": scored.candidate.domain,
                "duration": scored.candidate.duration,
                "energy": normalize_energy(scored.candidate.energy),
                "location": scored.candidate.location,
                "deadline": scored.candidate.deadline,
                "authority_level": normalize_authority(scored.candidate.authority),
                "governance_status": "ready",
                "target_behavior": scored.candidate.target_behavior,
                "environment_design": scored.candidate.environment_design,
                "source": scored.candidate.source,
                "score_total": scored.scorecard.score_total,
                "scorecard": scorecard_to_dict(scored.scorecard),
                "selection_rationale": scored.scorecard.selection_rationale,
            }
            for rank, scored in enumerate(active, start=1)
        ],
        "deferred": [
            {
                "candidate_id": f"deferred-{index}",
                "candidate": scored.candidate.name,
                "reason_deferred": reason,
                "deferral_reason": reason,
                "next_review": "Next synthesis",
                "consequence_of_deferral": scored.candidate.deferral,
                "authority_level": normalize_authority(scored.candidate.authority),
                "governance_status": deferred_governance_status(scored.candidate, reason),
                "score_total": scored.scorecard.score_total,
                "scorecard": scorecard_to_dict(scored.scorecard),
                "selection_rationale": scored.scorecard.selection_rationale,
            }
            for index, (scored, reason) in enumerate(deferred, start=1)
        ],
        "blocked": [],
        "next_directive": next_directive,
        "next_check_in": "After completion, blockage, or material state change.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--candidate", type=Path, action="append", default=[])
    parser.add_argument("--available", type=int)
    parser.add_argument("--time")
    parser.add_argument("--location")
    parser.add_argument("--energy")
    parser.add_argument("--environment")
    parser.add_argument("--obligations")
    parser.add_argument("--constraints")
    parser.add_argument("--protected-time", default="")
    parser.add_argument("--frame", default="Synthesize current candidate directives into one active queue.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    if not args.candidate:
        raise SystemExit("at least one --candidate file is required")

    candidates = read_candidates(args.candidate)
    output = args.output or private / "directives" / "queues" / f"{args.date}-queue.md"
    queue = build_queue(candidates, args)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_markdown_queue(queue))
    print(f"wrote: {output}")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        if args.json_output.exists() and not args.force:
            raise SystemExit(f"refusing to overwrite existing file: {args.json_output}")
        args.json_output.write_text(json.dumps(build_json_queue(queue), indent=2) + "\n")
        print(f"wrote: {args.json_output}")


if __name__ == "__main__":
    main_with_args()
