# State Inputs

PEGO should understand the human's current state from more than text prompts.
Text check-ins are the first adapter, not the final model.

The normalized input artifact is:

```text
pego/schemas/state-signal.schema.json
pego/templates/state-signal.md
```

State signals are protected private evidence that can inform agent
recommendations, goal progress, council deliberation, directive synthesis, and
outcome review.

## Input Sources

Supported source classes:

- Manual text check-ins.
- Directive outcomes.
- Wearable activity, sleep, recovery, and health summaries.
- Calendar availability and event context.
- Bank account activity summaries.
- Device sensors, app usage, location context, and environment signals.
- Documents or imported private files.
- External APIs and runtime adapters.
- Agent observations and inferences.

Future adapters may connect Apple Watch, activity feeds, bank data providers,
calendar tools, mobile apps, home devices, or other sources. The public
framework must stay provider-neutral. Provider-specific credentials, tokens,
raw records, and sync code belong outside public framework artifacts.

## Normalization Rule

Every adapter should convert raw input into a state signal before PEGO uses it
for governance decisions.

```text
raw input -> private adapter -> state signal -> goal progress -> agent recommendation -> council/directive/outcome
```

The signal should preserve:

- Source type.
- Ingestion mode.
- Domain and owning agent.
- Signal type.
- Decision-relevant summary.
- Measurements if useful.
- Affected goals.
- Evidence strength.
- Confidence.
- Privacy class.
- Raw source reference.
- Raw data retention.
- Governance notes.
- Review and expiry timing.

## Finance Boundary

Bank account activity is useful state evidence, but it is sensitive financial
data.

Rules:

- Treat bank activity as protected private state.
- Store summaries or derived measurements by default, not raw transactions.
- Do not store account numbers, credentials, OAuth tokens, cookies, or raw
  provider payloads in PEGO framework files.
- Use read-only imports unless a separate governance review explicitly grants
  narrower authority.
- Bank activity may inform spending patterns, income timing, cashflow risk,
  subscription drift, upcoming bill pressure, or finance check-in questions.
- Bank activity never authorizes transfers, trades, purchases, debt actions,
  account changes, or disclosure.

## Health And Wearable Boundary

Wearable activity can inform health, energy, sleep debt, recovery, and movement
defaults. It should not become constant surveillance.

Rules:

- Summarize continuous telemetry into decision-relevant signals.
- Prefer low-burden signals that change directives.
- Do not request new biometric tracking unless the expected governance value is
  clear.
- Treat health telemetry as protected private state.
- Escalate medical interpretation beyond lifestyle directive selection.

## Agent Ownership

Each domain agent owns interpretation in its specialization:

- Finance Agent: bank activity, spending, income, cashflow, account-data
  recency, downside risk.
- Health Agent: activity, sleep, recovery, nutrition, energy, health
  constraints.
- Career Agent: work context, calendar pressure, career-risk signals.
- Venture Agent: venture work evidence, market observations, experiment
  progress.
- Home and Environment Agent: home state, maintenance, supplies, environment
  friction.
- Relationships Agent: protected time, stakeholder impact, social context.
- Exploration Agent: curiosity, renewal, culture, travel, life richness.
- Happiness Agent: contentment, meaning, proxy-goal traps, lived fit.
- Operations Agent: time windows, location, energy, blockers, queue fit.
- Governance Agent: authority, privacy, risk, reversibility, data retention,
  and third-party exposure.

## Goal Progress

State signals should feed domain goal progress records:

```text
pego/schemas/goal-progress.schema.json
pego/templates/goal-progress.md
```

Goal progress separates:

- Leading indicators: signals likely to affect future progress.
- Lagging indicators: evidence that progress or risk actually happened.
- Trajectory: improving, stable, worsening, mixed, or unknown.
- Confidence: how much PEGO should trust the current model.
- Directive attribution: which directives or outcomes appear to have moved the
  goal.

If evidence is thin, stale, or ambiguous, PEGO should lower confidence and
prefer a targeted measurement or low-risk information-gathering directive.

## Governance

Any new adapter that reads accounts, health telemetry, location, messages,
browser history, app usage, home sensors, or third-party services must include
a governance and privacy review.

State-input features must preserve the public/private boundary:

- Public framework files define provider-neutral contracts.
- Private raw data and provider identifiers stay in protected private storage
  or external providers.
- Public examples use synthetic signals only.
