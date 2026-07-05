# Agent Infrastructure

PEGO is agent infrastructure for governing human activity toward predicted
outcomes.

It is not primarily a Python app, a web app, a chatbot, a habit tracker, or a
single automation workflow. Those can all become runtime surfaces. PEGO itself
is the framework that defines how agents reason, govern, coordinate, issue
directives, protect privacy, and learn from outcomes.

## Runtime Boundary

The runtime can later be a graph orchestrator, hosted agent service, custom
service, mobile app, messaging surface, local CLI, or another environment.
Those are hosting and surface choices, not PEGO itself.

PEGO should remain portable across runtimes by defining stable contracts for:

- Agent roles and mandates.
- Agent-to-agent deliberation and dissent.
- Tool contracts for bounded capabilities agents may call.
- Constitutions and authority levels.
- Directive candidates and synthesized directives.
- Governance review and escalation.
- Memory, context updates, and outcome reviews.
- Runtime-neutral artifact schemas for agent output, directive candidates,
  compliance review, and outcome records.
- Privacy boundaries between reusable framework material and protected private
  instance data.
- Runtime adapters that can read and write PEGO-compatible artifacts.
- Runtime adapters that preserve the PEGO lifecycle from intake through outcome
  learning.

## Product Shape

A user should experience PEGO as a governing system that decides what should
happen next within explicit authority limits. The interface may be conversational,
scheduled, ambient, mobile, or CLI-based, but the core experience is the same:

- PEGO understands the subject's values, resources, environment, constraints,
  goals, and current state.
- Domain agents produce recommendations or directive candidates.
- Governance evaluates quality, risk, alignment, privacy, reversibility, and
  authority.
- Operations synthesizes competing directives into a coherent next action or
  plan.
- Outcomes update the operating memory and alter future directives.

## Engineering Rule

Framework files should describe PEGO in runtime-neutral language. Runtime-specific
code belongs in adapter layers and must not define the conceptual architecture.

PEGO's core behavior should remain prompt/protocol-based agent governance:
domain agents deliberate, governance constrains authority, operations synthesize
directives, reviews learn from outcomes, and strategic reviews adjust future
behavior. Code may support that lifecycle, but it should not replace the
agent-governance model as the source of product behavior.

Python and other scripts are appropriate for CI, repository validation,
scaffolding, linting, migration, privacy checks, template generation, and local
developer workflows. They can help build and maintain PEGO.

Continuous integration should validate PEGO's framework invariants: public files
exist, private data is not tracked, registry paths are valid, operation scripts
compile, and smoke tests can run without protected private instance contents.

Reference scripts under `ops/` are allowed when they make the framework usable
locally, but they are support tooling or examples of one runtime adapter. They
should not imply that PEGO is a Python application or that future users must
operate PEGO through the same tooling.

When a script encodes reusable PEGO behavior, the behavior should also be
captured in public-safe protocols, templates, schemas, or tool contracts so a
pure prompt-agent runtime or another adapter can implement the same contract.

## Adapter Contract

A runtime adapter should be able to:

- Load a protected private operating brief.
- Load the relevant public agent protocols and governance rules.
- Allow agents to call declared tools within granted authority.
- Produce structured agent recommendations or directive candidates that conform
  to public PEGO schemas.
- Run governance preflight before adoption or execution.
- Write private outputs only to the protected private instance.
- Preserve dissent, uncertainty, evidence level, review dates, and stop
  conditions.
- Expose a clear user-facing command surface such as "what is next?",
  "resynthesize", "record outcome", "update context", or "review goals".
- Declare capabilities with a runtime adapter manifest before being treated as
  a complete PEGO runtime.

Adapters may differ in execution model, storage, UI, scheduling, and model
provider. They should not differ in constitutional authority or privacy rules.

See `pego/architecture/runtime-adapter-lifecycle.md` for the required lifecycle.
See `pego/architecture/tool-contracts.md` for how agents call tools without
making any one tool implementation the PEGO runtime.
