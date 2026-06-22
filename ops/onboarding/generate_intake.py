#!/usr/bin/env python3
"""Generate one protected PEGO first-run intake packet."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


@dataclass(frozen=True)
class Question:
    text: str
    why: str
    destination: str


@dataclass(frozen=True)
class Phase:
    name: str
    purpose: str
    questions: list[Question]
    avoid: list[str]
    output: str


PHASES: dict[str, Phase] = {
    "boundary": Phase(
        name="Boundary",
        purpose="Establish privacy, collaboration mode, authority level, and stop rules before collecting sensitive operating state.",
        questions=[
            Question("Which PEGO mode are we in right now: Engineering, UX, or USER?", "Prevents framework work from mixing with private operation.", "private/operator/session-start.md"),
            Question("What information should PEGO treat as especially sensitive during setup?", "Sets the first privacy constraints.", "private/constitution/constitution.md"),
            Question("What words or signals should pause PEGO immediately?", "Defines stop behavior before directives begin.", "private/constitution/constitution.md"),
        ],
        avoid=[
            "Ask for account balances before the privacy boundary is clear.",
            "Ask for health details before authority and storage are clear.",
        ],
        output="Constitution privacy and stop-rule draft.",
    ),
    "aim": Phase(
        name="Aim",
        purpose="Capture desired life states and protected values without making the user estimate timelines or strategy.",
        questions=[
            Question("What future state would make life clearly better?", "Defines the direction PEGO should govern toward.", "private/goals/life-aim.md"),
            Question("What should PEGO help you stop tolerating?", "Identifies avoidable friction or underperformance.", "private/goals/life-aim.md"),
            Question("What should PEGO preserve even while pushing hard?", "Protects happiness-critical constraints.", "private/constitution/constitution.md"),
        ],
        avoid=[
            "Ask the user to choose a 1-year or 10-year timeline.",
            "Ask the user to design the strategy PEGO should model.",
        ],
        output="Life aim and constitution values draft.",
    ),
    "current-state": Phase(
        name="Current state",
        purpose="Capture current resources, constraints, and leverage points PEGO must use now.",
        questions=[
            Question("Where does daily life happen right now, and what constraints does that environment create?", "Grounds directives in the real setting.", "private/current-state/current-state.md"),
            Question("What work, income, assets, skills, network, and obligations exist today?", "Identifies resources PEGO can use for strategy.", "private/current-state/current-state.md"),
            Question("What time is realistically available on a normal weekday and weekend?", "Prevents impossible directive schedules.", "private/time/protected-time.md"),
        ],
        avoid=[
            "Ask whether the current job, home, or city is optimal.",
            "Ask the user to solve opportunity-cost strategy.",
        ],
        output="Current-state draft.",
    ),
    "environment": Phase(
        name="Environment",
        purpose="Identify concrete upcoming friction in home, household, supplies, events, and recurring annoyances.",
        questions=[
            Question("Which visible part of the home or yard is most annoying right now?", "Creates a concrete environment directive candidate.", "private/operator/operating-register.md"),
            Question("What upcoming event requires clothing, reservation, transport, gift, documents, or prep?", "Gives PEGO lead time before scrambling.", "private/operator/operating-register.md"),
            Question("Which food default, household supply, tool, or medication is missing or running low?", "Prevents avoidable health or household friction.", "private/operator/operating-register.md"),
        ],
        avoid=[
            "Ask broad questions about ideal home aesthetics.",
            "Ask for a complete inventory.",
        ],
        output="Operating-register update.",
    ),
    "strategy": Phase(
        name="Strategy",
        purpose="Capture the constraints and resources PEGO needs to model finance, career, venture, and skill paths.",
        questions=[
            Question("What income, autonomy, or ownership outcome would change life meaningfully?", "Defines strategic target classes without requiring a path.", "private/goals/strategy.md"),
            Question("What existing skill, asset, audience, network, or domain knowledge might create leverage?", "Identifies raw material for venture and career strategy.", "private/current-state/current-state.md"),
            Question("What financial, family, work, or time constraint limits risk-taking today?", "Bounds strategy and governance.", "private/governance/constraints.md"),
        ],
        avoid=[
            "Ask the user to pick the business idea prematurely.",
            "Ask the user to decide whether to quit a job.",
        ],
        output="Goal-strategy input.",
    ),
    "health": Phase(
        name="Health",
        purpose="Capture food, movement, sleep, optional health evidence, and medical boundaries for safe low-friction health directives.",
        questions=[
            Question("What are the current default breakfasts, lunches, dinners, snacks, and drinks?", "Identifies the actual diet baseline.", "private/health/baseline.md"),
            Question("What foods, movements, or routines are unacceptable, medically constrained, or likely to fail?", "Prevents brittle health directives.", "private/health/baseline.md"),
            Question("Which health metrics already exist and are acceptable to use as context: weight trend, blood pressure, blood sugar/A1C, lipids, resting heart rate, sleep, wearable summaries, or clinician guidance?", "Captures useful evidence without requiring new tracking.", "private/health/baseline.json"),
            Question("What is the smallest movement option that can happen without motivation?", "Creates a viable first movement directive.", "private/operator/operating-register.md"),
        ],
        avoid=[
            "Give medical advice.",
            "Ask the user to start measuring biomarkers unless the benefit and burden are explicit.",
            "Prescribe aggressive exercise or diet changes without review.",
        ],
        output="Health baseline.",
    ),
    "authority": Phase(
        name="Authority",
        purpose="Define what PEGO may recommend, direct, execute, or escalate.",
        questions=[
            Question("Which low-risk daily choices may PEGO direct by default?", "Establishes practical Level 2 territory if granted.", "private/constitution/constitution.md"),
            Question("Which domains require explicit approval every time?", "Protects high-impact areas.", "private/constitution/constitution.md"),
            Question("Which decisions require a waiting period, outside counsel, or governance review?", "Prevents reckless escalation.", "private/constitution/constitution.md"),
        ],
        avoid=[
            "Treat silence as authority.",
            "Bundle high-impact decisions into routine daily directives.",
        ],
        output="Authority grant draft.",
    ),
}


def normalize_phase(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def build_packet(phase: Phase, packet_date: str) -> str:
    question_rows = [
        f"| {question.text} | {question.why} | {question.destination} |"
        for question in phase.questions
    ]
    avoid_rows = [f"- {item}" for item in phase.avoid]
    return "\n".join(
        [
            "# First-Run Intake Packet",
            "",
            "## Date",
            "",
            packet_date,
            "",
            "## Phase",
            "",
            phase.name,
            "",
            "## Collaboration Mode",
            "",
            "USER mode.",
            "",
            "## Authority",
            "",
            "Level 1: Recommend during onboarding unless the private constitution grants more.",
            "",
            "## Purpose",
            "",
            phase.purpose,
            "",
            "## Known Facts",
            "",
            "Read from protected private state before asking. If missing, say that this phase is starting from no recorded facts.",
            "",
            "## Targeted Questions",
            "",
            "| Question | Why It Matters | Destination |",
            "| --- | --- | --- |",
            *question_rows,
            "",
            "## Do Not Ask",
            "",
            *avoid_rows,
            "",
            "## Output Candidate",
            "",
            phase.output,
            "",
            "## Privacy Status",
            "",
            "Protected private instance.",
            "",
            "## Next Step",
            "",
            "Ask targeted questions, record answers, update protected private state, then run the next intake phase.",
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--phase", default="boundary")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    phase_key = normalize_phase(args.phase)
    if phase_key not in PHASES:
        options = ", ".join(sorted(PHASES))
        raise SystemExit(f"unknown phase {args.phase!r}; expected one of: {options}")

    output = args.output or PRIVATE / "onboarding" / "intake" / f"{args.date}-{phase_key}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_packet(PHASES[phase_key], args.date))
    print(f"wrote: {output}")


if __name__ == "__main__":
    main_with_args()
