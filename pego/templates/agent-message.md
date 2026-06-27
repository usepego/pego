# Agent Message Template

Use this template when one PEGO agent sends a message to another agent during
deliberation.

Structured runtimes should emit `pego/schemas/agent-message.schema.json`.

## Message

Short message title.

## From Agent

Agent sending the message.

## To Agent

Agent receiving the message.

## Message Type

Request position / Provide position / Challenge assumption / Request evidence /
Request governance review / Handoff / Dissent / Tool result summary / Final
position.

## Decision Frame

The concrete directive, decision, loop, tool call, or escalation being discussed.

## Claim

The agent's main claim or request.

## Evidence

Facts, private-state references, tool outputs, outcomes, or assumptions used.

Do not copy private facts into public framework examples.

## Confidence

High / Medium / Low / Unknown.

## Authority Implication

Level 0 / Level 1 / Level 2 / Level 3 / Level 4 / Unknown.

## Privacy Impact

Private-only / Safe to summarize / Requires explicit disclosure approval.

## Requested Response

What should the receiving agent return?

## Stop or Escalation Condition

What should stop the thread or trigger Governance/Council escalation?
