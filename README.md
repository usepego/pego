# PEGO

Personal Executive Governance OS.

PEGO is a framework for delegated next-action decision-making.

The premise is simple and a little uncomfortable: people already delegate their
next action to inboxes, calendars, habits, anxiety, and whatever is loudest.
PEGO asks whether a governed multi-agent system can do better.

Not better advice. A directive: one bounded next action, with why now, what is
deferred, and what authority the system does not have.

The human supplies goals, constraints, authority limits, private context, and
outcome feedback. PEGO synthesizes the next call.

## Core Loop

PEGO converts current life context into a directive, then evaluates the result.

```text
goals + constraints + current state + domain recommendations
  -> council synthesis
  -> governance check
  -> bounded directive
  -> outcome review
  -> updated context
```

Visible output:

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

Internal structure:

- domain agents produce specialized recommendations
- council resolves cross-domain conflict
- governance checks authority, privacy, risk, and reversibility
- private memory stores operating state
- outcome review scores decision quality

## Research Question

Can a governed agent system improve human action selection without eating the
human's authority layer?

PEGO treats this as an evaluation problem, not a productivity claim.

The framework tracks:

- directive quality
- goal fit
- constraint fit
- human burden
- follow-through probability
- outcome quality
- learning value

## Architecture

PEGO is a framework first. The current repository defines the protocols,
schemas, prompts, reference tools, and private-instance boundary.

```text
Human Constitution
  values, goals, constraints, authority, privacy, objections

Private Operating State
  current situation, domain baselines, outcomes, queues, session memory

Domain Agents
  finance, health, career, venture, home, relationships, exploration,
  happiness, communications, operations

Council
  cross-domain conflict resolution and single-directive synthesis

Governance
  authority level, risk, reversibility, privacy, dissent, protected time

Directive Surface
  one action, reason, fallback, deferrals, stop condition, next check-in

Outcome Review
  completion, friction, benefit, burden, contentment, decision quality
```

Core directories:

- `pego/`: reusable framework, protocols, schemas, templates, UX notes
- `ops/`: reference scripts for validation, synthesis, reviews, and local runs
- `AGENTS.md`: runtime instructions for AI agents operating in this workspace
- `decisions/`: durable architecture and governance decisions
- `private/`: protected private instance boundary; do not commit private facts

The reusable framework and the private instance are intentionally separate. See
`pego/governance/private-data-policy.md`.

## Agent Model

PEGO uses specialized agents because a life has real conflicts.

- Finance: runway, resilience, allocation, income, ownership
- Health: food, movement, sleep, recovery, follow-through
- Career: leverage, skill, reputation, autonomy, exit strategy
- Venture: independent income, market evidence, experiments
- Home: environment, supplies, maintenance, household friction
- Relationships: partner time, social connection, stakeholder impact
- Exploration: curiosity, craft, taste, optionality
- Happiness: whether the system is serving the actual life objective
- Communications: voice, public writing, positioning, opportunity
- Operations: daily and weekly directive execution
- Governance: authority, privacy, risk, reversibility, dissent
- Council: cross-domain reconciliation into one directive

Agents do not all get equal airtime. PEGO should ask only for the information
that would change the next decision.

## Council And Governance

The council is where conflict becomes a decision.

Finance may argue for reducing burn. Health may argue for sleep. Career may
argue for a leverage move. Home may argue that the environment is becoming a
drag. Governance asks whether the proposed action is allowed.

The council should record:

- candidate directives
- domain arguments
- dissent
- deferrals
- priority assumptions
- missing information
- selected directive
- reason the selected directive won

Authority is explicit:

- Level 0: Observe
- Level 1: Recommend
- Level 2: Direct
- Level 3: Execute
- Level 4: Escalate

High-impact financial, medical, legal, career, housing, relationship, privacy,
or hard-to-reverse actions require stronger review. PEGO can direct evidence
gathering before it can direct execution.

## Evaluation Loop

PEGO should prove itself against baselines.

The framework now includes review artifacts for:

- agent recommendation quality
- council synthesis quality
- information-value assessment
- decision-quality review
- goal reconciliation
- outcome review

Decision quality is not the same as task completion. A completed directive can
still be a bad call. A blocked directive can still teach the system something
important.

Outcome review evaluates:

- actionability
- goal fit
- constraint fit
- human burden
- timeliness
- risk control
- explanation quality
- follow-through probability
- outcome quality
- learning value

The research question is direct:

```text
Can governed agents produce better next-action decisions than unmanaged
prioritization, generic assistant advice, or single-domain optimization?
```

## Runtime Model

PEGO is runtime-neutral.

The framework should be portable across Codex, another LLM agent host,
LangGraph, Vercel AI SDK, an MCP server, a mobile app, or a custom runtime. The
important thing is preserving the lifecycle:

```text
state -> agent recommendations -> council -> governance -> directive
  -> outcome -> review -> updated state
```

### Current Runtime: Codex

The current practical runtime is Codex operating in this repository.

When the user says:

```text
Start PEGO.
```

Codex should:

1. Read `AGENTS.md`.
2. Load `pego/operations/first-run.md`.
3. Select USER mode unless the user is clearly doing engineering or UX work.
4. Check private-instance readiness.
5. Read active private operating state.
6. Load relevant agent and governance protocols.
7. Ask one decision-grade question or issue one directive.
8. Hide setup commands, diffs, scratch reasoning, and file mechanics from the
   user-facing PEGO response.

The human should experience PEGO, not the adapter.

### Future Runtimes

Possible future adapters:

- MCP server for agent-host interoperability
- Vercel AI SDK / Next.js for a polished web and mobile product surface
- LangGraph for durable stateful orchestration
- custom runtime if PEGO-specific governance concepts outgrow general tools

See `pego/architecture/runtime-options.md` and
`pego/architecture/runtime-roadmap.md`.

## What The Python Scripts Are

The Python in `ops/` is reference adapter machinery.

It does useful deterministic work:

- generate structured artifacts
- validate schemas
- synthesize queues
- run council-reference flows
- check private-instance readiness
- record outcomes
- review decision quality
- run smoke tests
- enforce privacy and repository hygiene

But Python is not "the PEGO brain."

The LLM runtime performs interpretation, agent reasoning, council argument, and
operator-facing synthesis. Python tools support that runtime by producing and
validating portable PEGO artifacts.

## Use With Your LLM

Near-term assumption:

```text
Install PEGO, open an LLM agent workspace, and let the agent discover the
framework instructions.
```

For this repository today:

1. Open the repo in Codex or another capable agent environment.
2. Let the agent read `AGENTS.md`.
3. For framework development, ask engineering questions normally.
4. For active operation, say `Start PEGO`.
5. The agent should use PEGO protocols, private state, and local adapter tools
   behind the scenes.

For future packaged use, the shape may become:

```sh
uv tool install usepego
pegoctl init
```

Then open Codex or another LLM runtime against the initialized PEGO workspace.

## Local Verification

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

Only `private/README.md` should be tracked.

## Current Status

PEGO is early and experimental.

The current focus is making the loop real:

```text
onboarding -> domain baselines -> goal reconciliation -> agent recommendations
  -> council synthesis -> directive -> outcome -> decision-quality review
```

The public site explains the idea. This repository is where the framework,
contracts, and reference implementation live.
