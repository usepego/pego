# PEGO Schemas

Runtime-neutral JSON Schema contracts for PEGO artifacts.

These schemas define the shape future runtimes should preserve when moving from
markdown templates to structured data. They are not a runtime choice. A
LangGraph adapter, Vercel interface, custom service, mobile app, Slack bot, CLI,
or local script should all be able to produce and consume these contracts.

## Core Artifacts

- `agent-recommendation.schema.json`: structured output from a domain agent.
- `command-response.schema.json`: single next-directive response from the
  intra-day command loop.
- `directive-candidate.schema.json`: proposed action before synthesis.
- `compliance-review.schema.json`: governance review of a recommendation,
  directive, or decision packet.
- `decision-packet.schema.json`: formal escalation artifact for high-impact
  Level 4 decisions.
- `directive-outcome.schema.json`: evidence captured after a directive is
  attempted.
- `outcome-review.schema.json`: learning decision produced from directive
  outcome evidence.
- `directive-preflight.schema.json`: lightweight governance classification for
  a proposed directive before adoption.
- `directive-queue.schema.json`: live intra-day queue for active, deferred,
  blocked, and selected directives.
- `synthesized-day-plan.schema.json`: scheduled operating plan produced from
  prioritized directive candidates.
- `runtime-adapter-manifest.schema.json`: capability declaration for a PEGO
  runtime adapter.
- `finance-scenario-input.schema.json`: protected private finance assumptions
  consumed by scenario engines.
- `finance-scenario-output.schema.json`: protected private scenario results
  produced by finance engines.
- `finance-check-in.schema.json`: targeted protected finance questions used to
  gather only the state needed for scenario updates, runway classification, or
  governance review.
- `private-instance-readiness.schema.json`: safe readiness status for a
  protected private PEGO instance.
- `goal-strategy.schema.json`: structured strategy for a long-range goal.
- `monthly-strategy-review.schema.json`: structured review of goals,
  assumptions, agent assessments, and next-month priorities.
- `health-baseline.schema.json`: protected private health baseline with
  optional evidence tiers and biomarker fields.
- `health-check-in.schema.json`: targeted protected health questions used to
  gather only the state needed for directive selection or review.

## Rules

- Public schemas must not contain private subject facts.
- Schemas should model PEGO concepts, not a specific hosting runtime.
- Enum values should match the public markdown templates unless a decision
  record explicitly changes them.
- Runtime adapters may add private implementation metadata outside the reusable
  framework, but must preserve these public fields when exchanging PEGO
  artifacts.
