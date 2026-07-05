#!/usr/bin/env python3
"""Synthesize PEGO agent recommendations into a council decision."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


def load_goal_reconciler():
    path = ROOT / "ops" / "goals" / "reconcile_goals.py"
    spec = importlib.util.spec_from_file_location("goal_reconcile_goals", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load goal reconciliation runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


goal_reconcile_goals = load_goal_reconciler()


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

HIGH_RISKS = {"financial", "health", "relationship", "career", "legal", "tax", "privacy"}


@dataclass(frozen=True)
class Recommendation:
    source: str
    agent: str
    recommendation_type: str
    proposed_directive: str
    authority_level: str
    relevant_facts: list[str]
    assumptions: list[str]
    evidence_quality: list[str]
    expected_benefit: str
    costs_and_tradeoffs: list[str]
    risks: list[str]
    reversibility: str
    privacy_impact: str
    required_handoffs: list[str]
    dissent: str
    stop_conditions: list[str]
    review: str
    claims: list[str]
    objections: list[str]
    concessions: list[str]
    evidence_gaps: list[str]
    vetoes: list[str]
    deferrals: list[str]


@dataclass(frozen=True)
class AgentCalibration:
    agent: str
    record_count: int
    score_delta_total: int
    calibration_actions: tuple[str, ...]
    cautions: tuple[str, ...]
    future_weighting_notes: tuple[str, ...]
    selection_adjustment: int


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


def clean_value(value: object) -> str:
    if isinstance(value, dict):
        statement = value.get("statement")
        certainty = value.get("certainty")
        if statement and certainty:
            return f"{statement} (certainty: {certainty})"
        if statement:
            return str(statement).strip()
        return json.dumps(value, sort_keys=True)
    return str(value).strip()


def split_values(value: object) -> list[str]:
    if isinstance(value, list):
        values = []
        for item in value:
            cleaned = clean_value(item)
            if cleaned:
                values.append(cleaned)
        return values
    if not value:
        return []
    values = []
    for line in str(value).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        values.extend(part.strip() for part in stripped.split(";") if part.strip())
    return values


def unique_values(values: list[str]) -> list[str]:
    seen = set()
    unique = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            unique.append(cleaned)
    return unique


def normalize_choice(value: object) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def normalize_agent_key(value: object) -> str:
    text = str(value or "").lower()
    text = text.replace("agent", "")
    return "".join(char for char in text if char.isalnum())


def normalize_risks(values: object) -> list[str]:
    risks = []
    for value in split_values(values):
        normalized = normalize_choice(value)
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
            recommendation_type=normalize_choice(data.get("recommendation_type", "recommend")),
            proposed_directive=str(data.get("proposed_directive", "")),
            authority_level=str(data.get("authority_level", "level_1_recommend")),
            relevant_facts=split_values(data.get("relevant_facts", [])),
            assumptions=split_values(data.get("assumptions", [])),
            evidence_quality=split_values(data.get("evidence_quality", [])),
            expected_benefit=str(data.get("expected_benefit", "")),
            costs_and_tradeoffs=split_values(data.get("costs_and_tradeoffs", [])),
            risks=normalize_risks(data.get("risks", [])),
            reversibility=str(data.get("reversibility", "")),
            privacy_impact=str(data.get("privacy_impact", "")),
            required_handoffs=split_values(data.get("required_handoffs", [])),
            dissent=str(data.get("dissent", "")),
            stop_conditions=split_values(data.get("stop_conditions", [])),
            review=str(review.get("review_date_or_success_criteria", "")),
            claims=split_values(data.get("claims", [])),
            objections=split_values(data.get("objections", [])),
            concessions=split_values(data.get("concessions", [])),
            evidence_gaps=split_values(data.get("evidence_gaps", [])),
            vetoes=unique_values(split_values(data.get("vetoes", [])) + split_values(data.get("veto", []))),
            deferrals=split_values(data.get("deferrals", [])),
        )

    sections = parse_sections(text)
    return Recommendation(
        source=str(path),
        agent=first_line(sections.get("Agent", ""), "Unknown"),
        recommendation_type=normalize_choice(first_line(sections.get("Recommendation Type", ""), "Recommend")),
        proposed_directive=first_line(sections.get("Proposed Directive", ""), path.stem),
        authority_level=first_line(sections.get("Authority Level", ""), "Level 1"),
        relevant_facts=split_values(sections.get("Relevant Facts", "")),
        assumptions=split_values(sections.get("Assumptions", "")),
        evidence_quality=split_values(sections.get("Evidence Quality", "")),
        expected_benefit=first_line(sections.get("Expected Benefit", ""), ""),
        costs_and_tradeoffs=split_values(sections.get("Costs and Tradeoffs", "")),
        risks=normalize_risks(sections.get("Risks", "")),
        reversibility=first_line(sections.get("Reversibility", ""), ""),
        privacy_impact=first_line(sections.get("Privacy Impact", ""), ""),
        required_handoffs=split_values(sections.get("Required Handoffs", "")),
        dissent=sections.get("Dissent", ""),
        stop_conditions=split_values(sections.get("Stop Conditions", "")),
        review=first_line(sections.get("Review Date or Success Criteria", ""), "Next review."),
        claims=split_values(sections.get("Claims", "")),
        objections=split_values(sections.get("Objections", "")),
        concessions=split_values(sections.get("Concessions", "")),
        evidence_gaps=split_values(sections.get("Evidence Gaps", "")),
        vetoes=unique_values(split_values(sections.get("Vetoes", "")) + split_values(sections.get("Veto", ""))),
        deferrals=split_values(sections.get("Deferrals", "")),
    )


def read_agent_calibration(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"agent calibration is not valid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("artifact_type") != "agent_calibration_record":
        raise SystemExit(f"not an agent calibration record: {path}")
    return data


def calibration_action_adjustment(action: str) -> int:
    return {
        "increase_weight": 1,
        "keep_weight": 0,
        "decrease_weight": -1,
        "quarantine": -3,
        "escalate": -2,
    }.get(action, 0)


def build_calibration_context(paths: list[Path] | None) -> dict[str, AgentCalibration]:
    entries: dict[str, dict[str, object]] = {}
    for path in paths or []:
        record = read_agent_calibration(path)
        agent = str(record.get("agent", "Unknown Agent"))
        key = normalize_agent_key(agent)
        entry = entries.setdefault(
            key,
            {
                "agent": agent,
                "record_count": 0,
                "score_delta_total": 0,
                "calibration_actions": [],
                "cautions": [],
                "future_weighting_notes": [],
                "selection_adjustment": 0,
            },
        )
        action = str(record.get("calibration_action", "keep_weight"))
        score_delta = int(record.get("score_delta", 0))
        entry["record_count"] = int(entry["record_count"]) + 1
        entry["score_delta_total"] = int(entry["score_delta_total"]) + score_delta
        entry["selection_adjustment"] = (
            int(entry["selection_adjustment"])
            + score_delta
            + calibration_action_adjustment(action)
        )
        actions = entry["calibration_actions"]
        if isinstance(actions, list):
            actions.append(action)
        cautions = entry["cautions"]
        if isinstance(cautions, list):
            cautions.extend(split_values(record.get("cautions", [])))
        notes = entry["future_weighting_notes"]
        if isinstance(notes, list):
            note = str(record.get("future_weighting_note", "")).strip()
            if note:
                notes.append(note)

    return {
        key: AgentCalibration(
            agent=str(value["agent"]),
            record_count=int(value["record_count"]),
            score_delta_total=int(value["score_delta_total"]),
            calibration_actions=tuple(unique_values([str(item) for item in value["calibration_actions"]])),
            cautions=tuple(unique_values([str(item) for item in value["cautions"]])),
            future_weighting_notes=tuple(unique_values([str(item) for item in value["future_weighting_notes"]])),
            selection_adjustment=int(value["selection_adjustment"]),
        )
        for key, value in entries.items()
    }


def calibration_for_agent(
    item: Recommendation,
    context: dict[str, AgentCalibration],
) -> AgentCalibration | None:
    return context.get(normalize_agent_key(item.agent))


def calibration_context_rows(context: dict[str, AgentCalibration]) -> list[dict[str, object]]:
    return [
        {
            "agent": item.agent,
            "record_count": item.record_count,
            "score_delta_total": item.score_delta_total,
            "calibration_actions": list(item.calibration_actions),
            "cautions": list(item.cautions),
            "future_weighting_notes": list(item.future_weighting_notes),
            "selection_adjustment": item.selection_adjustment,
        }
        for item in sorted(context.values(), key=lambda record: record.agent)
    ]


def authority_requires_escalation(item: Recommendation) -> bool:
    authority = item.authority_level.lower()
    return "level_4" in authority or "level 4" in authority


def has_high_risk(item: Recommendation) -> bool:
    return bool(HIGH_RISKS.intersection(item.risks))


def has_veto(item: Recommendation) -> bool:
    return bool(item.vetoes) or normalize_choice(item.privacy_impact) == "blocked"


def outcome(recommendations: list[Recommendation]) -> str:
    if any(has_veto(item) for item in recommendations):
        return "block"
    if any(item.recommendation_type == "dissent" for item in recommendations):
        return "revise"
    if any(item.recommendation_type == "escalate" for item in recommendations):
        return "escalate"
    if any(authority_requires_escalation(item) for item in recommendations):
        return "escalate"
    if any(has_high_risk(item) for item in recommendations):
        return "escalate"
    if any(item.recommendation_type == "request_more_information" for item in recommendations):
        return "request_more_information"
    return "adopt"


def choose_directive(recommendations: list[Recommendation], selected_index: int) -> str:
    selected = recommendations[selected_index]
    if selected.recommendation_type in {"recommend", "direct"} and selected.proposed_directive:
        return selected.proposed_directive
    for item in recommendations:
        if item.recommendation_type in {"recommend", "direct"} and item.proposed_directive:
            return item.proposed_directive
    return recommendations[0].proposed_directive or "Request more information."


def selected_recommendation_index(
    recommendations: list[Recommendation],
    calibration_context: dict[str, AgentCalibration] | None = None,
) -> int:
    calibration_context = calibration_context or {}
    selected = 0
    best_adjustment: int | None = None
    for index, item in enumerate(recommendations):
        if item.recommendation_type in {"recommend", "direct"} and item.proposed_directive:
            calibration = calibration_for_agent(item, calibration_context)
            adjustment = calibration.selection_adjustment if calibration else 0
            if best_adjustment is None or adjustment > best_adjustment:
                selected = index
                best_adjustment = adjustment
    return selected


def goal_context(
    goal_reconciliations: list[Path],
    priority_assumption: str,
) -> tuple[str, list[str], str]:
    sources = [str(path) for path in goal_reconciliations]
    if sources:
        return "current_goal_reconciliation_supplied", sources, priority_assumption
    if priority_assumption:
        return "temporary_priority_assumption", [], priority_assumption
    return (
        "missing_goal_reconciliation",
        [],
        "Temporary conservative assumption: select only low-risk, reversible directives unless a recommendation requests information or a high-impact risk requires escalation.",
    )


def prefix_values(agent: str, values: list[str]) -> list[str]:
    return [f"{agent}: {value}" for value in values if value]


def recommendation_claims(item: Recommendation) -> list[str]:
    claims = prefix_values(item.agent, item.claims)
    if not claims:
        if item.proposed_directive and item.expected_benefit:
            claims.append(f"{item.agent}: proposes {item.proposed_directive}; expected benefit: {item.expected_benefit}")
        elif item.proposed_directive:
            claims.append(f"{item.agent}: proposes {item.proposed_directive}")
    if item.relevant_facts:
        claims.append(f"{item.agent}: facts considered: {', '.join(item.relevant_facts)}")
    return claims


def recommendation_objections(item: Recommendation) -> list[str]:
    objections = prefix_values(item.agent, item.objections)
    if item.dissent:
        objections.append(f"{item.agent}: {item.dissent}")
    elif item.recommendation_type == "dissent":
        objections.append(f"{item.agent}: dissent recommendation: {item.proposed_directive}")
    if item.risks:
        objections.append(f"{item.agent}: risk categories: {', '.join(item.risks)}")
    if item.costs_and_tradeoffs:
        objections.append(f"{item.agent}: costs/tradeoffs: {'; '.join(item.costs_and_tradeoffs)}")
    return objections


def recommendation_concessions(item: Recommendation) -> list[str]:
    concessions = prefix_values(item.agent, item.concessions)
    reversibility = normalize_choice(item.reversibility)
    privacy = normalize_choice(item.privacy_impact)
    if item.required_handoffs:
        concessions.append(f"{item.agent}: handoff required before full adoption: {', '.join(item.required_handoffs)}")
    if reversibility and reversibility != "easy_to_reverse":
        concessions.append(f"{item.agent}: reversibility constraint: {item.reversibility}")
    if privacy and privacy != "private_only":
        concessions.append(f"{item.agent}: privacy constraint: {item.privacy_impact}")
    return concessions


def recommendation_evidence_gaps(item: Recommendation) -> list[str]:
    gaps = prefix_values(item.agent, item.evidence_gaps)
    evidence = {normalize_choice(value) for value in item.evidence_quality}
    if item.recommendation_type == "request_more_information":
        gaps.append(f"{item.agent}: requested information before adoption: {item.proposed_directive}")
    if "speculation" in evidence:
        gaps.append(f"{item.agent}: evidence quality includes speculation.")
    if not item.relevant_facts:
        gaps.append(f"{item.agent}: no relevant facts recorded.")
    for assumption in item.assumptions:
        if "certainty: low" in assumption.lower() or assumption.lower().endswith("(low)"):
            gaps.append(f"{item.agent}: low-certainty assumption: {assumption}")
    return gaps


def recommendation_vetoes(item: Recommendation) -> list[str]:
    vetoes = prefix_values(item.agent, item.vetoes)
    if normalize_choice(item.privacy_impact) == "blocked":
        vetoes.append(f"{item.agent}: privacy impact is blocked.")
    return vetoes


def unresolved_dissent(recommendations: list[Recommendation]) -> list[str]:
    return unique_values(
        [
            f"{item.agent}: {item.dissent or item.proposed_directive}"
            for item in recommendations
            if item.dissent or item.recommendation_type == "dissent"
        ]
    )


def build_deliberation_summary(recommendations: list[Recommendation]) -> dict[str, list[str]]:
    return {
        "claims": unique_values([value for item in recommendations for value in recommendation_claims(item)]),
        "objections": unique_values([value for item in recommendations for value in recommendation_objections(item)]),
        "concessions": unique_values([value for item in recommendations for value in recommendation_concessions(item)]),
        "evidence_gaps": unique_values([value for item in recommendations for value in recommendation_evidence_gaps(item)]),
        "vetoes": unique_values([value for item in recommendations for value in recommendation_vetoes(item)]),
        "unresolved_dissent": unresolved_dissent(recommendations),
    }


def scorecard_status(
    item: Recommendation,
    index: int,
    selected_index: int,
    council_outcome: str,
) -> str:
    if has_veto(item):
        return "blocked"
    if item.recommendation_type == "dissent":
        return "unresolved_dissent"
    if item.recommendation_type == "request_more_information":
        return "information_request"
    if item.recommendation_type == "escalate" or authority_requires_escalation(item) or has_high_risk(item):
        return "escalated"
    if index == selected_index:
        return {
            "adopt": "selected",
            "revise": "proposed_for_revision",
            "request_more_information": "held_for_information",
            "escalate": "held_for_governance",
            "block": "blocked",
        }.get(council_outcome, "proposed")
    return "deferred"


def build_tradeoff_scorecard(
    recommendations: list[Recommendation],
    council_outcome: str,
    selected_index: int,
    calibration_context: dict[str, AgentCalibration],
) -> list[dict[str, object]]:
    rows = []
    for index, item in enumerate(recommendations):
        calibration = calibration_for_agent(item, calibration_context)
        rows.append(
            {
                "agent": item.agent,
                "recommendation_type": item.recommendation_type,
                "proposed_directive": item.proposed_directive,
                "selection_status": scorecard_status(item, index, selected_index, council_outcome),
                "authority_level": item.authority_level,
                "expected_benefit": item.expected_benefit,
                "tradeoffs": item.costs_and_tradeoffs,
                "risks": item.risks,
                "evidence_quality": item.evidence_quality,
                "reversibility": item.reversibility,
                "privacy_impact": item.privacy_impact,
                "required_handoffs": item.required_handoffs,
                "calibration_score_delta": calibration.score_delta_total if calibration else 0,
                "calibration_actions": list(calibration.calibration_actions) if calibration else [],
                "calibration_adjustment": calibration.selection_adjustment if calibration else 0,
                "calibration_note": (
                    "; ".join(calibration.future_weighting_notes)
                    if calibration and calibration.future_weighting_notes
                    else ""
                ),
            }
        )
    return rows


def build_deferrals(
    recommendations: list[Recommendation],
    council_outcome: str,
    selected_index: int,
) -> list[str]:
    deferrals = [
        value
        for item in recommendations
        for value in prefix_values(item.agent, item.deferrals)
    ]
    if council_outcome != "adopt":
        return unique_values(deferrals)
    for index, item in enumerate(recommendations):
        if index == selected_index:
            continue
        if item.recommendation_type not in {"recommend", "direct"} or not item.proposed_directive:
            continue
        if item.expected_benefit:
            deferrals.append(
                f"{item.agent}: deferred {item.proposed_directive}; benefit preserved for review: {item.expected_benefit}"
            )
        else:
            deferrals.append(f"{item.agent}: deferred {item.proposed_directive}")
    return unique_values(deferrals)


def build_tradeoff_rationale(
    council_outcome: str,
    directive: str,
    risks: list[str],
    evidence_gaps: list[str],
    vetoes: list[str],
    dissent: list[str],
    deferrals: list[str],
    calibration_rows: list[dict[str, object]],
) -> str:
    if council_outcome == "block":
        base = "Blocked because a veto or blocked privacy impact is present."
    elif council_outcome == "revise":
        base = "Revision required because unresolved dissent is present."
    elif council_outcome == "request_more_information":
        base = "Information requested because the current evidence is not decision-grade."
    elif council_outcome == "escalate":
        base = "Escalation required because authority level or high-risk categories prevent normal adoption."
    else:
        base = f"Selected {directive} as the first eligible adoptable recommendation under the current priority model."
    risk_text = ", ".join(risks) if risks else "none"
    calibration_text = (
        " Calibration was supplied and affected eligible recommendation weighting."
        if any(int(row.get("selection_adjustment", 0)) for row in calibration_rows)
        else " No calibration adjustment affected eligible recommendation weighting."
    )
    return (
        f"{base} Key risks: {risk_text}. "
        f"Evidence gaps recorded: {len(evidence_gaps)}. "
        f"Vetoes recorded: {len(vetoes)}. "
        f"Unresolved dissent items: {len(dissent)}. "
        f"Deferrals recorded: {len(deferrals)}."
        f"{calibration_text}"
    )


def build_artifact(
    recommendations: list[Recommendation],
    decision_date: str,
    frame: str,
    goal_reconciliations: list[Path] | None = None,
    priority_assumption: str = "",
    agent_calibrations: list[Path] | None = None,
) -> dict[str, object]:
    if not recommendations:
        raise SystemExit("at least one recommendation is required")
    council_outcome = outcome(recommendations)
    calibration_context = build_calibration_context(agent_calibrations)
    selected_index = selected_recommendation_index(recommendations, calibration_context)
    directive = choose_directive(recommendations, selected_index)
    calibration_rows = calibration_context_rows(calibration_context)
    goal_status, goal_sources, active_priority_assumption = goal_context(
        goal_reconciliations or [],
        priority_assumption,
    )
    risks = sorted({risk for item in recommendations for risk in item.risks})
    dissent = [
        f"{item.agent}: {item.dissent or item.proposed_directive}"
        for item in recommendations
        if item.dissent or item.recommendation_type == "dissent"
    ]
    handoffs = sorted({handoff for item in recommendations for handoff in item.required_handoffs})
    stops = sorted({stop for item in recommendations for stop in item.stop_conditions})
    deliberation_summary = build_deliberation_summary(recommendations)
    deferrals = build_deferrals(recommendations, council_outcome, selected_index)
    tradeoff_scorecard = build_tradeoff_scorecard(
        recommendations,
        council_outcome,
        selected_index,
        calibration_context,
    )
    tradeoff_rationale = build_tradeoff_rationale(
        council_outcome,
        directive,
        risks,
        deliberation_summary["evidence_gaps"],
        deliberation_summary["vetoes"],
        deliberation_summary["unresolved_dissent"],
        deferrals,
        calibration_rows,
    )
    if council_outcome == "adopt":
        governance = "Level 1 council synthesis; no authority increase approved."
        next_action = directive
    elif council_outcome == "block":
        governance = "Council veto preserved; adoption is blocked until governance clears the constraint."
        next_action = "Stop adoption and resolve the veto before directive synthesis."
    elif council_outcome == "revise":
        governance = "Council dissent preserved; revise before directive synthesis."
        next_action = "Revise the directive and rerun council synthesis."
    elif council_outcome == "request_more_information":
        governance = "Insufficient decision-grade evidence."
        next_action = "Ask the targeted information request before directive synthesis."
    else:
        governance = "Governance review required before adoption or execution."
        next_action = "Create or update a decision packet before adoption."
    if goal_status != "current_goal_reconciliation_supplied":
        governance = f"{governance} Goal reconciliation status: {goal_status}."

    return {
        "artifact_type": "council_decision",
        "schema_version": 2,
        "date": decision_date,
        "decision_frame": frame,
        "goal_reconciliation_status": goal_status,
        "goal_reconciliation_sources": goal_sources,
        "priority_assumption": active_priority_assumption,
        "source_recommendations": [item.source for item in recommendations],
        "proposed_directive": directive,
        "council_outcome": council_outcome,
        "rationale": "Synthesized from agent recommendations while preserving dissent, risks, handoffs, and authority constraints.",
        "expected_benefit": " | ".join(item.expected_benefit for item in recommendations if item.expected_benefit),
        "key_risks": risks,
        "dissent": dissent,
        "deliberation_summary": deliberation_summary,
        "evidence_gaps": deliberation_summary["evidence_gaps"],
        "vetoes": deliberation_summary["vetoes"],
        "unresolved_dissent": deliberation_summary["unresolved_dissent"],
        "tradeoff_rationale": tradeoff_rationale,
        "tradeoff_scorecard": tradeoff_scorecard,
        "agent_calibration_context": calibration_rows,
        "deferrals": deferrals,
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

    def summary_lines(value: object) -> list[str]:
        summary = value if isinstance(value, dict) else {}
        lines = []
        labels = [
            ("Claims", "claims"),
            ("Objections", "objections"),
            ("Concessions", "concessions"),
            ("Evidence Gaps", "evidence_gaps"),
            ("Vetoes", "vetoes"),
            ("Unresolved Dissent", "unresolved_dissent"),
        ]
        for label, key in labels:
            lines.append(f"{label}:")
            lines.extend(bullets(summary.get(key, [])))
            lines.append("")
        return lines[:-1]

    def scorecard_lines(value: object) -> list[str]:
        rows = value if isinstance(value, list) else []
        lines = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            risks = ", ".join(str(item) for item in row.get("risks", [])) or "none"
            evidence = ", ".join(str(item) for item in row.get("evidence_quality", [])) or "none"
            calibration = row.get("calibration_adjustment", 0)
            directive = str(row.get("proposed_directive", ""))
            lines.append(
                "- "
                f"{row.get('agent', 'Unknown')} | "
                f"{row.get('selection_status', 'unclassified')} | "
                f"{directive} | "
                f"authority: {row.get('authority_level', '')} | "
                f"risks: {risks} | "
                f"evidence: {evidence} | "
                f"calibration adjustment: {calibration}"
            )
        return lines or ["- None."]

    def calibration_lines(value: object) -> list[str]:
        rows = value if isinstance(value, list) else []
        lines = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            actions = ", ".join(str(item) for item in row.get("calibration_actions", [])) or "none"
            notes = "; ".join(str(item) for item in row.get("future_weighting_notes", [])) or "none"
            lines.append(
                "- "
                f"{row.get('agent', 'Unknown')} | "
                f"records: {row.get('record_count', 0)} | "
                f"score delta: {row.get('score_delta_total', 0)} | "
                f"adjustment: {row.get('selection_adjustment', 0)} | "
                f"actions: {actions} | "
                f"notes: {notes}"
            )
        return lines or ["- None supplied."]

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
            "## Goal Reconciliation Status",
            "",
            str(artifact["goal_reconciliation_status"]),
            "",
            "## Goal Reconciliation Sources",
            "",
            *bullets(artifact["goal_reconciliation_sources"]),
            "",
            "## Priority Assumption",
            "",
            str(artifact["priority_assumption"]),
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
            "## Deliberation Summary",
            "",
            *summary_lines(artifact.get("deliberation_summary", {})),
            "",
            "## Tradeoff Rationale",
            "",
            str(artifact["tradeoff_rationale"]),
            "",
            "## Tradeoff Scorecard",
            "",
            *scorecard_lines(artifact["tradeoff_scorecard"]),
            "",
            "## Agent Calibration Context",
            "",
            *calibration_lines(artifact.get("agent_calibration_context", [])),
            "",
            "## Deferrals",
            "",
            *bullets(artifact["deferrals"]),
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
    parser.add_argument("--goal-reconciliation", type=Path, action="append", default=[])
    parser.add_argument("--agent-calibration", type=Path, action="append", default=[])
    parser.add_argument("--priority-assumption", default="")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def existing_goal_reconciliations(private: Path) -> list[Path]:
    candidates = [
        private / "goals" / "goal-reconciliation.json",
        private / "goals" / "goal-reconciliation.md",
    ]
    return [path for path in candidates if path.is_file()]


def should_auto_build_goal_reconciliation(args: argparse.Namespace, output_was_provided: bool) -> bool:
    return bool(args.private_root) or not output_was_provided


def resolve_goal_reconciliations(
    args: argparse.Namespace,
    private: Path,
    output_was_provided: bool,
) -> list[Path]:
    if args.goal_reconciliation:
        return args.goal_reconciliation

    existing = existing_goal_reconciliations(private)
    if existing:
        return existing[:1]

    if not should_auto_build_goal_reconciliation(args, output_was_provided):
        return []

    goal_reconcile_goals.main_with_args(
        [
            "--private-root",
            str(private),
            "--date",
            args.date,
        ]
    )
    return existing_goal_reconciliations(private)[:1]


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    output_was_provided = args.output is not None
    args.output = args.output or private / "council" / "decisions" / "council-decision.md"
    if not args.recommendation:
        raise SystemExit("at least one --recommendation file is required")
    goal_reconciliations = resolve_goal_reconciliations(args, private, output_was_provided)
    recommendations = [read_recommendation(path) for path in args.recommendation]
    artifact = build_artifact(
        recommendations,
        args.date,
        args.frame,
        goal_reconciliations,
        args.priority_assumption,
        args.agent_calibration,
    )
    write_output(args.output, build_markdown(artifact), args.force)
    print(f"wrote: {args.output}")
    if args.json_output:
        write_output(args.json_output, json.dumps(artifact, indent=2, sort_keys=True) + "\n", args.force)
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
