# USER-Mode Simulation Review

This review defines how to evaluate PEGO by pretending to be a normal human
using the system, while keeping the simulation public-safe.

## Purpose

PEGO should feel like a working personal executive governance system, not a set
of repository tools. A simulation should test whether the user experiences:

- Targeted questions about goals, circumstance, constraints, and authority.
- Domain agents forming recommendations from the user's state.
- Council reconciliation into one next directive.
- Governance checks before high-impact action.
- Outcome capture that changes future directives.

## Simulation Method

Use a disposable protected private root, not the real private instance:

```sh
python3 pegoctl --private-root /private/tmp/pego-sim bootstrap
python3 pegoctl --private-root /private/tmp/pego-sim check-in "Start PEGO. Available: 30 minutes. Energy: medium. Location: computer."
```

The command output is adapter telemetry. It is useful for engineering review
but must not be treated as the user experience. The user-facing artifact is the
command response written under the simulated private root.

## Current Findings

The framework promise is strong:

- Public positioning describes PEGO as agent infrastructure for governed
  directives.
- Domain-agent protocols exist.
- Council synthesis exists as a reusable protocol and local runner.
- Governance, authority, privacy, and directive schemas exist.

The current first-run experience is not yet fully aligned:

- The normal path can expose adapter mechanics unless a runtime facade hides
  them.
- Fresh private instances do not yet ask enough domain-specific questions to
  let Finance, Career, Venture, Health, Relationships, Home, Exploration, and
  Happiness form meaningful recommendations.
- The council runner can synthesize existing recommendations, but the onboarding
  loop does not yet produce those recommendations from user answers.
- The directive selector mostly chooses from an existing queue. It does not yet
  make the council visibly negotiate across domain pressures during first use.
- The public site promises goal-to-agent-to-council-to-directive, but the
  reference adapter still feels closer to intake-to-queue-to-next-step.

## Required Experience Spine

The first usable PEGO experience should follow this spine:

1. Boundary: establish privacy, authority, protected time, and stop rules.
2. Aim: ask what future state matters and what should be preserved.
3. Current circumstance: collect time, energy, location, next hard stop, and
   immediate pressure.
4. Domain scan: ask one compact cross-domain question set that gives each
   relevant agent enough state to form a first recommendation.
5. Agent recommendations: create structured recommendations or requests for
   missing information.
6. Council synthesis: reconcile recommendations into one directive, one
   targeted question, or one escalation.
7. Command response: show only the selected question or directive.
8. Outcome capture: record completion, blockage, objection, or changed
   circumstance.
9. Memory application: promote useful outcomes into durable private context
   after review.

## First Domain Scan

After the boundary is clear, PEGO should ask a compact question that exposes
the council model without overwhelming the user:

```text
What is the main pressure PEGO should govern first: health/energy,
money/runway, career/work, venture creation, home, relationships, exploration,
or something else? Include what is true now, what must not be disturbed, and
the next hard stop.
```

If the answer is broad, PEGO should ask one follow-up tied to the highest-risk
or highest-leverage domain, not a full questionnaire.

## Implementation Steps

1. Build a USER-mode facade command that prints only the command response, not
   adapter summaries or file paths.
2. Add natural-language state extraction for available time, energy, location,
   completion, blockage, hard stop, and domain pressure.
3. Add first-run domain scan packets that map user answers into initial
   private-state destinations.
4. Add a recommendation generator that converts domain scan answers into
   structured agent recommendations.
5. Route first-run recommendations through council synthesis before creating a
   directive candidate.
6. Convert council decisions into directive candidates and synthesize the first
   queue.
7. Make the public `usepego` positioning show the same lifecycle the runtime
   actually performs.
8. Add simulation tests that assert no adapter telemetry appears in USER-mode
   output and that first-run produces either a domain-specific question or a
   council-derived directive.

## Acceptance Criteria

A simulated new user who says `Start PEGO.` should not see setup output. They
should see one of:

- A boundary question.
- A current-circumstance question.
- A domain-pressure question.
- A council-derived directive.
- A governance stop or escalation.

Within the first few exchanges, the user should be able to see why PEGO is not
just a chat assistant: domain agents should have positions, the council should
select, defer, or escalate, and the response should remain executable.
