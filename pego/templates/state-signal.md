# State Signal

Use this template when PEGO records protected evidence about the human's
current state, behavior, activity, environment, or progress.

State signals are the normalized input layer for text check-ins, directive
outcomes, wearable activity, calendar availability, bank account activity,
device sensors, app usage, documents, external APIs, and agent observations.

Structured runtimes should emit `pego/schemas/state-signal.schema.json`.

## Date

Date.

## Observed At

When the signal happened or was measured.

## Source Type

Manual text / Directive outcome / Wearable activity / Calendar / Bank account
activity / Device sensor / App usage / Location / Document / Agent observation
/ External API / Other.

## Ingestion Mode

Manual / Import / Polling / Webhook / Adapter / Agent inference.

## Domain

Finance / Health / Career / Venture / Home and Environment / Relationships /
Exploration / Happiness / Operations / Governance / Communications.

## Owning Agent

Which agent is responsible for interpreting the signal.

## Signal Type

Current state / Behavior observed / Activity / Sleep / Recovery / Nutrition /
Spending / Income / Account balance / Transaction pattern / Calendar
availability / Location context / Environment / Mood / Energy / Goal progress /
Risk / Blocker / Other.

## Summary

Decision-relevant summary. Do not paste raw private account records, health
telemetry, location trails, message contents, or credentials.

## Measurements

| Name | Value | Unit | Window | Directionality |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | Higher is better / Lower is better / Target range / Context only / Unknown |

## Affected Goals

Goals this signal may inform.

## Evidence Strength

Direct telemetry / Bank account activity / Human report / Observed behavior /
Directive outcome / External API / Agent inference / Speculation.

## Confidence

High / Medium / Low.

## Privacy Class

Protected private / Sensitive financial / Sensitive health / Safe to summarize.

## Raw Source Reference

Private local file, external provider reference, or adapter identifier. This
should be a pointer, not raw data.

## Raw Data Retention

Not stored / Private local / External provider / Unknown.

## Governance Notes

Authority, privacy, consent, retention, or review implications.

## Review After

When this signal should be reviewed.

## Expires After

When this signal should stop influencing current-state decisions by default.
