# PEGO Schemas

Runtime-neutral JSON Schema contracts for PEGO artifacts.

These schemas define the shape future runtimes should preserve when moving from
markdown templates to structured data. They are not a runtime choice. A
LangGraph adapter, Vercel interface, custom service, mobile app, Slack bot, CLI,
or local script should all be able to produce and consume these contracts.

## Core Artifacts

- `agent-recommendation.schema.json`: structured output from a domain agent.
- `directive-candidate.schema.json`: proposed action before synthesis.
- `compliance-review.schema.json`: governance review of a recommendation,
  directive, or decision packet.
- `decision-packet.schema.json`: formal escalation artifact for high-impact
  Level 4 decisions.
- `directive-outcome.schema.json`: evidence captured after a directive is
  attempted.
- `runtime-adapter-manifest.schema.json`: capability declaration for a PEGO
  runtime adapter.
- `finance-scenario-input.schema.json`: protected private finance assumptions
  consumed by scenario engines.
- `finance-scenario-output.schema.json`: protected private scenario results
  produced by finance engines.
- `private-instance-readiness.schema.json`: safe readiness status for a
  protected private PEGO instance.
- `goal-strategy.schema.json`: structured strategy for a long-range goal.
- `monthly-strategy-review.schema.json`: structured review of goals,
  assumptions, agent assessments, and next-month priorities.

## Rules

- Public schemas must not contain private subject facts.
- Schemas should model PEGO concepts, not a specific hosting runtime.
- Enum values should match the public markdown templates unless a decision
  record explicitly changes them.
- Runtime adapters may add private implementation metadata outside the reusable
  framework, but must preserve these public fields when exchanging PEGO
  artifacts.
