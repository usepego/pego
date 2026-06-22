# Health Check-In Packet

Use this packet when PEGO needs targeted health state before issuing or revising health directives.

Structured implementations should emit `pego/schemas/health-check-in.schema.json`.

## Date

Date.

## Purpose

Why this check-in is needed.

## Measurement Rule

Ask for new health metrics only when they change a directive, risk classification, escalation, or strategy review.

## Questions

| Question | Signal | Decision Use | Required |
| --- | --- | --- | --- |
| Targeted question. | Sleep / food / hunger / movement / symptoms / metric / constraint. | What PEGO can decide from the answer. | Yes / No |

## Do Not Ask

- Broad self-help reflection.
- New biomarker tracking without a decision reason.
- Medical interpretation that requires clinician review.

## Privacy Status

Protected private instance.

## Next Step

Record answers under protected private health state or the current session log, then regenerate health candidates if the answers change directive selection.
