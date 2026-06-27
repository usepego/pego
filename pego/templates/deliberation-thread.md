# Deliberation Thread Template

Use this template when PEGO preserves an agent-to-agent deliberation before a
Council decision.

Structured runtimes should emit `pego/schemas/deliberation-thread.schema.json`.

## Thread

Short thread name.

## Decision Frame

The concrete directive, decision, behavior loop, tool call, or escalation being
deliberated.

## Initiating Agent

Agent that opened the thread.

## Participating Agents

Agents asked to provide positions, dissent, evidence, or review.

## Trigger

What caused the deliberation: user update, circumstance update, outcome,
strategy review, tool result, conflict, risk, or stale assumption.

## Messages

List of agent messages using `pego/templates/agent-message.md`.

## Open Questions

Decision-grade questions that still matter.

## Dissent Preserved

Strongest opposing positions.

## Evidence Gaps

Missing facts or weak assumptions.

## Proposed Council Input

What should be handed to Council for synthesis.

## Governance Notes

Authority, privacy, reversibility, protected-time, stakeholder, legal, medical,
tax, or financial concerns.

## Next Step

Continue deliberation / Send to Council / Ask targeted question / Run tool /
Escalate / Block.
