# Recommendation Adoption Lifecycle

PEGO must distinguish recommendation, directive, and execution.

An agent recommendation is not automatically a directive. A directive is not
automatically execution authority. Execution authority exists only when the
private constitution, governance review, and tool permissions explicitly grant
it.

## Purpose

This lifecycle prevents agent outputs, tool results, council decisions, or queue
items from silently becoming stronger than their approved authority.

It applies when PEGO converts:

- Private facts into recommendations.
- Agent recommendations into directive candidates.
- Council decisions into directive candidates.
- Directive candidates into queues.
- Queue selections into command responses.
- Command responses into actions or tool execution.
- Outcomes into future memory or revised directives.

## Lifecycle States

### 1. Observation

Facts, telemetry, status updates, tool outputs, behavior loops, and outcomes are
observed.

Authority: Level 0.

Output examples:

- Context update.
- Tool result summary.
- Outcome record.
- Behavior loop record.

### 2. Recommendation

A domain agent proposes, dissents, requests information, or escalates.

Authority: Level 1 unless the private constitution grants more.

Output:

```text
pego/templates/agent-recommendation.md
```

### 3. Deliberation

Agents exchange positions, challenge assumptions, summarize tool results, or
handoff risks before Council synthesis.

Authority: deliberation only.

Outputs:

```text
pego/templates/agent-message.md
pego/templates/deliberation-thread.md
```

### 4. Council Decision

Council reconciles recommendations into adopt, revise, request information,
escalate, or block.

Authority: no automatic increase.

Output:

```text
pego/templates/council-decision.md
```

### 5. Directive Candidate

An adopted recommendation, information request, or revision request becomes a
candidate that can be compared, scheduled, deferred, or escalated.

Authority: preserved from source unless governance explicitly changes it.

Output:

```text
pego/templates/directive-candidate.md
```

### 6. Governance Preflight Or Review

Before adoption into the active queue or command response, PEGO evaluates
authority, privacy, risk, evidence, reversibility, protected time, stakeholder
impact, and constraints.

Outputs:

```text
pego/schemas/directive-preflight.schema.json
pego/templates/compliance-review.md
pego/templates/decision-packet.md
```

### 7. Adopted Directive

A reviewed candidate may become a directive if it fits the current operating
context.

Authority: Level 1 recommend or Level 2 direct unless explicitly reviewed
otherwise.

Outputs:

```text
pego/templates/directive-queue.md
pego/templates/command-response.md
```

### 8. Execution

Execution occurs only if the private constitution grants Level 3 authority for
the specific action and tool, and governance review confirms the action fits.

High-impact actions remain Level 4 escalations until formal review is complete.

### 9. Outcome And Learning

After the human or tool attempts the directive, PEGO records evidence and
decides whether to keep, revise, recur, defer, escalate, or remove the pattern.

Outputs:

```text
pego/templates/directive-outcome.md
pego/templates/outcome-review.md
```

## Adoption Record

When a runtime needs an explicit audit trail, use
`pego/templates/adoption-record.md`.

Structured runtimes should preserve adoption records using:

```text
pego/schemas/adoption-record.schema.json
```

## Adoption Rules

1. Preserve source authority.
2. Preserve dissent.
3. Preserve evidence quality.
4. Preserve privacy classification.
5. Do not increase authority through synthesis.
6. Do not hide escalation inside a daily directive.
7. Do not execute without tool-specific permission.
8. Ask one decision-grade question when missing information changes adoption.
9. Prefer the smallest reversible action when evidence is weak.
10. Record outcomes so future adoption decisions learn from reality.

## Blockers

Block adoption when:

- Authority is missing.
- Privacy risk is unresolved.
- Evidence is too weak for the proposed risk.
- Protected time would be consumed without override.
- Stakeholder impact is unreviewed.
- The action requires financial, medical, legal, tax, career, housing, or
  relationship-impacting execution without formal review.
- The directive depends on credentials, account access, or third-party
  disclosure not explicitly approved.
