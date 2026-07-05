#!/usr/bin/env python3
"""Review a protected PEGO directive outcome into a learning decision."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


MISSING_ASSESSMENT = {"rating": "missing", "notes": "Source artifact was not available for review."}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "outcome-review"


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


def read_outcome_sections(outcome_path: Path) -> dict[str, str]:
    text = outcome_path.read_text()
    if outcome_path.suffix == ".json":
        data = json.loads(text)
        if data.get("artifact_type") != "directive_outcome":
            raise SystemExit("json outcome must have artifact_type directive_outcome")
        return sections_from_json_outcome(data)
    return parse_sections(text)


def sections_from_json_outcome(data: dict[str, object]) -> dict[str, str]:
    def text_field(name: str, fallback: str = "") -> str:
        value = data.get(name, fallback)
        return str(value) if value is not None else fallback

    def list_field(name: str) -> str:
        value = data.get(name, [])
        if isinstance(value, list):
            return "\n".join(str(item) for item in value) or "None recorded."
        return str(value)

    completion = text_field("completion", "unknown").replace("_", " ").title()
    return {
        "Date": text_field("date"),
        "Source Directive": text_field("source_directive"),
        "Directive Summary": text_field("directive_summary"),
        "Completion": completion,
        "What Happened": text_field("what_happened", "Not supplied."),
        "Evidence": list_field("evidence"),
        "Friction": list_field("friction"),
        "Benefit": text_field("benefit", "None recorded."),
        "Outcome Progress": text_field("outcome_progress", "None recorded."),
        "Contentment Signal": text_field("contentment_signal", "Unknown"),
        "Cost": text_field("cost", "None recorded."),
        "Protected-Time Impact": text_field("protected_time_impact", "none").title(),
        "Stakeholder Impact": text_field("stakeholder_impact", "None recorded."),
        "Environment Impact": text_field("environment_impact", "None recorded."),
        "Follow-Up Directive Candidates": list_field("follow_up_directive_candidates"),
        "Agent Updates": list_field("agent_updates"),
        "Governance Notes": text_field("governance_notes", "None recorded."),
        "Next Review": text_field("next_review", "Next weekly review."),
    }


def first_line(value: str, fallback: str = "Not supplied.") -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return fallback


def completion_key(completion: str) -> str:
    normalized = completion.lower()
    if "completed" in normalized and "partially" not in normalized and "not" not in normalized:
        return "completed"
    if "partially" in normalized or "partial" in normalized:
        return "partial"
    if "not completed" in normalized:
        return "not_completed"
    if "blocked" in normalized:
        return "blocked"
    if "canceled" in normalized or "cancelled" in normalized:
        return "canceled"
    return "unknown"


def has_real_content(value: str) -> bool:
    normalized = value.strip().lower()
    return bool(normalized) and normalized not in {
        "none",
        "none recorded.",
        "not supplied.",
        "no governance issue recorded.",
    }


def clean_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/").strip()


def split_values(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if not value:
        return []
    values = []
    for line in str(value).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        values.extend(part.strip() for part in stripped.split(";") if part.strip())
    return values


def first_existing_path(paths: list[Path]) -> Path | None:
    for path in paths:
        try:
            if path.expanduser().is_file():
                return path.expanduser().resolve()
        except OSError:
            continue
    return None


def resolve_source_path(reference: str | Path, private: Path, base: Path | None = None) -> Path | None:
    text = str(reference).strip()
    if not text or text.lower() in {"none", "none recorded.", "not supplied."}:
        return None
    raw = Path(text).expanduser()
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        if base is not None:
            candidates.append(base.parent / raw)
        candidates.append(ROOT / raw)
        candidates.append(private / raw)
        if text.startswith("private/"):
            candidates.append(private / text.removeprefix("private/"))
        if text.startswith("external_private_root/"):
            candidates.append(private / text.removeprefix("external_private_root/"))
    return first_existing_path(candidates)


def read_json_artifact(path: Path, artifact_type: str) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or data.get("artifact_type") != artifact_type:
        return None
    return data


def read_source_sections(path: Path) -> dict[str, str]:
    return parse_sections(path.read_text())


def assessment(rating: str, notes: str) -> dict[str, str]:
    return {"rating": rating, "notes": notes}


def path_reference(path: Path | None, fallback: str = "missing") -> str:
    return str(path) if path else fallback


def outcome_summary_text(sections: dict[str, str]) -> str:
    completion = first_line(sections.get("Completion", ""), "Unknown")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    benefit = fallback_section(sections, "Benefit")
    friction = fallback_section(sections, "Friction")
    return f"{completion}: {happened} Benefit: {benefit} Friction: {friction}"


def review_outcome_from_quality(quality: dict[str, object], decision: str) -> str:
    overall = str(quality.get("overall_assessment", "insufficient_evidence"))
    if decision == "Escalate":
        return "escalate"
    if overall == "improved_decision_quality":
        return "improve"
    if overall == "poor_fit":
        return "downgrade"
    if overall == "insufficient_evidence":
        return "quarantine"
    return "keep"


def learning_decision(sections: dict[str, str]) -> str:
    key = completion_key(sections.get("Completion", ""))
    friction = has_real_content(sections.get("Friction", ""))
    benefit = has_real_content(sections.get("Benefit", ""))
    protected = sections.get("Protected-Time Impact", "").lower()
    governance = has_real_content(sections.get("Governance Notes", ""))
    if "medium" in protected or "high" in protected or governance:
        return "Escalate"
    if key == "completed" and benefit and not friction:
        return "Repeat"
    if key == "completed" and friction:
        return "Reduce"
    if key == "partial":
        return "Split"
    if key == "blocked":
        return "Block pending dependency"
    if key == "not_completed":
        return "Reschedule with smaller scope"
    if key == "canceled":
        return "Stop or defer"
    return "Gather more information"


def queue_implication(decision: str) -> str:
    if decision == "Repeat":
        return "Add follow-up candidate if recurrence is useful."
    if decision == "Reduce":
        return "Add smaller follow-up candidate."
    if decision == "Split":
        return "Split into smaller directive candidates."
    if decision == "Block pending dependency":
        return "Move candidate to blocked until dependency changes."
    if decision == "Reschedule with smaller scope":
        return "Defer original and add a smaller replacement candidate."
    if decision == "Stop or defer":
        return "Remove or defer until strategy changes."
    if decision == "Escalate":
        return "Escalate to governance review before repetition."
    return "Ask targeted question before queue synthesis."


def context_recommendation(decision: str, sections: dict[str, str]) -> str:
    friction = has_real_content(sections.get("Friction", ""))
    benefit = has_real_content(sections.get("Benefit", ""))
    if decision == "Repeat" and benefit:
        return "Record provisional pattern if repeated once more."
    if decision in {"Reduce", "Split", "Reschedule with smaller scope"} and friction:
        return "Record provisional execution-friction pattern."
    if decision == "Block pending dependency":
        return "Update operating register with blocker or dependency."
    if decision == "Escalate":
        return "Governance review before durable context change."
    return "No durable update yet."


def agent_routing(sections: dict[str, str]) -> str:
    explicit = sections.get("Agent Updates", "")
    if has_real_content(explicit) and "should ingest" not in explicit.lower():
        return explicit
    directive = sections.get("Directive Summary", "").lower()
    routes = ["Operations"]
    domain_keywords = [
        ("breakfast", "Health"),
        ("walk", "Health"),
        ("exercise", "Health"),
        ("garden", "Home and Environment"),
        ("weed", "Home and Environment"),
        ("yard", "Home and Environment"),
        ("venture", "Venture"),
        ("business", "Venture"),
        ("finance", "Finance"),
        ("money", "Finance"),
        ("spouse", "Relationships"),
        ("partner", "Relationships"),
    ]
    for keyword, route in domain_keywords:
        if keyword in directive and route not in routes:
            routes.append(route)
    return ", ".join(routes)


def governance_status(sections: dict[str, str]) -> str:
    protected = first_line(sections.get("Protected-Time Impact", "None"), "None")
    stakeholder = sections.get("Stakeholder Impact", "")
    governance = sections.get("Governance Notes", "")
    if protected in {"Medium", "High"} or has_real_content(stakeholder) or has_real_content(governance):
        return "Needs governance review before repetition or authority increase."
    return "Level 1 learning review; no authority increase approved."


def dimension(rating: str, evidence: str, implication: str) -> dict[str, str]:
    return {
        "rating": rating,
        "evidence": evidence,
        "implication": implication,
    }


def fallback_section(sections: dict[str, str], name: str, fallback: str = "None recorded.") -> str:
    return sections.get(name, fallback) or fallback


def read_council_decision(path: Path) -> dict[str, Any]:
    data = read_json_artifact(path, "council_decision")
    if data is not None:
        return {
            "source": str(path),
            "source_recommendations": split_values(data.get("source_recommendations", [])),
            "decision_frame": str(data.get("decision_frame", "Unknown decision frame")),
            "council_outcome": str(data.get("council_outcome", "adopt")),
            "proposed_directive": str(data.get("proposed_directive", "Unknown directive")),
            "deferrals": split_values(data.get("deferrals", [])),
            "dissent": split_values(data.get("dissent", [])),
            "evidence_gaps": split_values(data.get("evidence_gaps", [])),
            "vetoes": split_values(data.get("vetoes", [])),
            "governance_status": str(data.get("governance_status", "")),
        }

    sections = read_source_sections(path)
    return {
        "source": str(path),
        "source_recommendations": split_values(sections.get("Source Recommendations", "")),
        "decision_frame": first_line(sections.get("Decision Frame", ""), "Unknown decision frame"),
        "council_outcome": first_line(sections.get("Council Outcome", ""), "Adopt").lower().replace(" ", "_"),
        "proposed_directive": first_line(sections.get("Proposed Directive", ""), "Unknown directive"),
        "deferrals": split_values(sections.get("Deferrals", "")),
        "dissent": split_values(sections.get("Dissent", "")),
        "evidence_gaps": split_values(sections.get("Evidence Gaps", "")),
        "vetoes": split_values(sections.get("Vetoes", "")),
        "governance_status": first_line(sections.get("Governance Status", ""), ""),
    }


def council_synthesis_review(
    *,
    council_path: Path | None,
    council: dict[str, Any] | None,
    sections: dict[str, str],
    review_date: str,
    outcome_path: Path,
    quality: dict[str, object],
    decision: str,
) -> dict[str, object] | None:
    if council_path is None:
        return None
    if council is None:
        return {
            "artifact_type": "council_synthesis_review",
            "schema_version": 1,
            "date": review_date,
            "source_council_decision": str(council_path),
            "source_recommendations": [],
            "related_outcome": str(outcome_path),
            "decision_frame": "Unknown; source council decision could not be read.",
            "selected_outcome": "block",
            "selected_directive_or_question": first_line(sections.get("Directive Summary", ""), "Unknown directive"),
            "deferrals": [],
            "outcome_summary": outcome_summary_text(sections),
            "selection_quality": MISSING_ASSESSMENT,
            "dissent_handling": MISSING_ASSESSMENT,
            "information_timing": MISSING_ASSESSMENT,
            "human_burden": MISSING_ASSESSMENT,
            "governance_fit": MISSING_ASSESSMENT,
            "review_outcome": "quarantine",
            "future_adjustment": "Do not update council weighting until the source decision can be reviewed.",
            "durable_memory_candidate": "Record missing-source hygiene issue if repeated.",
            "next_review": "After source council decision is available.",
        }

    key = completion_key(sections.get("Completion", ""))
    friction = has_real_content(sections.get("Friction", ""))
    cost = has_real_content(sections.get("Cost", ""))
    governance = governance_status(sections)
    selected_outcome = str(council.get("council_outcome", "adopt"))
    if selected_outcome not in {"adopt", "revise", "request_more_information", "escalate", "block"}:
        selected_outcome = "adopt"
    source_recommendations = split_values(council.get("source_recommendations", []))
    dissent = split_values(council.get("dissent", []))
    evidence_gaps = split_values(council.get("evidence_gaps", []))
    vetoes = split_values(council.get("vetoes", []))
    overall = str(quality.get("overall_assessment", "insufficient_evidence"))

    selection_rating = "strong" if overall == "improved_decision_quality" else "weak" if overall == "poor_fit" else "adequate"
    dissent_rating = "strong" if dissent or evidence_gaps or vetoes else "not_applicable"
    if overall == "poor_fit" and not dissent and not evidence_gaps:
        dissent_rating = "weak"
    information_rating = "adequate"
    if selected_outcome == "request_more_information":
        information_rating = "strong" if key not in {"blocked", "not_completed"} else "weak"
    elif evidence_gaps and key in {"blocked", "not_completed"}:
        information_rating = "weak"
    burden_rating = "strong" if not friction and not cost else "adequate" if friction and not cost else "weak"
    governance_rating = "strong" if "Needs governance review" not in governance else "weak"

    return {
        "artifact_type": "council_synthesis_review",
        "schema_version": 1,
        "date": review_date,
        "source_council_decision": str(council_path),
        "source_recommendations": source_recommendations,
        "related_outcome": str(outcome_path),
        "decision_frame": str(council.get("decision_frame", "Unknown decision frame")),
        "selected_outcome": selected_outcome,
        "selected_directive_or_question": str(council.get("proposed_directive", "")) or first_line(
            sections.get("Directive Summary", ""),
            "Unknown directive",
        ),
        "deferrals": split_values(council.get("deferrals", [])),
        "outcome_summary": outcome_summary_text(sections),
        "selection_quality": assessment(
            selection_rating,
            f"Decision quality assessment: {overall}. Completion: {first_line(sections.get('Completion', ''), 'Unknown')}.",
        ),
        "dissent_handling": assessment(
            dissent_rating,
            f"Dissent items: {len(dissent)}. Evidence gaps: {len(evidence_gaps)}. Vetoes: {len(vetoes)}.",
        ),
        "information_timing": assessment(
            information_rating,
            f"Council outcome: {selected_outcome}. Evidence gaps preserved: {len(evidence_gaps)}.",
        ),
        "human_burden": assessment(
            burden_rating,
            f"Friction: {fallback_section(sections, 'Friction')} Cost: {fallback_section(sections, 'Cost')}",
        ),
        "governance_fit": assessment(governance_rating, governance),
        "review_outcome": review_outcome_from_quality(quality, decision),
        "future_adjustment": str(quality.get("next_architecture_adjustment", "")),
        "durable_memory_candidate": (
            "Preserve council weighting note if this pattern repeats."
            if overall != "insufficient_evidence"
            else "No durable council update until more evidence exists."
        ),
        "next_review": first_line(sections.get("Next Review", ""), "Next weekly review."),
    }


def read_agent_recommendation(path: Path) -> dict[str, Any]:
    data = read_json_artifact(path, "agent_recommendation")
    if data is not None:
        return {
            "source": str(path),
            "agent": str(data.get("agent", "Unknown Agent")),
            "recommendation_type": str(data.get("recommendation_type", "recommend")),
            "proposed_directive": str(data.get("proposed_directive", "")),
            "expected_benefit": str(data.get("expected_benefit", "")),
            "costs_and_tradeoffs": split_values(data.get("costs_and_tradeoffs", [])),
            "risks": split_values(data.get("risks", [])),
            "evidence_quality": split_values(data.get("evidence_quality", [])),
            "dissent": str(data.get("dissent", "")),
        }

    sections = read_source_sections(path)
    return {
        "source": str(path),
        "agent": first_line(sections.get("Agent", ""), "Unknown Agent"),
        "recommendation_type": first_line(sections.get("Recommendation Type", ""), "Recommend").lower().replace(" ", "_"),
        "proposed_directive": first_line(sections.get("Proposed Directive", ""), ""),
        "expected_benefit": first_line(sections.get("Expected Benefit", ""), ""),
        "costs_and_tradeoffs": split_values(sections.get("Costs and Tradeoffs", "")),
        "risks": split_values(sections.get("Risks", "")),
        "evidence_quality": split_values(sections.get("Evidence Quality", "")),
        "dissent": sections.get("Dissent", ""),
    }


def token_overlap(left: str, right: str) -> bool:
    left_tokens = {token for token in re.findall(r"[a-z0-9]+", left.lower()) if len(token) > 3}
    right_tokens = {token for token in re.findall(r"[a-z0-9]+", right.lower()) if len(token) > 3}
    return bool(left_tokens.intersection(right_tokens))


def stress_impact(sections: dict[str, str]) -> str:
    contentment = first_line(sections.get("Contentment Signal", ""), "Unknown")
    cost = sections.get("Cost", "")
    friction = sections.get("Friction", "")
    if contentment == "More contentment":
        return "reduced"
    if contentment == "Less contentment" or "stress" in cost.lower() or "stress" in friction.lower():
        return "increased"
    if contentment == "No material change":
        return "preserved"
    return "unknown"


def agent_recommendation_review(
    *,
    recommendation_path: Path | None,
    recommendation: dict[str, Any] | None,
    council_path: Path | None,
    sections: dict[str, str],
    review_date: str,
    outcome_path: Path,
) -> dict[str, object]:
    if recommendation_path is None or recommendation is None:
        return {
            "artifact_type": "agent_recommendation_review",
            "schema_version": 1,
            "date": review_date,
            "reviewed_agent": "Unknown Agent",
            "source_recommendation": path_reference(recommendation_path),
            "related_council_decision": path_reference(council_path, ""),
            "related_directive_outcome": str(outcome_path),
            "recommendation_summary": "Source recommendation could not be read.",
            "outcome_summary": outcome_summary_text(sections),
            "fit_assessment": MISSING_ASSESSMENT,
            "friction_prediction": MISSING_ASSESSMENT,
            "information_request_quality": MISSING_ASSESSMENT,
            "stress_impact": "unknown",
            "evidence_quality_review": MISSING_ASSESSMENT,
            "dissent_quality": MISSING_ASSESSMENT,
            "review_outcome": "quarantine",
            "future_adjustment": "Do not update agent weighting until the source recommendation is available.",
            "durable_memory_candidate": "Record missing-source hygiene issue if repeated.",
            "next_review": "After source recommendation is available.",
        }

    key = completion_key(sections.get("Completion", ""))
    friction = fallback_section(sections, "Friction")
    benefit = fallback_section(sections, "Benefit")
    outcome_progress = fallback_section(sections, "Outcome Progress")
    expected_benefit = str(recommendation.get("expected_benefit", ""))
    predicted_friction = " ".join(split_values(recommendation.get("costs_and_tradeoffs", [])))
    evidence_quality = split_values(recommendation.get("evidence_quality", []))
    risks = split_values(recommendation.get("risks", []))
    recommendation_type = str(recommendation.get("recommendation_type", "recommend"))
    stress = stress_impact(sections)

    completed = key == "completed"
    actual_friction = has_real_content(friction)
    benefit_visible = has_real_content(benefit) or has_real_content(outcome_progress)
    fit_rating = "strong" if completed and benefit_visible and not actual_friction else "adequate" if completed or benefit_visible else "weak"
    if key in {"blocked", "not_completed"}:
        fit_rating = "weak"
    friction_rating = "not_applicable"
    if actual_friction:
        friction_rating = "strong" if token_overlap(predicted_friction, friction) else "weak"
    elif predicted_friction:
        friction_rating = "adequate"
    info_rating = "not_applicable"
    if recommendation_type == "request_more_information":
        info_rating = "adequate" if key != "unknown" else "missing"
    evidence_rating = "strong" if benefit_visible and "speculation" not in evidence_quality else "weak" if "speculation" in evidence_quality and fit_rating == "weak" else "adequate"
    dissent = str(recommendation.get("dissent", ""))
    dissent_rating = "adequate" if has_real_content(dissent) else "not_applicable"
    if has_real_content(dissent) and fit_rating == "weak":
        dissent_rating = "strong"

    if fit_rating == "strong" and evidence_rating in {"strong", "adequate"} and stress != "increased":
        review_outcome = "improve"
    elif fit_rating == "weak" or friction_rating == "weak" or stress == "increased":
        review_outcome = "downgrade"
    elif evidence_rating == "weak":
        review_outcome = "downgrade"
    else:
        review_outcome = "keep"

    future_adjustment = "Keep this recommendation pattern available for similar contexts."
    if friction_rating == "weak":
        future_adjustment = "Lower confidence until this agent predicts execution friction more explicitly."
    elif evidence_rating == "weak":
        future_adjustment = "Require stronger evidence before this agent's similar recommendation is weighted heavily."
    elif stress == "increased":
        future_adjustment = "Reduce stress load or scope before adopting similar recommendations."

    return {
        "artifact_type": "agent_recommendation_review",
        "schema_version": 1,
        "date": review_date,
        "reviewed_agent": str(recommendation.get("agent", "Unknown Agent")),
        "source_recommendation": str(recommendation_path),
        "related_council_decision": path_reference(council_path, ""),
        "related_directive_outcome": str(outcome_path),
        "recommendation_summary": str(recommendation.get("proposed_directive", "")) or "No proposed directive recorded.",
        "outcome_summary": outcome_summary_text(sections),
        "fit_assessment": assessment(
            fit_rating,
            f"Expected benefit: {expected_benefit or 'not recorded'}. Actual benefit: {benefit}.",
        ),
        "friction_prediction": assessment(
            friction_rating,
            f"Predicted friction: {predicted_friction or 'none recorded'}. Actual friction: {friction}.",
        ),
        "information_request_quality": assessment(
            info_rating,
            f"Recommendation type: {recommendation_type}.",
        ),
        "stress_impact": stress,
        "evidence_quality_review": assessment(
            evidence_rating,
            "Evidence quality recorded: " + (", ".join(evidence_quality) or "none recorded"),
        ),
        "dissent_quality": assessment(
            dissent_rating,
            dissent or "No dissent recorded.",
        ),
        "review_outcome": review_outcome,
        "future_adjustment": future_adjustment,
        "durable_memory_candidate": (
            f"{recommendation.get('agent', 'Unknown Agent')}: {future_adjustment}"
            if review_outcome in {"improve", "downgrade"}
            else "No durable calibration memory from one routine outcome."
        ),
        "next_review": first_line(sections.get("Next Review", ""), "Next weekly review."),
    }


def missed_risks_from_review(review: dict[str, object]) -> list[str]:
    missed = []
    fit = review.get("fit_assessment", {})
    friction = review.get("friction_prediction", {})
    if isinstance(friction, dict) and friction.get("rating") == "weak":
        missed.append("friction")
    if review.get("stress_impact") == "increased":
        missed.append("stress")
    if isinstance(fit, dict) and fit.get("rating") == "weak":
        missed.append("fit")
    return missed


def calibration_record_from_agent_review(
    agent_review: dict[str, object],
    review_date: str,
) -> dict[str, object]:
    reviewed_agent = str(agent_review["reviewed_agent"])
    outcome = str(agent_review["review_outcome"])
    fit = agent_review.get("fit_assessment", {})
    friction = agent_review.get("friction_prediction", {})
    evidence = agent_review.get("evidence_quality_review", {})
    missed_risks = missed_risks_from_review(agent_review)
    score_delta = 1 if outcome == "improve" else -1 if outcome == "downgrade" else -2 if outcome in {"quarantine", "escalate"} else 0
    action = {
        "improve": "increase_weight",
        "keep": "keep_weight",
        "downgrade": "decrease_weight",
        "quarantine": "quarantine",
        "escalate": "escalate",
    }.get(outcome, "keep_weight")
    cautions = []
    if isinstance(friction, dict) and friction.get("rating") == "weak":
        cautions.append("Missed execution friction; require explicit friction prediction before high weighting.")
    if isinstance(evidence, dict) and evidence.get("rating") == "weak":
        cautions.append("Evidence quality was weak or overstated.")
    if agent_review.get("stress_impact") == "increased":
        cautions.append("Recommendation increased stress or decision burden.")
    if not cautions:
        cautions.append("No caution from this single outcome; keep evidence provisional.")
    council_summary = (
        f"{reviewed_agent}: outcome {outcome}; "
        f"fit={fit.get('rating', 'unknown') if isinstance(fit, dict) else 'unknown'}; "
        f"friction={friction.get('rating', 'unknown') if isinstance(friction, dict) else 'unknown'}."
    )
    return {
        "artifact_type": "agent_calibration_record",
        "schema_version": 1,
        "date": review_date,
        "agent": reviewed_agent,
        "source_reviews": [str(agent_review.get("source_recommendation", "")), str(agent_review.get("related_directive_outcome", ""))],
        "recommendation_usefulness": fit.get("rating", "unknown") if isinstance(fit, dict) else "unknown",
        "score_delta": score_delta,
        "calibration_action": action,
        "friction_prediction": friction.get("rating", "unknown") if isinstance(friction, dict) else "unknown",
        "evidence_quality": evidence.get("rating", "unknown") if isinstance(evidence, dict) else "unknown",
        "stress_impact": str(agent_review.get("stress_impact", "unknown")),
        "missed_risks": missed_risks,
        "cautions": cautions,
        "council_summary": council_summary,
        "future_weighting_note": str(agent_review.get("future_adjustment", "")),
        "next_review": str(agent_review.get("next_review", "Next weekly review.")),
    }


def baseline_comparison(sections: dict[str, str]) -> str:
    governance = sections.get("Governance Notes", "").lower()
    evidence = sections.get("Evidence", "").lower()
    if "goal reconciliation" in governance or "goal reconciliation" in evidence:
        return "council_with_goal_reconciliation"
    if "council" in governance or "council" in evidence:
        return "council_without_goal_reconciliation"
    return "unknown"


def decision_quality_review(
    outcome_path: Path,
    review_date: str,
    sections: dict[str, str],
    decision: str,
    directive: str,
    completion: str,
) -> dict[str, object]:
    key = completion_key(completion)
    friction = has_real_content(sections.get("Friction", ""))
    benefit = has_real_content(sections.get("Benefit", ""))
    outcome_progress = has_real_content(sections.get("Outcome Progress", ""))
    contentment = sections.get("Contentment Signal", "Unknown")
    cost = has_real_content(sections.get("Cost", ""))
    governance = governance_status(sections)
    protected = first_line(sections.get("Protected-Time Impact", "None"), "None")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    evidence = first_line(sections.get("Evidence", ""), "Human report.")

    completed = key == "completed"
    partial_or_blocked = key in {"partial", "blocked", "not_completed"}
    escalated = decision == "Escalate"
    low_governance_concern = "Needs governance review" not in governance
    useful_outcome_evidence = benefit or outcome_progress

    dimensions = {
        "actionability": dimension(
            "strong" if completed else "adequate" if key == "partial" else "weak",
            f"Completion class: {completion}.",
            "Directive was executable as written."
            if completed
            else "Directive size, timing, or dependency should be revised.",
        ),
        "goal_fit": dimension(
            "strong" if useful_outcome_evidence else "unknown",
            (
                f"Benefit: {fallback_section(sections, 'Benefit')} "
                f"Outcome progress: {fallback_section(sections, 'Outcome Progress')}"
            ),
            "Benefit or outcome progress was visible enough to preserve the pattern."
            if useful_outcome_evidence
            else "Outcome did not prove goal fit; ask or inspect next evidence.",
        ),
        "constraint_fit": dimension(
            "strong" if low_governance_concern else "weak",
            governance,
            "Constraints fit the directive."
            if low_governance_concern
            else "Governance or protected-time constraints should dominate future synthesis.",
        ),
        "burden": dimension(
            "strong" if not cost and not friction else "adequate" if friction and not cost else "weak",
            f"Friction: {fallback_section(sections, 'Friction')} Cost: {fallback_section(sections, 'Cost')}",
            "Human burden appears acceptable."
            if not cost
            else "Reduce question load, scope, timing, or emotional cost.",
        ),
        "timeliness": dimension(
            "adequate" if key != "unknown" else "unknown",
            happened,
            "Timing produced reviewable evidence." if key != "unknown" else "Timing quality is unclear.",
        ),
        "risk_control": dimension(
            "strong" if low_governance_concern else "weak",
            f"Protected-time impact: {protected}. {governance}",
            "Risk controls were sufficient for repetition."
            if low_governance_concern
            else "Escalate or lower authority before repetition.",
        ),
        "explanation_quality": dimension(
            "unknown",
            "Directive outcome does not yet capture whether the reason helped.",
            "Add lightweight outcome prompt when explanation quality would change future directives.",
        ),
        "follow_through_probability": dimension(
            "strong" if completed and not friction else "adequate" if completed else "weak" if partial_or_blocked else "unknown",
            f"Completion: {completion}. Friction: {fallback_section(sections, 'Friction')}",
            "Similar directives are likely viable."
            if completed and not friction
            else "Future directives should reduce friction or change conditions.",
        ),
        "outcome_quality": dimension(
            "strong"
            if completed and useful_outcome_evidence and not escalated
            else "adequate"
            if completed or useful_outcome_evidence
            else "weak"
            if partial_or_blocked
            else "unknown",
            (
                f"Benefit: {fallback_section(sections, 'Benefit')} "
                f"Outcome progress: {fallback_section(sections, 'Outcome Progress')} "
                f"Contentment signal: {contentment}."
            ),
            "Decision produced useful outcome evidence."
            if completed or useful_outcome_evidence
            else "Decision did not yet produce enough progress.",
        ),
        "learning_value": dimension(
            "strong" if friction or useful_outcome_evidence or escalated else "adequate",
            f"Evidence: {evidence}",
            "Outcome should update agent recommendations or synthesis."
            if friction or useful_outcome_evidence or escalated
            else "Preserve as light evidence only.",
        ),
    }

    weak_count = sum(1 for item in dimensions.values() if item["rating"] == "weak")
    strong_count = sum(1 for item in dimensions.values() if item["rating"] == "strong")
    if weak_count >= 3 or escalated:
        overall = "poor_fit" if weak_count >= 3 else "mixed"
    elif strong_count >= 4 and completed:
        overall = "improved_decision_quality"
    elif key == "unknown":
        overall = "insufficient_evidence"
    else:
        overall = "mixed"

    if overall == "improved_decision_quality":
        adjustment = "Preserve the directive pattern and compare future repetitions against this outcome."
    elif escalated:
        adjustment = "Route future similar directives through governance before adoption."
    elif friction:
        adjustment = "Reduce scope, alter conditions, or ask the one missing fact that would remove friction."
    else:
        adjustment = "Collect better evidence on explanation quality, goal fit, and user burden before changing architecture."

    return {
        "artifact_type": "decision_quality_review",
        "schema_version": 1,
        "date": review_date,
        "source_outcome": str(outcome_path),
        "directive": directive,
        "completion_class": completion,
        "baseline_comparison": baseline_comparison(sections),
        "dimensions": dimensions,
        "human_burden": {
            "questions_asked": 0,
            "answer_burden": "unknown",
            "burden_notes": "Outcome capture does not yet track question count or answer burden directly.",
        },
        "overall_assessment": overall,
        "next_architecture_adjustment": adjustment,
        "review_notes": f"Decision quality inferred from outcome evidence. What happened: {happened}",
    }


def decision_quality_rows(review: dict[str, object]) -> list[str]:
    dimensions = review.get("dimensions", {})
    if not isinstance(dimensions, dict):
        return ["| Unknown | Unknown | No dimensions recorded. | No implication recorded. |"]
    rows = []
    for name, value in dimensions.items():
        if not isinstance(value, dict):
            continue
        label = name.replace("_", " ").title()
        rows.append(
            f"| {label} | {value.get('rating', 'unknown')} | {value.get('evidence', '')} | {value.get('implication', '')} |"
        )
    return rows or ["| Unknown | Unknown | No dimensions recorded. | No implication recorded. |"]


def unique_paths(values: list[object]) -> list[object]:
    seen = set()
    output = []
    for value in values:
        key = str(value)
        if key and key not in seen:
            output.append(value)
            seen.add(key)
    return output


def resolve_requested_path(path: Path, private: Path, base: Path | None = None) -> tuple[Path, bool]:
    resolved = resolve_source_path(path, private, base)
    if resolved is not None:
        return resolved, True
    return path, path.is_file()


def build_review_artifact(
    outcome_path: Path,
    review_date: str,
    private: Path | None = None,
    council_decision: Path | None = None,
    recommendations: list[Path] | None = None,
) -> dict[str, object]:
    private_root = private or private_root_config.resolve_private_root(None)
    sections = read_outcome_sections(outcome_path)
    directive = first_line(sections.get("Directive Summary", ""), outcome_path.stem)
    completion = first_line(sections.get("Completion", ""), "Unknown")
    decision = learning_decision(sections)
    evidence = first_line(sections.get("Evidence", ""), "Human report.")
    happened = first_line(sections.get("What Happened", ""), "Not supplied.")
    quality = decision_quality_review(
        outcome_path,
        review_date,
        sections,
        decision,
        directive,
        completion,
    )
    council_path: Path | None = None
    council: dict[str, Any] | None = None
    if council_decision is not None:
        council_path, council_exists = resolve_requested_path(council_decision, private_root, outcome_path)
        if council_exists:
            council = read_council_decision(council_path)
    council_review = council_synthesis_review(
        council_path=council_path,
        council=council,
        sections=sections,
        review_date=review_date,
        outcome_path=outcome_path,
        quality=quality,
        decision=decision,
    )

    recommendation_refs: list[object] = list(recommendations or [])
    if council:
        recommendation_refs.extend(split_values(council.get("source_recommendations", [])))
    agent_reviews: list[dict[str, object]] = []
    for reference in unique_paths(recommendation_refs):
        resolved = resolve_source_path(reference, private_root, council_path or outcome_path)
        if resolved is None:
            missing_path = Path(str(reference))
            agent_reviews.append(
                agent_recommendation_review(
                    recommendation_path=missing_path,
                    recommendation=None,
                    council_path=council_path,
                    sections=sections,
                    review_date=review_date,
                    outcome_path=outcome_path,
                )
            )
            continue
        agent_reviews.append(
            agent_recommendation_review(
                recommendation_path=resolved,
                recommendation=read_agent_recommendation(resolved),
                council_path=council_path,
                sections=sections,
                review_date=review_date,
                outcome_path=outcome_path,
            )
        )
    calibration_records = [
        calibration_record_from_agent_review(agent_review, review_date)
        for agent_review in agent_reviews
    ]
    return {
        "artifact_type": "outcome_review",
        "schema_version": 1,
        "date": review_date,
        "source_outcome": str(outcome_path),
        "directive": directive,
        "completion_class": completion,
        "evidence_summary": f"{happened} Evidence: {evidence}",
        "friction_summary": sections.get("Friction", "None recorded.") or "None recorded.",
        "benefit_summary": sections.get("Benefit", "None recorded.") or "None recorded.",
        "outcome_progress": sections.get("Outcome Progress", "None recorded.") or "None recorded.",
        "contentment_signal": first_line(sections.get("Contentment Signal", ""), "Unknown"),
        "cost_summary": sections.get("Cost", "None recorded.") or "None recorded.",
        "learning_decision": decision,
        "queue_implication": queue_implication(decision),
        "context_update_recommendation": context_recommendation(decision, sections),
        "agent_routing": agent_routing(sections),
        "governance_status": governance_status(sections),
        "decision_quality_review": quality,
        "council_synthesis_review": council_review,
        "agent_recommendation_reviews": agent_reviews,
        "agent_calibration_records": calibration_records,
        "next_review": first_line(sections.get("Next Review", ""), "Next weekly review."),
    }


def assessment_rows(review: object, fields: list[tuple[str, str]]) -> list[str]:
    if not isinstance(review, dict):
        return ["| None | n/a | n/a |"]
    rows = []
    for label, key in fields:
        value = review.get(key, {})
        if isinstance(value, dict):
            rows.append(f"| {label} | {value.get('rating', 'unknown')} | {value.get('notes', '')} |")
    return rows or ["| None | n/a | n/a |"]


def agent_review_rows(reviews: object) -> list[str]:
    items = reviews if isinstance(reviews, list) else []
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        fit = item.get("fit_assessment", {})
        friction = item.get("friction_prediction", {})
        evidence = item.get("evidence_quality_review", {})
        rows.append(
            "| {agent} | {outcome} | {fit} | {friction} | {evidence} | {stress} |".format(
                agent=clean_cell(item.get("reviewed_agent", "Unknown")),
                outcome=clean_cell(item.get("review_outcome", "unknown")),
                fit=clean_cell(fit.get("rating", "unknown") if isinstance(fit, dict) else "unknown"),
                friction=clean_cell(friction.get("rating", "unknown") if isinstance(friction, dict) else "unknown"),
                evidence=clean_cell(evidence.get("rating", "unknown") if isinstance(evidence, dict) else "unknown"),
                stress=clean_cell(item.get("stress_impact", "unknown")),
            )
        )
    return rows or ["| None | n/a | n/a | n/a | n/a | n/a |"]


def calibration_rows(records: object) -> list[str]:
    items = records if isinstance(records, list) else []
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        rows.append(
            "| {agent} | {delta} | {action} | {summary} |".format(
                agent=clean_cell(item.get("agent", "Unknown")),
                delta=clean_cell(item.get("score_delta", 0)),
                action=clean_cell(item.get("calibration_action", "keep_weight")),
                summary=clean_cell(item.get("council_summary", "")),
            )
        )
    return rows or ["| None | n/a | n/a | n/a |"]


def build_review(
    outcome_path: Path,
    review_date: str,
    private: Path | None = None,
    council_decision: Path | None = None,
    recommendations: list[Path] | None = None,
) -> str:
    artifact = build_review_artifact(
        outcome_path,
        review_date,
        private=private,
        council_decision=council_decision,
        recommendations=recommendations,
    )
    council_review = artifact.get("council_synthesis_review")
    return "\n".join(
        [
            f"# Outcome Review: {review_date} - {artifact['directive']}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Source Outcome",
            "",
            str(artifact["source_outcome"]),
            "",
            "## Directive",
            "",
            str(artifact["directive"]),
            "",
            "## Completion Class",
            "",
            str(artifact["completion_class"]),
            "",
            "## Evidence Summary",
            "",
            str(artifact["evidence_summary"]),
            "",
            "## Friction Summary",
            "",
            str(artifact["friction_summary"]),
            "",
            "## Benefit Summary",
            "",
            str(artifact["benefit_summary"]),
            "",
            "## Outcome Progress",
            "",
            str(artifact["outcome_progress"]),
            "",
            "## Contentment Signal",
            "",
            str(artifact["contentment_signal"]),
            "",
            "## Cost Summary",
            "",
            str(artifact["cost_summary"]),
            "",
            "## Learning Decision",
            "",
            str(artifact["learning_decision"]),
            "",
            "## Queue Implication",
            "",
            str(artifact["queue_implication"]),
            "",
            "## Context Update Recommendation",
            "",
            str(artifact["context_update_recommendation"]),
            "",
            "## Agent Routing",
            "",
            str(artifact["agent_routing"]),
            "",
            "## Governance Status",
            "",
            str(artifact["governance_status"]),
            "",
            "## Decision Quality Review",
            "",
            "Baseline comparison: "
            + str(artifact["decision_quality_review"]["baseline_comparison"]),
            "",
            "| Dimension | Rating | Evidence | Implication |",
            "| --- | --- | --- | --- |",
            *decision_quality_rows(artifact["decision_quality_review"]),
            "",
            "## Human Burden",
            "",
            (
                f"Questions asked: {artifact['decision_quality_review']['human_burden']['questions_asked']}. "
                f"Answer burden: {artifact['decision_quality_review']['human_burden']['answer_burden']}. "
                f"{artifact['decision_quality_review']['human_burden']['burden_notes']}"
            ),
            "",
            "## Decision Quality Assessment",
            "",
            str(artifact["decision_quality_review"]["overall_assessment"]),
            "",
            "## Next Architecture Adjustment",
            "",
            str(artifact["decision_quality_review"]["next_architecture_adjustment"]),
            "",
            "## Decision Quality Notes",
            "",
            str(artifact["decision_quality_review"]["review_notes"]),
            "",
            "## Council Synthesis Review",
            "",
            "Source: "
            + (
                str(council_review.get("source_council_decision", "None"))
                if isinstance(council_review, dict)
                else "None supplied."
            ),
            "",
            "| Dimension | Rating | Notes |",
            "| --- | --- | --- |",
            *assessment_rows(
                council_review,
                [
                    ("Selection Quality", "selection_quality"),
                    ("Dissent Handling", "dissent_handling"),
                    ("Information Timing", "information_timing"),
                    ("Human Burden", "human_burden"),
                    ("Governance Fit", "governance_fit"),
                ],
            ),
            "",
            "## Agent Recommendation Reviews",
            "",
            "| Agent | Review Outcome | Fit | Friction Prediction | Evidence Quality | Stress Impact |",
            "| --- | --- | --- | --- | --- | --- |",
            *agent_review_rows(artifact["agent_recommendation_reviews"]),
            "",
            "## Agent Calibration Records",
            "",
            "| Agent | Score Delta | Action | Council Summary |",
            "| --- | --- | --- | --- |",
            *calibration_rows(artifact["agent_calibration_records"]),
            "",
            "## Next Review",
            "",
            str(artifact["next_review"]),
            "",
        ]
    )


def calibration_markdown(record: dict[str, object]) -> str:
    def bullets(values: object) -> list[str]:
        items = values if isinstance(values, list) else []
        return [f"- {item}" for item in items] or ["- None."]

    return "\n".join(
        [
            f"# Agent Calibration Record: {record['agent']}",
            "",
            "## Date",
            "",
            str(record["date"]),
            "",
            "## Agent",
            "",
            str(record["agent"]),
            "",
            "## Source Reviews",
            "",
            *bullets(record["source_reviews"]),
            "",
            "## Recommendation Usefulness",
            "",
            str(record["recommendation_usefulness"]),
            "",
            "## Score Delta",
            "",
            str(record["score_delta"]),
            "",
            "## Calibration Action",
            "",
            str(record["calibration_action"]),
            "",
            "## Friction Prediction",
            "",
            str(record["friction_prediction"]),
            "",
            "## Evidence Quality",
            "",
            str(record["evidence_quality"]),
            "",
            "## Stress Impact",
            "",
            str(record["stress_impact"]),
            "",
            "## Missed Risks",
            "",
            *bullets(record["missed_risks"]),
            "",
            "## Cautions",
            "",
            *bullets(record["cautions"]),
            "",
            "## Council Summary",
            "",
            str(record["council_summary"]),
            "",
            "## Future Weighting Note",
            "",
            str(record["future_weighting_note"]),
            "",
            "## Next Review",
            "",
            str(record["next_review"]),
            "",
        ]
    )


def write_calibration_records(
    records: list[dict[str, object]],
    output_dir: Path,
    force: bool,
) -> list[Path]:
    written: list[Path] = []
    for record in records:
        slug = slugify(f"{record['date']}-{record['agent']}")
        json_path = output_dir / f"{slug}.json"
        markdown_path = output_dir / f"{slug}.md"
        write_output(
            json_path,
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            force,
        )
        write_output(markdown_path, calibration_markdown(record), force)
        written.extend([markdown_path, json_path])
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--outcome", type=Path, required=True)
    parser.add_argument("--council-decision", type=Path)
    parser.add_argument("--recommendation", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--write-calibration", action="store_true")
    parser.add_argument("--calibration-dir", type=Path)
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
    if not args.outcome.is_file():
        raise SystemExit(f"missing outcome file: {args.outcome}")
    output = args.output or (
        private / "reviews" / "outcomes" / f"{args.date}-{slugify(args.outcome.stem)}.md"
    )
    write_output(
        output,
        build_review(
            args.outcome,
            args.date,
            private=private,
            council_decision=args.council_decision,
            recommendations=args.recommendation,
        ),
        args.force,
    )
    artifact: dict[str, object] | None = None
    if args.json_output:
        artifact = build_review_artifact(
            args.outcome,
            args.date,
            private=private,
            council_decision=args.council_decision,
            recommendations=args.recommendation,
        )
        write_output(
            args.json_output,
            json.dumps(artifact, indent=2, sort_keys=True) + "\n",
            args.force,
        )
    if args.write_calibration or args.calibration_dir:
        if artifact is None:
            artifact = build_review_artifact(
                args.outcome,
                args.date,
                private=private,
                council_decision=args.council_decision,
                recommendations=args.recommendation,
            )
        calibration_dir = args.calibration_dir or private / "agents" / "calibration"
        records = artifact.get("agent_calibration_records", [])
        if isinstance(records, list):
            for path in write_calibration_records(records, calibration_dir, args.force):
                print(f"wrote: {path}")
    print(f"wrote: {output}")
    if args.json_output:
        print(f"wrote: {args.json_output}")
    return output


if __name__ == "__main__":
    main_with_args()
