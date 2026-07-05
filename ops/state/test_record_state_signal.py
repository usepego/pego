#!/usr/bin/env python3
"""Smoke tests for PEGO state signal recording."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import record_state_signal


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "private"
        output = private / "telemetry" / "signals" / "health.json"
        markdown = private / "telemetry" / "signals" / "health.md"

        record_state_signal.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--observed-at",
                "2026-07-04T08:30:00-04:00",
                "--source-type",
                "wearable_activity",
                "--ingestion-mode",
                "import",
                "--domain",
                "health",
                "--signal-type",
                "activity",
                "--summary",
                "Synthetic wearable activity summary shows a short morning walk.",
                "--measurement",
                "steps=3200,count,today,higher_is_better",
                "--affected-goal",
                "Improve repeatable movement baseline.",
                "--output",
                str(output),
                "--markdown-output",
                str(markdown),
            ]
        )

        data = json.loads(output.read_text())
        if data["artifact_type"] != "state_signal":
            raise AssertionError(data)
        if data["privacy_class"] != "sensitive_health":
            raise AssertionError("wearable activity should default to sensitive health")
        if data["evidence_strength"] != "direct_telemetry":
            raise AssertionError("wearable activity should default to direct telemetry")
        if data["owning_agent"] != "Health Agent":
            raise AssertionError("health signal should route to Health Agent")
        if "State Signal" not in markdown.read_text():
            raise AssertionError("expected markdown output")

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "private"
        output = private / "telemetry" / "signals" / "finance.json"

        record_state_signal.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--observed-at",
                "2026-07-04",
                "--source-type",
                "bank_account_activity",
                "--ingestion-mode",
                "adapter",
                "--domain",
                "finance",
                "--signal-type",
                "transaction_pattern",
                "--summary",
                "Synthetic bank activity summary shows recurring subscription drift.",
                "--measurement",
                "recurring_subscription_count=4,count,last_30_days,lower_is_better",
                "--affected-goal",
                "Protect financial downside.",
                "--raw-source-reference",
                "private/_local/finance/synthetic-bank-summary.json",
                "--raw-data-retention",
                "private_local",
                "--output",
                str(output),
            ]
        )

        data = json.loads(output.read_text())
        if data["privacy_class"] != "sensitive_financial":
            raise AssertionError("bank activity should default to sensitive financial")
        if data["evidence_strength"] != "bank_account_activity":
            raise AssertionError("bank activity should default to bank account evidence")
        if not any("does not authorize transfers" in note for note in data["governance_notes"]):
            raise AssertionError("expected finance governance warning")

    print("state signal smoke tests passed.")


if __name__ == "__main__":
    main()
