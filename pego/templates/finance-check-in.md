# Finance Check-In Packet

Use this packet when PEGO needs targeted finance state before issuing or revising finance, career, venture, spending, runway, or lifestyle directives.

Structured implementations should emit `pego/schemas/finance-check-in.schema.json`.

## Date

Date.

## Purpose

Why this finance check-in is needed.

## Privacy Rule

Ask for private financial values only inside the protected private instance, and only when the answer changes a directive, scenario, governance gate, or strategy review.

## Questions

| Question | Signal | Decision Use | Required |
| --- | --- | --- | --- |
| Targeted question. | Assumption / spending / runway / income / account-data / tax / decision / risk. | What PEGO can decide from the answer. | Yes / No |

## Do Not Ask

- Broad money reflection.
- Account balances or holdings unless the protected private destination is clear.
- Trade, transfer, or allocation instructions without governance review.
- Public or third-party disclosure of private financial facts.

## Privacy Status

Protected private instance.

## Next Step

Record answers under protected private finance state or the current session log, then rerun scenario generation or scenario review if the answers change assumptions, runway, risk, or directive selection.
