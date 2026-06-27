# Recommendation Quality Loop

The recommendation quality loop evaluates whether PEGO's agents, council, and
information requests are improving the human's life instead of merely producing
plausible directives.

This loop is internal. The human should experience the result as a simpler,
more confident directive or one necessary question.

## Purpose

PEGO should learn from outcomes at three levels:

- Decision quality: whether the selected directive was a good decision for the
  human and context, not merely whether it was completed.
- Agent quality: whether each specialized agent made a useful recommendation.
- Council quality: whether the council selected, deferred, escalated, or
  requested information well.
- Information quality: whether questions asked of the human were worth the
  interruption and improved directive selection.

The goal is not to create more review bureaucracy. The goal is to make future
directives better, calmer, and more context-aware.

## Decision Quality Review

Every meaningful directive outcome should produce or update a decision quality
review.

The review should ask:

- Was the directive actionable?
- Did it fit the active goal and goal reconciliation?
- Did it respect constraints, protected time, authority, privacy, and risk?
- Was the human burden appropriate?
- Was the timing right?
- Did the explanation help enough to preserve or change future phrasing?
- Was follow-through more likely because PEGO shaped conditions well?
- Did the outcome improve, prove, or disprove the decision?
- Did PEGO learn enough to change agent weighting, council synthesis,
  information requests, or directive design?

Use `pego/templates/decision-quality-review.md`.

Structured runtimes should preserve reviews using:

```text
pego/schemas/decision-quality-review.schema.json
```

## Operating Principle

The system may deliberate deeply. The human should receive one calm directive,
one necessary question, or one stop condition.

PEGO should reduce anxiety by:

- Choosing one action.
- Explaining the reason briefly.
- Preserving deferrals.
- Asking fewer and better questions.
- Avoiding premature high-impact recommendations.
- Learning which agent judgments actually helped.

## Required Inputs

- Agent recommendations.
- Council decision.
- Command response.
- Directive outcome.
- Session review, if present.
- Current state at issue time.
- Current state after outcome.
- Human objection, blockage, or completion report.
- Governance notes.
- Known protected-time, privacy, and authority constraints.

## Agent Recommendation Review

After a directive outcome, review relevant agent recommendations.

The review should ask:

- Was the proposed directive useful?
- Did it fit time, energy, location, protected time, and authority?
- Did the agent correctly identify the main friction?
- Did the agent overstate confidence?
- Did the agent ask for too much or too little information?
- Did the recommendation reduce or increase human stress?
- Should the agent's future weighting, assumptions, or required inputs change?

Use `pego/templates/agent-recommendation-review.md`.

Structured runtimes should preserve reviews using:

```text
pego/schemas/agent-recommendation-review.schema.json
```

## Council Synthesis Review

Review council decisions separately from individual agent quality.

The council may fail even when an agent made a good recommendation. Examples:

- The council selected the wrong domain.
- The council deferred the action with the highest consequence of deferral.
- The council asked a question when it could have safely acted.
- The council acted when a question would have changed the directive.
- The council hid dissent to produce false clarity.
- The council produced a directive that increased anxiety or cognitive load.

Use `pego/templates/council-synthesis-review.md`.

Structured runtimes should preserve reviews using:

```text
pego/schemas/council-synthesis-review.schema.json
```

## Information Value Assessment

Before asking the human for more information, PEGO should assess whether the
question is worth the interruption.

Ask:

- Would the answer change the next directive?
- Which agent needs the information?
- What decision would be wrong without it?
- Can PEGO infer safely from existing private state?
- Is the question narrow enough to answer quickly?
- Does asking now reduce future stress, risk, or rework?
- Does the question request sensitive information before the privacy or
  authority boundary is clear?

If the answer would not change the next directive, do not ask. Make a safe
assumption and state it briefly when needed.

Use `pego/templates/information-value-assessment.md`.

Structured runtimes should preserve assessments using:

```text
pego/schemas/information-value-assessment.schema.json
```

## Review Timing

Run the loop when:

- A directive is completed, blocked, objected to, or partially completed.
- A recommendation was surprising, high-friction, or anxiety-producing.
- A council decision deferred a major domain.
- PEGO asked the human a question.
- A new pattern appears in outcomes.
- A directive succeeded or failed for reasons not predicted by the selected
  agent.

For low-risk routine directives, the loop may be lightweight. For repeated
failures, cross-domain conflict, or high-impact areas, preserve explicit review
artifacts.

## Human-Facing Constraint

The review loop should not leak into USER-mode output.

The human should not see:

- Agent scorecards.
- Internal weighting updates.
- Long council retrospectives.
- Every missed assumption.
- A list of all possible follow-up questions.

The human may see:

```text
State update: the prior directive was blocked by location.
Next directive: answer one location question before PEGO resynthesizes.
Reason: location changes which actions are feasible.
```

## Learning Outputs

The quality loop may produce:

- Context update candidates.
- Operating-register updates.
- Agent assumption changes.
- Council weighting notes.
- Better intake questions.
- Stop conditions.
- Governance escalation triggers.
- Directive candidate revisions.

Learning should be conservative. A single outcome can create a provisional
note, but durable changes should require repeated evidence unless the outcome
reveals safety, privacy, authority, or protected-time risk.

## Success Criteria

The loop is working when:

- Agents become more specialized and less generic.
- Council decisions improve from outcome evidence.
- PEGO asks fewer but higher-impact questions.
- Directives fit the human's actual time, energy, location, and constraints.
- Dissent is preserved internally without burdening the human.
- The human experiences less anxiety from next-action selection.
- Outcome reports visibly improve future directives.

## Failure Modes

Stop, downgrade, or revise if:

- PEGO keeps asking broad questions that do not change directives.
- One agent dominates without outcome evidence.
- Council synthesis hides dissent.
- Directives repeatedly fail for predictable situational reasons.
- The human receives plans instead of one next action.
- Review artifacts become productivity theater.
- The system interprets compliance with a directive as proof that the directive
  was good.
