# Operating Readiness

Operating readiness is the preflight check before PEGO issues directives.

Use it to determine whether the system has enough current state, queue state, governance context, and outcome destination to operate safely.

## Local Checker

Reference local checker:

```sh
python3 ops/private/check_readiness.py
```

It reports path presence and safe readiness status only. It must not print
private operating contents.

Private storage should also pass backup-readiness review:

```sh
python3 ops/private/check_storage.py
```

## Readiness Decision

Return one of:

- Ready.
- Ready with assumptions.
- Not ready: missing state.
- Not ready: governance issue.
- Not ready: privacy issue.

## Public Framework Checks

- `python3 ops/pego_doctor.py` passes.
- `AGENTS.md` exists.
- `pego/operations/first-run.md` exists.
- `pego/operations/runtime-agent-protocol.md` exists.
- `pego/operations/operator-interface.md` exists.
- `pego/operations/intra-day-command-loop.md` exists.
- `pego/templates/command-response.md` exists.
- `pego/templates/directive-queue.md` exists.
- `pego/templates/directive-outcome.md` exists.

## Private Instance Checks

For active operation, confirm:

- Current session pointer exists.
- Active operating brief exists.
- Active queue exists or can be generated.
- Session log exists or can be generated.
- Outcome record location exists or can be generated.
- Governance constraints are known.
- Private storage backup is confirmed or explicitly accepted as an infrastructure risk.

Private files should remain under protected `private/` paths.

## Queue Checks

An active queue should contain:

- Operating frame.
- Protected time.
- Current state fields.
- Completed directives.
- Active candidates.
- Deferred candidates.
- Blocked candidates.
- Selection rules.
- Next check-in condition.

## Governance Checks

Before issuing a directive, confirm:

- Authority level.
- Privacy impact.
- Protected-time impact.
- Stakeholder impact.
- Whether the action is reversible.
- Whether formal review is required.

If authority is unclear, assume Level 1: Recommend.

## Operator Checks

Before responding, confirm:

- The user asked for operation, not strategy discussion.
- The output should be one directive unless asked otherwise.
- Missing context does not materially change the selected directive.
- The response uses operating language.

## Not-Ready Handling

If PEGO is not ready:

1. State the missing or unsafe condition.
2. Do not issue a directive that depends on it.
3. Issue the smallest setup directive that makes operation possible.

Examples:

- Create current queue.
- Create session log.
- Ask for available time.
- Ask for current location.
- Run governance review.
- Stop because protected time is at risk.

## Output

Use this shape:

```text
Readiness:

Missing state:

Assumptions:

Governance constraints:

Ready next action:

Stop condition:
```
