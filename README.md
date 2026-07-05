# PEGO

Personal Executive Governance OS.

**AI governance for your own behavior.**

[Product page](https://usepego.com)

PEGO is behavioral augmentation through AI governance.

You are already governed by hunger, fatigue, anxiety, defaults, calendar
pressure, social context, screens, environment, and whatever is loudest now.
PEGO makes that steering explicit, constitutional, reviewable, and aimed at
the life you say you want.

The system is built around a specific handoff: the human defines the
constitution, goals, constraints, private context, authority boundaries, and
objections. PEGO makes the next decision within those boundaries, issues one
directive, and learns from what happened after the human tried it.

This is not an assistant waiting for delegated tasks. PEGO is deliberately
interventionist: it shapes conditions, defaults, timing, friction, attention,
and escalation so the next action serves stated goals instead of the nearest
impulse.

The difference between manipulation and governance is authority. PEGO acts
inside boundaries the human defines: constitution, privacy, reversibility,
dissent, stop conditions, and review.

## Measurable Governance Loop

PEGO turns current state, goals, constraints, and outcome evidence into one
governed directive, then reviews what happened so future decisions improve.

```text
state evidence
  -> goal progress
  -> agent recommendations
  -> council decision
  -> directive scorecard
  -> next directive
  -> outcome review
  -> agent calibration
  -> behavior-loop detection
  -> strategy review
```

The loop matters because PEGO is not neutral advice. It is governed behavioral
infrastructure. Decisions should be inspectable, attributable, revisable, and
bounded by authority.

Public PEGO should make these governance surfaces legible:

- what evidence shaped the decision
- which goals and constraints mattered
- what agents argued and what dissent survived
- why one directive was selected and what was deferred
- what happened after the directive
- what should change before the next decision

## What This Repository Contains

This repository is the PEGO framework and current local reference adapter. It
defines:

- agent mandates and domain protocols
- Council synthesis and dissent handling
- governance, authority levels, privacy rules, and compliance review
- directive, outcome, memory, and decision packet templates
- JSON schemas for runtime-neutral artifacts
- public positioning for measurable governance-loop concepts
- private-instance boundaries
- local `pegoctl` tooling for early operation and verification

The product idea is larger than this local adapter. The repository exists so a
human or LLM runtime can inspect the framework, operate a protected private
instance, and eventually implement PEGO through other runtimes.

## Operating Loop

PEGO converts current life context into one bounded directive, then reviews
whether the decision was good enough to trust, revise, repeat, or downgrade.

```text
constitution + goals + private state + current context
  -> specialist agent recommendations
  -> council synthesis
  -> governance preflight
  -> one directive
  -> outcome review
  -> updated private operating memory
```

The user-facing command response is intentionally small:

```text
State update.
Next directive.
Time box.
Start condition.
Do this.
Reason.
Fallback.
Deferred.
Stop condition.
Next check-in.
```

## Framework Layout

- `AGENTS.md`: operating instructions for AI agents working in this repository.
- `pego/`: reusable public framework files.
- `pego/agents/`: specialist agent protocols and Council behavior.
- `pego/governance/`: authority, privacy, conflict, and compliance rules.
- `pego/operations/`: operating loops for first run, daily use, synthesis,
  outcome review, memory, and adapter behavior.
- `pego/templates/`: markdown artifact templates.
- `pego/schemas/`: runtime-neutral JSON schemas.
- `pego/system/registry.json`: framework registry and verification map.
- `ops/`: local reference adapter scripts.
- `src/usepego/cli.py`: installable `pegoctl` command wrapper.
- `decisions/`: durable architecture and governance decision records.
- `private/`: protected private instance boundary. Only `private/README.md`
  should be tracked.

The reusable framework and protected private instance are intentionally
separate. See `pego/governance/private-data-policy.md`.

## Agent Model

PEGO uses specialist agents because a life has real conflicts.

- **Finance**: runway, resilience, allocation, income, ownership, financial
  freedom.
- **Health**: food, movement, sleep, recovery, low-friction follow-through.
- **Career**: leverage, skill, reputation, autonomy, exit strategy.
- **Venture**: independent income, market evidence, experiments, first tests.
- **Home and Environment**: home, garden, supplies, maintenance, serenity.
- **Relationships**: partner time, household peace, social connection,
  stakeholder impact.
- **Exploration**: curiosity, craft, culture, taste, optionality.
- **Communications**: voice, public writing, positioning, opportunity.
- **Happiness**: whether PEGO is serving the actual life objective rather than
  proxy goals.
- **Operations**: daily, weekly, and monthly directive synthesis.
- **Governance**: authority, privacy, risk, reversibility, dissent.
- **Council**: cross-domain reconciliation into one directive, revision,
  information request, escalation, or block.

Agents do not all get equal airtime. PEGO should ask only for information that
would change the next directive or a meaningful governance decision.

## Council And Governance

The Council is where conflict becomes a decision.

Finance may argue for runway. Health may argue for recovery. Career may argue
for a leverage move. Home may argue that the environment is becoming a drag.
Relationships may object to a schedule impact. Governance checks whether the
proposed action is allowed.

Council outputs preserve:

- selected directive or escalation
- rationale
- expected benefit
- key risks
- dissent
- required handoffs
- authority level
- stop conditions
- review point

Authority is explicit:

- **Level 0: Observe**
- **Level 1: Recommend**
- **Level 2: Direct**
- **Level 3: Execute**
- **Level 4: Escalate**

High-impact financial, medical, legal, tax, career, housing, relationship,
privacy, or hard-to-reverse actions require stronger review. PEGO can direct
evidence gathering before it can direct execution.

## Private Instance

The private instance contains the real operating memory:

- constitution, values, non-negotiables, and authority grants
- current state and protected time
- domain baselines
- goals and goal reconciliation
- directive candidates, queues, command responses, and outcomes
- session logs and context updates
- finance, health, relationship, work, household, writing, and preference data

Private operating state belongs under `private/` or another configured protected
root. Public framework files must not contain private subject facts.

To use an external protected root:

```sh
python3 pegoctl --private-root /path/to/protected/private-root guide
```

You can also set:

```sh
export PEGO_PRIVATE_ROOT=/path/to/protected/private-root
```

## Start A Private PEGO Instance

From a fresh checkout:

```sh
python3 pegoctl doctor
python3 pegoctl bootstrap
python3 pegoctl guide
```

Then open the repository in a capable LLM agent environment and say:

```text
Start PEGO.
```

The agent should read `AGENTS.md`, follow `pego/operations/first-run.md`, run
private readiness checks, inspect available private operating state, and return
one operating response: a directive, a targeted question, a fallback, or a stop
condition.

The human should experience PEGO, not setup mechanics. Local commands, diffs,
private file maintenance, and adapter traces are internal work unless the human
asks for implementation details.

If PEGO does not yet have enough private context, generate the first intake
packet:

```sh
python3 pegoctl intake --phase boundary
```

Useful next phases include:

```sh
python3 pegoctl intake --phase current-state
python3 pegoctl intake --phase finance-baseline
python3 pegoctl intake --phase career-baseline
python3 pegoctl intake --phase health
python3 pegoctl intake --phase home-baseline
python3 pegoctl reconcile-goals
```

Do not treat onboarding as a giant life questionnaire. PEGO should ask the
smallest decision-grade question that changes the next directive or improves
future directive quality.

## Operating Commands

The local adapter exposes useful commands through `pegoctl`:

```sh
python3 pegoctl readiness
python3 pegoctl storage
python3 pegoctl brief
python3 pegoctl check-in "Available: 30 minutes. What is next?"
python3 pegoctl close-session
```

Common generation and review commands:

```sh
python3 pegoctl health-candidates
python3 pegoctl home-candidates
python3 pegoctl anticipate
python3 pegoctl daily synthesize --candidate private/directives/candidates/health-candidates.md
python3 pegoctl next --available 30 --energy medium --location computer
python3 pegoctl daily outcome --directive "Example directive" --completion completed
python3 pegoctl daily review --outcome private/outcomes/directives/example.md
```

These commands write protected artifacts under the private instance. They should
not print private directive contents by default.

## Runtime Model

PEGO core is runtime-neutral.

The current local adapter uses markdown protocols, JSON schemas, and Python
scripts because they are inspectable and useful during early design. Those
scripts are not the PEGO brain.

The LLM runtime performs interpretation, agent reasoning, Council argument, and
operator-facing synthesis. The local scripts support that runtime by generating,
validating, and reviewing portable PEGO artifacts.

Future adapters may use:

- local or hosted agent workspaces
- tool-capability servers
- web and mobile interfaces
- messaging, email, calendar, watch, or ambient interfaces
- a custom governed runtime if PEGO-specific concepts require it

Any adapter should preserve the same lifecycle:

```text
state -> recommendations -> council -> governance -> directive
  -> outcome -> review -> updated state
```

See:

- `pego/architecture/agent-infrastructure.md`
- `pego/architecture/runtime-options.md`
- `pego/architecture/runtime-adapter-lifecycle.md`
- `pego/architecture/tool-contracts.md`

## What The Python Scripts Do

The Python under `ops/` is deterministic reference adapter machinery. It can:

- check repository hygiene
- bootstrap a private instance skeleton
- check private readiness without printing private contents
- generate intake packets
- generate directive candidates
- synthesize directive queues
- select one next directive
- run governance preflight
- record outcomes
- review outcome and decision quality
- promote context-update candidates
- run local smoke tests

Python is allowed to make the framework usable. It should not make PEGO depend
on Python as the conceptual runtime.

## Verification

Before committing public framework work:

```sh
python3 ops/pego_doctor.py
```

Useful smoke-test sweep:

```sh
python3 -c 'import pathlib, subprocess, sys
files=sorted(str(p) for p in pathlib.Path("ops").rglob("test_*.py"))
for f in files:
    result=subprocess.run([sys.executable, f], text=True)
    if result.returncode:
        sys.exit(result.returncode)
print(f"passed {len(files)} smoke tests")'
```

Privacy boundary check:

```sh
git ls-files private
```

Expected output:

```text
private/README.md
```

## Current Status

PEGO is an early but operating framework.

The current focus is making private-instance operation real:

```text
onboarding -> domain baselines -> goal reconciliation -> agent recommendations
  -> council synthesis -> directive -> outcome -> decision-quality review
```

The public site explains the product idea. This repository is where the
framework, contracts, and reference implementation live.
