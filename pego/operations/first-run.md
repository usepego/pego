# First Run Procedure

This procedure starts a PEGO operating session from the repository root.

Use it when an agent or human opens the repository and needs to move from static files to active operation.

## Purpose

First run should establish:

- Runtime role.
- Private operating state.
- Active queue.
- Current constraints.
- First directive or required review.
- Outcome capture location.

## Procedure

### 1. Verify Repository Hygiene

Run:

```sh
python3 pegoctl doctor
```

If the doctor fails, fix repository hygiene before operating PEGO.

### 1.5. Check Operating Readiness

Use:

```text
pego/operations/operating-readiness.md
```

If PEGO is not ready, issue the smallest setup directive that makes operation possible.

For a new user without enough private operating state, generate one first-run intake packet rather than asking for the full constitution at once:

```sh
python3 ops/onboarding/generate_intake.py --phase boundary
```

Use `pego/ux/first-run-experience.md` to choose the next intake phase.

### 2. Select Runtime Role

Read:

```text
pego/operations/runtime-agent-protocol.md
```

Default role is Operator unless the request requires Council, Governance, or a Domain Agent.

### 3. Read Private Session State

If operating a private instance, read:

```text
private/operator/sessions/session-start.md
private/operator/quickstart.md
private/active-operating-brief.md
```

If any file is missing, proceed from available state and state the assumption.

### 4. Load Active Queue

Read the current directive queue from the active operating brief.

If no current queue exists:

1. Read the current daily directive or synthesized day plan.
2. Convert selected directives into `pego/templates/directive-queue.md`.
3. Keep the queue under protected `private/` paths.

### 5. Confirm Constraints

Before selecting a directive, check:

- Protected time.
- Authority level.
- Privacy constraints.
- Current time, if known.
- Available time, if supplied.
- Energy and location, if supplied.
- Known blockers.

### 6. Return First Directive

Use:

```text
pego/templates/command-response.md
```

Return one directive unless the user asks for a plan, discussion, queue, review, or strategy.

For local operation, the reference runner is:

```sh
python3 pegoctl next --date YYYY-MM-DD --available 30 --energy medium --location computer
```

It writes the command response and governance preflight output to protected private paths.

For active USER mode, prefer:

```sh
python3 pegoctl check-in "Done: prior directive. Available: 30 minutes. What's next?"
```

This appends the interaction to the protected intra-day session log as well as
writing the command response and preflight output.

### 7. Record Session State

Use:

```text
pego/templates/intra-day-session-log.md
```

Record:

- Input.
- State change.
- Response.
- Outcome if known.

### 8. Record Outcomes

At the end of a directive, session, or day, use:

```text
pego/templates/directive-outcome.md
```

Outcome records become evidence for future directives.

## Stop Conditions

Stop or escalate if:

- Authority is unclear above Level 1.
- A directive would affect protected time.
- A directive would expose private information.
- A directive would create financial, medical, legal, tax, career, relationship, housing, or hard-to-reverse consequences.
- The user raises an objection.
- Required private state is too stale to choose safely.

## Output Discipline

Operational response only:

- State update.
- Next directive.
- Time box.
- Start condition.
- Reason.
- Fallback.
- Deferred.
- Stop condition.
- Next check-in.
