# Operating Memory Lifecycle

PEGO memory is governance material, not a passive transcript.

The system should remember what improves future directives and forget or
quarantine what is noisy, stale, unsafe, overly private, or not decision-grade.

## Memory Tiers

### Session Memory

Short-lived context used during a current operating session.

Examples:

- Current location class.
- Available time.
- Energy state.
- Current directive.
- Blockers reported today.

Session memory should normally expire after session closeout unless promoted by
review.

### Working Memory

Near-term context used across a day or week.

Examples:

- Active queue.
- Weekly priority.
- Open decision-grade questions.
- Known upcoming events.
- Temporary constraints.

Working memory should be reviewed during daily and weekly loops.

### Durable Private Memory

Stable or repeatedly useful private operating context.

Examples:

- Goals.
- Constitutional constraints.
- Stable preferences.
- Repeated behavior loops.
- Health, finance, career, home, relationship, and voice models.
- Strategy decisions.

Durable private memory must live in the protected private instance.

### Quarantined Memory

Potentially useful but unsafe or uncertain material.

Examples:

- Speculation.
- Sensitive third-party details.
- Employer-sensitive context.
- Health, legal, tax, or financial claims needing professional review.
- One-off mood states that may be mistaken for traits.

Quarantined memory should not affect directives until reviewed.

### Expired Memory

Context that is no longer true or no longer decision-useful.

Examples:

- Old schedule constraints.
- Completed event prep.
- Resolved blockers.
- Stale assumptions.

Expired memory should be removed from active operating context and retained only
if audit value justifies it.

## Promotion Rule

PEGO may promote memory only when the update is:

- Decision-relevant.
- Supported by enough evidence for its impact.
- Properly classified.
- Routed to a protected private destination.
- Reviewed for privacy and authority effects.
- Given a review date or expiry rule when appropriate.

Use `pego/templates/context-update.md` for individual update candidates.

Use `pego/templates/memory-lifecycle-review.md` when reviewing a batch of
session, outcome, or context evidence for promotion, quarantine, expiry, or
durable application.

Structured runtimes should preserve lifecycle reviews using:

```text
pego/schemas/memory-lifecycle-review.schema.json
```

## Memory Actions

- Record only.
- Promote to working memory.
- Promote to durable private memory.
- Quarantine pending review.
- Expire from active context.
- Correct or supersede prior memory.
- Reject.

## Evidence Rules

Evidence strength should scale with memory impact.

- Direct statement may update a preference.
- Repeated observed behavior may update a behavior loop.
- Directive outcomes may update strategy or friction models.
- Financial model output may update scenario assumptions, but not execution
  authority.
- Agent inference should stay provisional unless confirmed.
- Speculation should not become durable memory.

## Governance Triggers

Require governance review when a memory update:

- Changes authority.
- Changes protected time.
- Affects a protected stakeholder.
- Touches medical, legal, tax, financial, career, housing, or relationship risk.
- Involves credentials, account access, or third-party disclosure.
- Could expose private subject information outside the protected private
  instance.

## Anti-Patterns

PEGO must not:

- Treat chat history as durable truth.
- Treat one-off mood as stable identity.
- Use private facts in public framework files.
- Preserve unnecessary third-party details.
- Let stale assumptions silently drive directives.
- Use memory promotion to bypass adoption or governance review.

## Relationship To Existing Reviews

Outcome review decides what was learned from execution.

Context update records a proposed memory change.

Memory application review decides whether eligible context updates may be
applied to destination files.

Operating memory lifecycle defines the broader policy for promotion,
quarantine, expiry, correction, and use in directives.
