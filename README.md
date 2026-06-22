# PEGO

Personal Executive Governance OS.

PEGO is an experiment in turning personal decision-making over to a governed council of AI agents.

Most "life OS" systems help you organize yourself. They track habits, summarize calendars, capture goals, or act like a helpful assistant waiting for instructions. PEGO starts from a different premise: many people already know, at some level, that they need stronger direction than another dashboard can provide. The hard part is not always information. It is deciding, committing, sequencing, and acting through uncertainty, anxiety, competing goals, and short-term avoidance.

PEGO is designed for that harder problem.

The human supplies values, goals, constraints, objections, telemetry, preferences, and lived feedback. The system is responsible for producing directives, plans, tradeoff analyses, dissent, reviews, and escalations. Within explicit authority limits, PEGO does not merely suggest what the human could do. It governs what should happen next.

## The Core Idea

PEGO treats a life as something that can be governed without pretending it can be fully optimized.

The goal is not maximum productivity, maximum wealth, perfect health metrics, or a quantified-self score. The top-level aim is a better life: happiness, autonomy, health, love, meaning, competence, security, beauty, curiosity, and long-term flourishing.

That requires more than one assistant. PEGO uses specialized agents with different mandates:

- Finance protects resilience, capital allocation, runway, income, ownership, and financial freedom.
- Health converts food, movement, sleep, and recovery into sustainable directives.
- Career evaluates work, leverage, skill growth, reputation, autonomy, and exit strategy.
- Relationships protects spouse/partner time, household peace, social connection, and stakeholder impact.
- Exploration preserves curiosity, learning, travel, craft, taste, and optionality.
- Happiness checks whether the system is serving the actual life objective rather than proxy goals.
- Operations turns strategy into daily and weekly directives.
- Governance enforces authority levels, privacy, evidence quality, reversibility, constraints, and dissent.
- The Council reconciles domain-agent recommendations into one coherent directive or escalation.

## What Makes PEGO Different

PEGO is not a personal assistant.

A personal assistant helps when asked. PEGO is intended to decide what should be done, surface the next action, and keep the human moving toward stated goals.

PEGO is not a habit tracker.

A habit tracker records behavior. PEGO asks which behaviors should exist, why they matter, what tradeoffs they create, and how they should be governed.

PEGO is not quantified self.

Quantified-self systems can collect useful telemetry, but PEGO treats telemetry as evidence for governance, not as the objective. A good life is not reducible to a dashboard.

PEGO is not pure automation.

The system has authority, but that authority is constitutional. High-impact decisions require stronger review, dissent, waiting periods, explicit approval, or outside professional input. Decisive does not mean reckless.

PEGO is not just goal planning.

Long-range goals are decomposed into strategies, milestones, fallback paths, experiments, and immediate directives. PEGO owns the strategy work; the human owns values, constraints, objections, and final constitutional authority.

## Why This Exists

Decision anxiety, ambiguity, and competing priorities can quietly cap a person's life. The cost is not only missed productivity. It can be years of under-commitment, stale work, neglected health, unmanaged finances, shallow exploration, or choices optimized for short-term comfort instead of long-term happiness.

PEGO is a response to that pattern. It asks:

- What if the person did not have to personally arbitrate every tradeoff from scratch?
- What if specialized agents could reason from the person's constitution, current state, resources, goals, and constraints?
- What if the system could be bold about life direction while still being governed, private, reviewable, and reversible where possible?
- What if the output was not advice, but a directive small enough to execute today?

## Governance Model

PEGO authority is explicit.

- Level 0: Observe.
- Level 1: Recommend.
- Level 2: Direct.
- Level 3: Execute.
- Level 4: Escalate.

Low-risk directives can be routine. High-impact actions such as major financial decisions, career exits, medical changes, legal commitments, relationship-impacting decisions, privacy-impacting disclosure, relocation, or hard-to-reverse moves require formal governance review.

Every meaningful directive should be assessed for:

- Constitutional alignment.
- Goal alignment.
- Constraint fit.
- Evidence quality.
- Risk.
- Reversibility.
- Privacy impact.
- Dissent.
- Review date or stop condition.

## Repository Boundary

This repository separates the reusable PEGO framework from a private local instance.

- `AGENTS.md` contains runtime instructions for AI agents operating in this repository.
- `pego/` contains reusable framework material that may eventually become open source or productized.
- `private/` contains the private PEGO instance: real goals, constraints, telemetry, directives, and life details.
- `ops/` contains lightweight scripts, integrations, checks, and local operating machinery.
- `decisions/` contains durable decision records about PEGO architecture and governance.

Do not place private life details, secrets, credentials, real financial data, health records, relationship details, personal journals, or local directives in `pego/`.

Private instance files under `private/` are local-only and ignored by Git, except for the placeholder `private/README.md`.

Repository access should be least-privilege and scoped only to this PEGO repository. Do not grant unrelated organization or employer access for PEGO work.

## Current Status

PEGO is in early architecture and governance design.

The current focus is the agent layer: constitutions, authority levels, council protocols, decision packets, compliance review, private-instance boundaries, and the operating loop that turns long-range goals into actions the human can take now.
