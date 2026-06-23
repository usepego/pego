# Intra-Day Command Loop

The intra-day command loop lets PEGO update and deliver directives during the
day when cadence, status, available time, energy, location, constraints,
completed work, or known events change.

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

## PEGO-Initiated Triggers

PEGO should initiate the loop when:

- A scheduled directive window opens.
- A meal decision is approaching.
- A prior directive should be complete.
- A known event requires lead-time preparation.
- Protected time is approaching.
- A blocker, missed directive, or stale context changes the queue.
- End-of-day closeout is due.

## Human Inputs

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

Structured runtimes should preserve command responses using:

```text
pego/schemas/command-response.schema.json
```

Use `pego/templates/intra-day-session-log.md` to preserve the state changes caused by the command.

The reference USER-mode runner is:

```text
ops/operator/user_check_in.py
```

It records the status update, calls the next-step selector, runs governance
preflight through that selector, and appends the result to a protected session
log. It is a local adapter for the protocol, not the PEGO runtime.

The response should include:

- State update.
- Next directive.
- Duration.
- Target behavior, when known.
- Environment design, when known.
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

When a selected directive has behavioral-strategy metadata, PEGO should preserve it in the response. The human should know not only what to do, but what action pattern and environmental condition the directive is meant to create.

Do not select a directive that requires missing information, unavailable tools, unsafe conditions, or higher authority than granted.

## Cadence

PEGO should not interrupt constantly by default.

Recommended interaction model:

- Morning: operating brief and initial queue.
- During day: human checks in after completion, blockage, or when asking what is next.
- Before protected time: PEGO stops expansion and preserves the boundary.
- End of day: outcome review.
- Session closeout: run `python3 pegoctl close-session` so completed
  directives, blockers, governance notes, and context-update candidates feed
  the next operating cycle.

Future versions may add automated nudges, but only after the constitution grants that authority.

## Governance

Intra-day resynthesis may reorder Level 1 and approved Level 2 directives.

It must not:

- Escalate authority silently.
- Add high-impact directives without review.
- Consume protected time.
- Convert a deferred candidate into execution authority.
- Ignore a human objection.
