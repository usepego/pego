# Tool Contract: governance.preflight

## Tool

`governance.preflight`

## Purpose

Classify a proposed directive before adoption or execution so PEGO can decide
whether it may proceed, needs review, must be escalated, or should be blocked.

## Owning Agents

Governance Agent, Operations Agent, Council.

## Inputs

- Proposed directive.
- Authority level.
- Domain.
- Risk categories.
- Privacy impact.
- Protected-time impact.
- Reversibility.
- Evidence quality.
- Known constraints.

## Outputs

- Preflight outcome.
- Review level.
- Required next step.
- Risk categories.
- Authority classification.
- Stop conditions.

## Authority Required

Level 0 observe for classification.

Level 4 escalate when a directive exceeds authority or risk limits.

## Operation Type

Escalate.

## Private Data Used

- Directive content.
- Relevant constraints, protected time, and private context needed to classify
  risk.

## Third-Party Disclosure

Local only by default.

## Write Locations

Protected governance preflight or review artifacts.

## Governance Review

This tool is a review gate. It does not grant execution authority by itself.

## Failure Mode

If classification is uncertain, PEGO should downgrade authority, ask one
decision-grade question, or escalate.

## Logging Rule

Log classification, evidence, and required next step. Do not log unnecessary
private details.

## Prohibited Uses

- Approving execution by implication.
- Hiding risk or dissent.
- Bypassing formal review for high-impact decisions.
