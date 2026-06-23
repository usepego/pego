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

## Local Operation

The local reference command wrapper is `pegoctl`. It is a thin adapter for
checking and exercising PEGO artifacts during development. It is not the PEGO
runtime.

### First Use

The intended first-use experience is not a command hunt. A human should start
by talking to the agent:

```text
Start PEGO.
```

or:

```text
What should I do next?
```

The agent or runtime adapter should then:

- Check the framework and protected private instance.
- Create missing private-instance skeleton files if needed.
- Explain only the user-facing decision, not the underlying command sequence.
- Begin phased onboarding if core private state is missing.
- Return one targeted question or one directive, depending on readiness.

The human-facing start protocol is defined in
`pego/operations/start-pego.md`.

For the current local adapter, those behind-the-scenes checks may include:

```sh
python3 pegoctl doctor
python3 pegoctl bootstrap
python3 pegoctl guide
```

These are adapter mechanics, not the user experience. If PEGO does not yet have
enough queue or context to choose a real directive, it should ask one targeted
operating question rather than issuing a generic plan.

### Reference Commands

The broader local command surface is:

```sh
python3 pegoctl doctor
python3 pegoctl guide
python3 pegoctl readiness
python3 pegoctl storage --confirm-backup
python3 pegoctl intake --phase boundary
python3 pegoctl daily-directive
python3 pegoctl daily health-check-in
python3 pegoctl weekly
python3 pegoctl monthly
python3 pegoctl finance-run --write-summary
python3 pegoctl finance-review
python3 pegoctl health-candidates
python3 pegoctl meal --option private/health/food-options/options.json
python3 pegoctl home-candidates
python3 pegoctl anticipate --domain Environment
python3 pegoctl attention --option private/attention/options/options.json
python3 pegoctl compliance-review --directive private/directives/daily/YYYY-MM-DD.md
python3 pegoctl public-writing
python3 pegoctl brief
python3 pegoctl check-in "Done: breakfast. Available: 45 minutes. What's next?"
python3 pegoctl close-session
python3 pegoctl promote-context
python3 pegoctl apply-context
```

Future interfaces may be CLI, chat, mobile, watch, Slack, web, or another
surface, but they should preserve the same agent contracts, schemas, governance
checks, and private-instance boundary.

For protected operation outside the framework checkout, set `PEGO_PRIVATE_ROOT`
or pass `--private-root` before the command:

```sh
python3 pegoctl --private-root ~/Documents/PEGO/private guide
python3 pegoctl --private-root ~/Documents/PEGO/private check-in "Done: lunch. Available: 30 minutes. What's next?"
```

Start with `pegoctl guide` when you are unsure what PEGO needs next. It reports
safe operating status, storage posture, and a recommended next command without
printing private contents or absolute protected paths.

## Packaging Direction

The installable package name is `usepego`, and the installed command is
`pegoctl`.

PEGO should use standard Python packaging only as a distribution surface, not as
the definition of the product runtime. The current direction is a small
`pyproject.toml` package with a `[project.scripts]` entry point, installed
eventually through tools such as:

```sh
uv tool install usepego
```

or:

```sh
pipx install usepego
```

Public publishing is intentionally not enabled yet. Before that happens, PEGO
should use a public repository, clean release process, security policy, CI,
PyPI Trusted Publishing, and package provenance/attestations. See
`pego/architecture/distribution-installation.md`.

## Current Status

PEGO is in early architecture and governance design.

The current focus is the agent layer: constitutions, authority levels, council protocols, decision packets, compliance review, private-instance boundaries, and the operating loop that turns long-range goals into actions the human can take now.
