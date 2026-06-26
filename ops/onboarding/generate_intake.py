#!/usr/bin/env python3
"""Generate one protected PEGO first-run intake packet."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


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
    "finance-baseline": Phase(
        name="Finance baseline",
        purpose="Create a first decision-grade finance map without requiring an uploaded spreadsheet or account integration.",
        questions=[
            Question("What are your current income sources, rough monthly take-home pay, and how dependent is your household on that income?", "Establishes income dependency, runway risk, and career/finance governance constraints.", "private/finance/financial-position.md"),
            Question("What is your rough monthly burn, including housing, food, transport, insurance, travel, debt payments, and irregular annual expenses?", "Creates the first burn model so PEGO can reason about runway, freedom targets, and spending tradeoffs.", "private/finance/burn-model-notes.md"),
            Question("What assets and liabilities should PEGO know at a bucket level: cash, taxable investments, retirement, crypto, real estate, private equity, debt, taxes, or other obligations?", "Builds a protected bucket map without requiring account credentials or exact holdings first.", "private/finance/capital-buckets.md"),
            Question("What major future costs or lifestyle upgrades matter: home projects, family support, travel, vehicles, health care, education, business capital, taxes, or other commitments?", "Prevents PEGO from underestimating target lifestyle and capital needs.", "private/goals/financial-freedom.md"),
            Question("What financial actions are forbidden until explicit review: trades, transfers, account linking, debt changes, tax moves, job changes, purchases, or disclosures?", "Sets finance governance boundaries before recommendations drift into execution.", "private/constitution/constitution.md"),
        ],
        avoid=[
            "Ask for credentials, account linking, or exact account numbers.",
            "Ask for trades, allocation instructions, or tax actions.",
            "Require a spreadsheet before creating a useful baseline.",
            "Treat rough estimates as verified facts.",
        ],
        output="Finance baseline and unknowns map.",
    ),
    "career-baseline": Phase(
        name="Career baseline",
        purpose="Capture current work, income dependency, leverage, constraints, reputation, and risk boundaries.",
        questions=[
            Question("What is your current role, compensation dependency, main responsibilities, and near-term work pressure?", "Lets Career and Finance protect income while evaluating autonomy and optionality.", "private/career/baseline.md"),
            Question("What skills, proof of work, relationships, domain knowledge, or assets create leverage outside your current role?", "Identifies raw material for career capital, venture paths, and reputation-building directives.", "private/career/career-capital.md"),
            Question("What is unsatisfying, risky, or limiting about the current work path, and what must not be jeopardized?", "Defines the career problem without forcing premature job-change strategy.", "private/governance/constraints.md"),
            Question("What career-risking moves require explicit approval or waiting periods?", "Prevents PEGO from turning ambition into reckless action.", "private/constitution/constitution.md"),
        ],
        avoid=[
            "Ask the user to decide whether to quit.",
            "Recommend public reputation moves before privacy and employer constraints are clear.",
            "Use employer-sensitive information in reusable framework artifacts.",
        ],
        output="Career baseline and optionality map.",
    ),
    "home-baseline": Phase(
        name="Home baseline",
        purpose="Capture the home environment, recurring irritants, maintenance risks, household constraints, and serenity goals.",
        questions=[
            Question("What about the home, yard, land, or neighborhood most affects daily happiness right now?", "Identifies the environment condition most likely to become a high-value directive.", "private/goals/home-serenity.md"),
            Question("What recurring maintenance, clutter, repair, supply, seasonal, or pet/household issue should PEGO anticipate?", "Builds the operating register before annoyances become urgent.", "private/operator/operating-register.md"),
            Question("What work would disturb protected people, neighbors, sleep, quiet, privacy, or protected time?", "Prevents environment directives from damaging relationship or serenity goals.", "private/governance/constraints.md"),
            Question("What home projects or purchases are large enough to require governance review?", "Separates low-risk maintenance from renovation, contractor, property, or major purchase decisions.", "private/home/maintenance-system.md"),
        ],
        avoid=[
            "Ask for a complete home inventory.",
            "Turn a maintenance prompt into a renovation plan.",
            "Authorize purchases, contractors, or property actions without governance review.",
        ],
        output="Home baseline and operating-register update.",
    ),
    "relationships-baseline": Phase(
        name="Relationships baseline",
        purpose="Capture protected people, household peace, obligations, communication constraints, and disturbance boundaries.",
        questions=[
            Question("Who must PEGO protect from disturbance or unintended consequences?", "Identifies stakeholders and protected relationship constraints.", "private/current-state/current-state.md"),
            Question("What recurring relationship, household, family, friend, or social obligation should PEGO account for?", "Prevents directives from colliding with real commitments.", "private/operator/operating-register.md"),
            Question("What time, topics, decisions, or actions require explicit approval before PEGO directs them?", "Creates relationship-impact governance rules.", "private/constitution/constitution.md"),
        ],
        avoid=[
            "Ask for private third-party details unless needed for a directive.",
            "Issue confrontation, disclosure, or relationship-impacting directives without governance review.",
            "Treat protected relationship time as spare capacity.",
        ],
        output="Relationship constraints and protected-stakeholder map.",
    ),
    "exploration-baseline": Phase(
        name="Exploration baseline",
        purpose="Capture curiosity, travel, learning, leisure, taste, and renewal signals that make life richer.",
        questions=[
            Question("What activities, places, ideas, skills, games, travel, art, food, or experiences reliably make life feel larger or more alive?", "Gives Exploration and Happiness agents positive targets beyond productivity.", "private/goals/lifestyle-and-taste.md"),
            Question("What exploration has been crowded out by work, money, health, or household pressure?", "Identifies neglected but meaningful directives.", "private/operator/operating-register.md"),
            Question("What exploration costs time, money, health, or relationship capacity enough to need governance review?", "Prevents curiosity directives from bypassing real constraints.", "private/governance/constraints.md"),
        ],
        avoid=[
            "Turn exploration into productivity homework.",
            "Assume expensive travel is the only path to novelty.",
            "Schedule exploration into protected relationship or recovery time without review.",
        ],
        output="Exploration baseline and renewal candidates.",
    ),
    "communications-baseline": Phase(
        name="Communications baseline",
        purpose="Capture voice, taste, public-positioning constraints, and opportunity goals for writing or communication.",
        questions=[
            Question("What kind of public or private communication should PEGO help you produce, and what opportunities should it attract?", "Connects communications work to career, venture, taste, and opportunity strategy.", "private/person/voice-and-taste.md"),
            Question("What writing, tone, claims, topics, or private material would feel embarrassing, false, risky, or off-brand?", "Sets communication constraints before drafting or public positioning.", "private/person/tone.md"),
            Question("What examples of writing, design, software, places, people, or objects reflect your taste?", "Creates evidence for voice and taste rather than asking for abstract personality labels.", "private/person/voice-and-taste.md"),
        ],
        avoid=[
            "Use private facts publicly without explicit approval.",
            "Ask the user to describe their entire personality.",
            "Publish, post, or disclose without governance review.",
        ],
        output="Voice, taste, and communication baseline.",
    ),
    "happiness-baseline": Phase(
        name="Happiness baseline",
        purpose="Capture what PEGO should ultimately optimize for and which proxy goals may become traps.",
        questions=[
            Question("What reliably creates peace, joy, pride, meaning, love, curiosity, beauty, competence, or freedom?", "Defines positive signals the council should preserve and seek.", "private/happiness/model.md"),
            Question("What reliably creates regret, depletion, resentment, anxiety, shame, drift, or deadness?", "Identifies states PEGO should reduce or treat as warning signs.", "private/happiness/model.md"),
            Question("Which impressive goals could become traps if PEGO pursued them too aggressively?", "Prevents money, productivity, fitness, career, or status from overriding the actual life objective.", "private/constitution/constitution.md"),
            Question("What discomfort is worth choosing, and what discomfort should PEGO treat as a stop signal?", "Distinguishes useful challenge from harmful friction.", "private/happiness/model.md"),
        ],
        avoid=[
            "Use therapy framing.",
            "Treat happiness as a mood score.",
            "Optimize proxy goals without checking lived fit.",
        ],
        output="Happiness model baseline.",
    ),
    "goal-reconciliation": Phase(
        name="Goal reconciliation",
        purpose="Turn separate domain goals into council priority rules for cross-domain directive selection.",
        questions=[
            Question("Which goals must PEGO protect even when another goal seems urgent?", "Identifies constitutional or protected goals that should dominate council tradeoffs.", "private/goals/goal-reconciliation.md"),
            Question("Which active goals create the most upside if advanced this month, and which protect against the most downside if maintained?", "Separates upside creation from downside protection for council prioritization.", "private/goals/goal-reconciliation.md"),
            Question("When finance, health, work, home, relationships, exploration, or venture conflict, what tradeoffs feel acceptable and what tradeoffs require explicit approval?", "Creates conflict rules for Council before it claims to choose the best directive.", "private/goals/goal-reconciliation.md"),
            Question("What missing fact would most change PEGO's current goal priority?", "Identifies the highest-value next information request instead of asking broad questions.", "private/goals/goal-reconciliation.md"),
        ],
        avoid=[
            "Ask the user to rank every life goal.",
            "Force permanent priority rules from weak evidence.",
            "Let a proxy goal such as money, productivity, fitness, or status silently dominate protected goals.",
        ],
        output="Goal reconciliation and council priority model.",
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
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--phase", default="boundary")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    phase_key = normalize_phase(args.phase)
    if phase_key not in PHASES:
        options = ", ".join(sorted(PHASES))
        raise SystemExit(f"unknown phase {args.phase!r}; expected one of: {options}")

    output = args.output or private / "onboarding" / "intake" / f"{args.date}-{phase_key}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_packet(PHASES[phase_key], args.date))
    print(f"wrote: {output}")


if __name__ == "__main__":
    main_with_args()
