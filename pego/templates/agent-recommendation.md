# Agent Recommendation Template

Use this template when any PEGO agent proposes, revises, or dissents from a directive.

## Agent

Agent name and domain.

## Recommendation Type

Recommend / Direct / Dissent / Request more information / Escalate.

## Proposed Directive

The concrete action or decision the agent wants PEGO to adopt.

This should be small enough to evaluate. If the recommendation is broad, break it into a strategy plus the next executable directive.

## Authority Level

Level 0 / Level 1 / Level 2 / Level 3 / Level 4.

## Relevant Facts

Facts used by the agent.

Do not include private facts in reusable public framework files.

## Assumptions

Assumptions the agent is making.

Mark uncertain assumptions clearly.

## Evidence Quality

Direct telemetry / Financial model output / Human report / Repeated observed pattern / Expert source / Agent inference / Speculation.

## Expected Benefit

What improves if this recommendation is followed?

## Behavior Loop

If this recommendation is responding to a recurring loop, identify the trigger,
routine, reward or relief, strategic effect, and proposed replacement frame.

Use `pego/templates/behavior-loop.md` when the loop should become durable
operating memory.

## Costs and Tradeoffs

What does this consume, delay, risk, or make harder?

## Risks

Financial / Health / Relationship / Career / Legal / Tax / Privacy / Reputation / Time / Energy / Psychological / Opportunity cost.

## Reversibility

Easy to reverse / Reversible with cost / Hard to reverse / Irreversible.

## Privacy Impact

Private-only / Safe to summarize / Requires explicit disclosure approval.

## Required Handoffs

Which agents or governance layers must review this before adoption?

## Dissent

What would the strongest opposing agent say?

## Stop Conditions

What should cause PEGO to stop, revise, or escalate?

## Review Date or Success Criteria

When should this be reviewed, or what outcome proves it worked?

After outcome evidence is available, evaluate the recommendation with
`pego/templates/agent-recommendation-review.md` and
`pego/operations/recommendation-quality-loop.md`.
