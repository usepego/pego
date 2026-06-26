# First Run Procedure

This procedure starts a PEGO operating session from the repository root.

Use it when an agent or human opens the repository and needs to move from static files to active operation.

The preferred human entry point is conversational:

```text
Start PEGO.
```

or:

```text
What should I do next?
```

The agent or runtime adapter should perform the local checks and setup steps.
Do not require the USER-mode human to look up command syntax unless they ask for
Engineering-mode details.

The agent or runtime adapter must not expose the setup steps as the experience.
Repository hygiene checks, readiness checks, bootstrap actions, private-file
updates, diffs, and internal plans are adapter work. The user-facing result must
be one operating response.

Use `pego/operations/start-pego.md` as the human-facing entry protocol.

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

Agent-side check:

```sh
python3 pegoctl doctor
```

If the doctor fails, fix repository hygiene before operating PEGO.

Doctor passing only proves the framework structure. It does not mean the
protected private instance is initialized.

For a fresh checkout or a private instance with many missing readiness checks,
the agent should create the private skeleton:

```sh
python3 pegoctl bootstrap
```

Bootstrap should be safe by default: it creates missing private paths and skips
existing files unless `--force` is explicitly supplied.

### 1.5. Check Operating Readiness

Agent-side guided status:

```sh
python3 pegoctl guide
```

It reports safe operating status and the recommended next command without
printing private contents.

If readiness reports `ready_with_assumptions`, inspect whether the missing
checks are core state or generated operating paths:

- Missing core state such as constitution, current state, person profile,
  protected time, or operating register means PEGO should generate the relevant
  intake packet before governing USER-mode directives.
- Missing generated paths such as food options, meal decisions, operator
  briefs, session reviews, context promotions, or application reviews usually
  means `pegoctl bootstrap` should be run or rerun.

Use:

```text
pego/operations/operating-readiness.md
```

If PEGO is not ready, issue the smallest setup directive that makes operation possible.

For a new user without enough private operating state, generate one first-run
intake packet rather than asking for the full constitution at once:

```sh
python3 pegoctl intake --phase boundary
```

Use `pego/ux/first-run-experience.md` to choose the next intake phase.

For net-new users or domains that lack enough context for agent
recommendations, use:

```text
pego/operations/domain-baseline-bootstrap.md
```

Generate the smallest relevant baseline intake packet, such as:

```sh
python3 pegoctl intake --phase finance-baseline
python3 pegoctl intake --phase career-baseline
python3 pegoctl intake --phase health
python3 pegoctl intake --phase home-baseline
```

After enough domain baselines exist, reconcile the active goals before Council
claims it has selected the best cross-domain directive:

```sh
python3 pegoctl reconcile-goals
```

Use `pego/operations/goal-reconciliation.md` to decide whether Council has
enough priority context, should ask one targeted priority question, or must use
a conservative temporary priority assumption.

If the generated reconciliation reports missing baselines, ask the smallest
listed targeted question or generate the relevant `goal-reconciliation` intake
packet. Do not ask the human to rank every life goal.

Do not treat readiness as proof that onboarding is complete.

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

To generate a protected operating brief from the current queue and session:

```sh
python3 pegoctl brief
```

To create daily or weekly operating artifacts through the installed command
surface:

```sh
python3 pegoctl daily health-check-in
python3 pegoctl weekly
python3 pegoctl monthly
```

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

If the first run needs setup or resynthesis, do that before responding. Then
return only the operating response:

- A brief state update.
- One next directive or one targeted missing-fact question.
- Time box and start condition when applicable.
- Reason selected.
- Fallback.
- Stop condition.
- Next check-in.

Do not include patch output, file changes, command transcripts, or agent
planning text in the USER-mode reply.

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
