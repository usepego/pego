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
- Communications preserves voice, taste, public writing, positioning, and opportunity-oriented communication.
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

## Project Goals And Constraints

PEGO core should remain runtime-neutral agent infrastructure.

The project goal is to define the governing framework: agent roles, constitutions, authority levels, directive schemas, governance checks, privacy rules, memory protocols, operating loops, and adapter contracts.

The runtime can later be LangGraph, Vercel AI SDK, a custom service, a mobile app, a Slack bot, a local CLI, or another environment. Those are hosting and surface choices, not PEGO itself.

Python and other code are welcome for validation, CI, scaffolding, migrations, privacy checks, reference adapters, and developer workflows. They should not make the framework depend on one runtime, programming language, vendor, or user interface.

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

## Framework And Private Instance

This repository separates the reusable PEGO framework from a private local instance.

- `AGENTS.md` contains runtime instructions for AI agents operating in this repository.
- `pego/` contains reusable framework material that may eventually become open source or productized.
- `private/` is reserved for the protected private PEGO instance: real goals, constraints, telemetry, directives, and life details.
- `ops/` contains lightweight scripts, integrations, checks, CI-oriented validation, and local operating machinery.
- `decisions/` contains durable decision records about PEGO architecture and governance.

Do not place private life details, secrets, credentials, real financial data, health records, relationship details, personal journals, or local directives in `pego/`.

The reusable framework layer and the protected private instance are intentionally separate. See `pego/governance/private-data-policy.md` for the product boundary and implementation rules.

Repository access should be least-privilege and scoped only to this PEGO repository. Do not grant unrelated organization or employer access for PEGO work.

## How You Experience PEGO

PEGO should not feel like a command line or a dashboard.

The intended experience is a governed operating cadence:

- PEGO learns enough about goals, constraints, environment, resources, and
  authority to govern safely.
- The Council reconciles finance, health, career, venture, home, relationships,
  happiness, and governance.
- PEGO delivers one directive at the right time.
- The human executes, objects, reports status, or supplies missing facts.
- Outcomes update the system so tomorrow's directives are better.

A first interaction should be as simple as:

```text
Start PEGO.
```

But mature PEGO should not depend on the human remembering to ask. Approved
runtime surfaces should deliver directives through the right medium: mobile,
watch, desktop, chat, calendar, email, or another adapter.

Example PEGO outputs:

- "Spend 60 minutes filling the customer-pain evidence map. This is the
  lowest-risk path toward business evidence. Stop before protected evening
  time."
- "For the next meal, choose the option that best fits the active health goal,
  available food environment, cost, time, and likely follow-through."
- "Do not execute the portfolio change yet. Build the account, holdings, risk,
  and authority map first; execution remains locked."
- "The garden is becoming a visible home-serenity risk. Do a 25-minute targeted
  outdoor block before the problem expands."

The local `pegoctl` commands are developer adapter mechanics, not the primary
new-user experience. See `pego/operations/local-adapter.md` for local
verification and command details.

## Builder Notes

PEGO is currently private and pre-release.

The reusable framework is being designed so future users can interact with PEGO
through normal surfaces: conversation, mobile, watch, desktop, calendar, email,
Slack, or another approved adapter. The local command-line tools exist for early
operators and maintainers to validate the framework, exercise operating loops,
and protect the private-instance boundary while the user experience matures.

For those engineering details, see:

- `pego/operations/local-adapter.md`
- `pego/architecture/distribution-installation.md`

## Current Status

PEGO is in early architecture and governance design.

The current focus is the agent layer: constitutions, authority levels, council protocols, decision packets, compliance review, private-instance boundaries, and the operating loop that turns long-range goals into actions the human can take now.
