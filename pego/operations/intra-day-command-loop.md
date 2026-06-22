# Intra-Day Command Loop

The intra-day command loop lets PEGO update directives during the day when the human reports status, available time, energy, location, constraints, or completed work.

The daily loop sets the operating frame. The intra-day loop selects the next directive from the live queue.

Use `pego/operations/operator-interface.md` for the human-facing command protocol.

## Purpose

The command loop should answer:

- What changed?
- What is now available?
- What has been completed?
- What remains in the directive queue?
- What is the next directive?
- What should be deferred, revised, or escalated?

## User Inputs

The human may report:

- Completed directive.
- Partially completed directive.
- Blocked directive.
- Available time.
- Current location.
- Current energy.
- Weather or environmental condition.
- New obligation.
- New concern or objection.
- Request for next directive.

Examples:

- `Breakfast done. What's next?`
- `I have 45 minutes before a meeting.`
- `It is raining.`
- `I am low energy.`
- `The garden block is done.`
- `I cannot do venture work now.`

## Required State

Before selecting the next directive, PEGO should check:

- Active operating brief.
- Current daily directive or synthesized day plan.
- Directive queue.
- Completed directives.
- Deferred directives.
- Protected time.
- Current time, if known.
- Available time, if supplied.
- Energy and location, if supplied.
- Governance constraints.
- Intra-day session log, if one exists.

## Steps

1. Parse the status update.
2. Record any completed, partial, blocked, or canceled directive.
3. Update the intra-day session log using `pego/templates/intra-day-session-log.md`.
4. Update the directive queue.
5. Remove candidates that no longer fit the day.
6. Re-rank remaining candidates by priority, timing, energy, location, and consequence of deferral.
7. Select one next directive.
8. Provide a fallback if the selected directive becomes blocked.
9. State what is deferred.
10. State the next check-in condition.

## Output Shape

Use `pego/templates/command-response.md`.

Use `pego/templates/intra-day-session-log.md` to preserve the state changes caused by the command.

The response should include:

- State update.
- Next directive.
- Duration.
- Why this directive now.
- Fallback.
- Deferred candidates.
- Stop condition.
- Next check-in.

## Directive Selection Rules

Prefer the candidate that:

- Fits the available time.
- Fits the current location.
- Fits the current energy level.
- Does not violate protected time.
- Has the highest consequence of deferral.
- Advances an active strategy.
- Produces evidence for future decisions.
- Can be completed cleanly.

Do not select a directive that requires missing information, unavailable tools, unsafe conditions, or higher authority than granted.

## Cadence

PEGO should not interrupt constantly by default.

Recommended interaction model:

- Morning: operating brief and initial queue.
- During day: human checks in after completion, blockage, or when asking what is next.
- Before protected time: PEGO stops expansion and preserves the boundary.
- End of day: outcome review.

Future versions may add automated nudges, but only after the constitution grants that authority.

## Governance

Intra-day resynthesis may reorder Level 1 and approved Level 2 directives.

It must not:

- Escalate authority silently.
- Add high-impact directives without review.
- Consume protected time.
- Convert a deferred candidate into execution authority.
- Ignore a human objection.
