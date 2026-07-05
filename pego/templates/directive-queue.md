# Directive Queue Template

Use this template to maintain the live queue for a day or work session.

The queue is not a backlog. It is the active set of candidates that PEGO may select from during intra-day command cycles.

Structured runtimes should preserve the public schema at:

```text
pego/schemas/directive-queue.schema.json
```

## Date or Session

Date or session name.

## Operating Frame

Current daily thesis, weekly priority, or active operating mode.

## Protected Time

Time and commitments unavailable for directives.

## Current State

- Time:
- Location:
- Energy:
- Weather/environment:
- Active obligations:
- Known constraints:

## Completed

| Time | Directive | Outcome |
| --- | --- | --- |
| TBD | TBD | TBD |

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Scoring Model

Model: `directive-scoring-v1`. Score range is 0-3 per dimension before weighting. Governance deferral remains a hard gate before selection.

| Dimension | Weight | Description |
| --- | --- | --- |
| goal contribution | 3 | Contribution to a stated domain goal, non-negotiable, or operating priority. |
| urgency | 3 | Timing pressure from deadline, lead time, or current operating window. |
| consequence of deferral | 3 | Expected downside if the candidate waits until a later synthesis. |
| energy fit | 1 | Fit between required energy and supplied or assumed current energy. |
| reversibility | 2 | Preference for low-commitment, reversible actions. |
| downside protection | 2 | Protection against avoidable deterioration, friction, or future interruption. |
| anxiety reduction | 2 | Reduction of ambiguity, cognitive load, open loops, or future scrambling. |
| evidence value | 2 | Value of producing decision-grade information when evidence is weak. |
| environment leverage | 1 | Ability to reshape future behavior through context or setup. |

Safe tie-break order: lower authority, lower protected-time impact, lower required energy, shorter duration, then information-gathering or environment-shaping work when evidence is weak.

## Scorecards

| Scope | Candidate | Score | Selection Rationale | Deferral Reason |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## Behavioral Strategy

| Rank | Candidate | Target Behavior | Environment Design |
| --- | --- | --- | --- |
| 1 | TBD | TBD | TBD |

## Deferred

| Candidate | Reason Deferred | Next Review |
| --- | --- | --- |
| TBD | TBD | TBD |

## Blocked

| Candidate | Blocker | Required Change |
| --- | --- | --- |
| TBD | TBD | TBD |

## Next Directive

The next directive selected by the intra-day command loop.

## Next Check-In

When PEGO should be asked again or when the queue should be reviewed.
