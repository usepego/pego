# Adoption Record Template

Use this template when PEGO needs an explicit audit trail for a recommendation
becoming a directive, being deferred, being escalated, or being blocked.

Structured runtimes should emit `pego/schemas/adoption-record.schema.json`.

## Record

Short name.

## Date

Date.

## Source Artifact

Agent recommendation, deliberation thread, council decision, tool result,
behavior loop, outcome review, or private fact that triggered adoption.

## Source Authority

Level 0 / Level 1 / Level 2 / Level 3 / Level 4 / Unknown.

## Proposed Adoption

Adopt as directive candidate / Adopt into queue / Adopt as command response /
Request information / Revise / Defer / Escalate / Block.

## Adopted Authority

Authority level after review.

## Governance Review

Preflight, compliance review, decision packet, or other review reference.

## Dissent Preserved

Strongest dissent or uncertainty.

## Evidence Quality

Direct telemetry / Financial model output / Human report / Repeated observed
pattern / Expert source / Agent inference / Speculation.

## Privacy Classification

Private-only / Safe to summarize / Requires explicit disclosure approval /
Blocked.

## Execution Permission

None / Manual human execution only / Tool execution permitted / Escalated.

## Conditions

Conditions required before the adopted action can proceed.

## Stop Conditions

What should stop or reverse the adoption?

## Outcome Review Required

When and how PEGO should review whether this adoption worked.
