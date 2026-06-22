#!/usr/bin/env python3
"""Smoke tests for PEGO public-writing brief generation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_public_writing_brief


VOICE_MODEL = """# Voice And Taste Model

## Writing Voice

Clear, concrete, serious, with quiet humor.

## Humor

Understated.

## Intellectual Posture

Practical builder, not academic.

## Vocabulary

Use: governance, directives.

Avoid: self-help.

## Public Positioning

Attract serious technical opportunity.

## Drafting Preferences

Draft privately before publishing.
"""


EXPECTED_CANDIDATE_FIELDS = {
    "artifact_type",
    "schema_version",
    "candidate",
    "domain",
    "altitude",
    "proposed_action",
    "duration",
    "timing",
    "energy_required",
    "location_required",
    "dependencies",
    "expected_benefit",
    "consequence_of_deferral",
    "protected_time_impact",
    "authority_level",
    "governance_status",
    "conflicts",
    "stop_condition",
}


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        voice = root / "voice.md"
        brief = root / "brief.md"
        candidate = root / "candidate.md"
        candidate_json = root / "candidate.json"
        voice.write_text(VOICE_MODEL)

        generate_public_writing_brief.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--artifact",
                "PEGO introduction essay",
                "--voice-model",
                str(voice),
                "--brief-output",
                str(brief),
                "--candidate-output",
                str(candidate),
                "--json-output",
                str(candidate_json),
                "--force",
            ]
        )

        brief_text = brief.read_text()
        if "Public Writing Brief" not in brief_text:
            raise AssertionError(brief_text)
        if "self-help" not in brief_text:
            raise AssertionError("expected voice constraints in brief")

        structured = json.loads(candidate_json.read_text())
        if set(structured) != EXPECTED_CANDIDATE_FIELDS:
            raise AssertionError(structured)
        if structured["domain"] != "communications":
            raise AssertionError("expected communications domain")
        if "publishing" not in structured["conflicts"][0].lower():
            raise AssertionError("expected publishing governance conflict")

    print("public writing brief smoke tests passed.")


if __name__ == "__main__":
    main()
