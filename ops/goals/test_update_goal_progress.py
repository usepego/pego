#!/usr/bin/env python3
"""Smoke tests for protected goal progress generation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import update_goal_progress


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def health_activity_signal(observed_at: str = "2026-07-04T08:15:00") -> dict[str, object]:
    return {
        "artifact_type": "state_signal",
        "schema_version": 1,
        "date": observed_at[:10],
        "observed_at": observed_at,
        "source_type": "wearable_activity",
        "ingestion_mode": "import",
        "domain": "health",
        "owning_agent": "Health Agent",
        "signal_type": "activity",
        "summary": "Synthetic activity window shows the movement habit happened.",
        "measurements": [
            {
                "name": "active_minutes",
                "value": "32",
                "unit": "minutes",
                "window": "same_day",
                "directionality": "higher_is_better",
            }
        ],
        "affected_goals": ["Synthetic health consistency"],
        "evidence_strength": "direct_telemetry",
        "confidence": "high",
        "privacy_class": "sensitive_health",
        "raw_source_reference": "synthetic-wearable://activity/day",
        "raw_data_retention": "not_stored",
        "governance_notes": ["Synthetic health data; private artifact only."],
        "review_after": "2026-07-11",
        "expires_after": "2026-07-18",
    }


def finance_account_signal() -> dict[str, object]:
    return {
        "artifact_type": "state_signal",
        "schema_version": 1,
        "date": "2026-07-04",
        "observed_at": "2026-07-04T09:00:00",
        "source_type": "bank_account_activity",
        "ingestion_mode": "import",
        "domain": "finance",
        "owning_agent": "Finance Agent",
        "signal_type": "account_balance",
        "summary": "Synthetic account activity confirms the buffer measurement was refreshed.",
        "measurements": [
            {
                "name": "cash_buffer_days",
                "value": "45",
                "unit": "days",
                "window": "current_snapshot",
                "directionality": "higher_is_better",
            }
        ],
        "affected_goals": ["Synthetic runway protection"],
        "evidence_strength": "bank_account_activity",
        "confidence": "high",
        "privacy_class": "sensitive_financial",
        "raw_source_reference": "synthetic-bank://account-activity/day",
        "raw_data_retention": "not_stored",
        "governance_notes": ["Synthetic financial data; no execution authority."],
        "review_after": "2026-07-11",
        "expires_after": "2026-07-18",
    }


def read_progress(private: Path, domain: str) -> dict[str, object]:
    return json.loads((private / "goals" / "progress" / f"{domain}.json").read_text())


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in {text!r}")


def test_health_signal_derives_leading_indicator() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "private"
        signal = private / "signals" / "health-activity.json"
        write_json(signal, health_activity_signal())

        update_goal_progress.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--signal",
                str(signal),
                "--force",
            ]
        )

        structured = read_progress(private, "health")
        # T-001/R-001: each domain exposes trajectory and confidence.
        if structured["trajectory"] != "stable":
            raise AssertionError(structured)
        if structured["confidence"] != "medium":
            raise AssertionError("missing lagging evidence should cap confidence at medium")
        if structured["progress_status"] != "unknown":
            raise AssertionError("single-sided evidence should not claim on-track progress")

        # T-003/R-003: wearable activity becomes a leading indicator.
        leading = structured["leading_indicators"]
        if leading[0]["name"] != "active_minutes" or leading[0]["indicator_type"] != "leading":
            raise AssertionError(leading)
        if structured["lagging_indicators"] != []:
            raise AssertionError("health activity signal should not become lagging evidence")
        assert_contains(structured["next_measurement_need"], "lagging outcome")

        markdown = (private / "goals" / "progress" / "health.md").read_text()
        assert_contains(markdown, "Goal Progress: health")
        assert_contains(markdown, "active_minutes")


def test_finance_signal_manual_indicator_and_attribution() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "private"
        signal = private / "signals" / "finance-account.json"
        write_json(signal, finance_account_signal())

        update_goal_progress.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--signal",
                str(signal),
                "--leading-indicator",
                "name=weekly_spend_review;value=complete;unit=check;confidence=medium;updated_at=2026-07-04",
                "--directive",
                "synthetic-directive://finance/check-account-activity",
                "--force",
            ]
        )

        structured = read_progress(private, "finance")
        # T-003/R-003: bank account activity becomes lagging evidence while manual input stays leading.
        lagging = structured["lagging_indicators"]
        if lagging[0]["name"] != "cash_buffer_days" or lagging[0]["indicator_type"] != "lagging":
            raise AssertionError(lagging)
        leading = structured["leading_indicators"]
        if leading[0]["name"] != "weekly_spend_review" or leading[0]["indicator_type"] != "leading":
            raise AssertionError(leading)

        # T-001/R-001 and T-002/R-002: trajectory/status are readable and directives are attributed.
        if structured["trajectory"] != "improving":
            raise AssertionError(structured)
        if structured["progress_status"] != "on_track":
            raise AssertionError(structured)
        if "synthetic-directive://finance/check-account-activity" not in structured["directive_attribution"]:
            raise AssertionError(structured["directive_attribution"])
        if structured["confidence"] != "medium":
            raise AssertionError("manual medium-confidence indicator should lower combined confidence")
        assert_contains(" ".join(structured["governance_notes"]), "Sensitive financial")


def test_stale_signal_lowers_confidence() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "private"
        signal = private / "signals" / "stale-health-activity.json"
        write_json(signal, health_activity_signal(observed_at="2026-05-01T08:15:00"))

        update_goal_progress.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--signal",
                str(signal),
                "--stale-after-days",
                "14",
                "--force",
            ]
        )

        structured = read_progress(private, "health")
        # T-004/R-004: stale evidence lowers confidence and asks for measurement refresh.
        if structured["confidence"] != "low":
            raise AssertionError(structured)
        if structured["progress_status"] != "unknown":
            raise AssertionError(structured)
        assert_contains(structured["next_measurement_need"], "Refresh health state signals")


def main() -> None:
    test_health_signal_derives_leading_indicator()
    test_finance_signal_manual_indicator_and_attribution()
    test_stale_signal_lowers_confidence()
    print("goal progress smoke tests passed.")


if __name__ == "__main__":
    main()
