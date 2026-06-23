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
- `intra-day-session-log.schema.json`: protected USER-mode session log
  preserving check-ins, state changes, command responses, and governance notes
  across a day.
- `directive-candidate.schema.json`: proposed action before synthesis.
- `compliance-review.schema.json`: governance review of a recommendation,
  directive, or decision packet.
- `decision-packet.schema.json`: formal escalation artifact for high-impact
  Level 4 decisions.
- `council-decision.schema.json`: cross-agent synthesis decision preserving
  outcome, dissent, handoffs, governance status, and next action.
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
- `voice-and-taste-model.schema.json`: protected private model for writing
  voice, humor, taste, influences, public positioning, and drafting rules.
- `food-option.schema.json`: protected food option from manual, grocery,
  restaurant, menu, nutrition, map, delivery, or agent-estimate sources.
- `meal-decision.schema.json`: protected meal decision comparing available
  food options and producing a concrete food directive.
- `attention-option.schema.json`: protected live-event, media, leisure, or
  rest option used for attention governance.
- `attention-decision.schema.json`: protected attention decision selecting
  watch live, multitask live, highlights later, score only, defer, skip, or
  escalate.

## Rules

- Public schemas must not contain private subject facts.
- Schemas should model PEGO concepts, not a specific hosting runtime.
- Enum values should match the public markdown templates unless a decision
  record explicitly changes them.
- Runtime adapters may add private implementation metadata outside the reusable
  framework, but must preserve these public fields when exchanging PEGO
  artifacts.
