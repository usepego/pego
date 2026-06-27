# Runtime-Neutral Agent Infrastructure

Date: 2026-06-22

## Decision

PEGO will be designed as runtime-neutral agent infrastructure.

The framework defines constitutions, agent mandates, directive schemas,
governance checks, memory rules, privacy boundaries, operating loops, and runtime
adapter contracts. Runtime choices such as LangGraph, Vercel AI SDK, a custom
service, a mobile app, a Slack bot, or a local CLI are implementation choices.
They should not define PEGO itself.

## Rationale

PEGO's core novelty is not the hosting environment. It is the delegation of
personal executive governance to a coordinated, constitutionally bounded council
of agents.

Keeping the core runtime-neutral lets PEGO:

- Remain understandable as an open framework.
- Support multiple user experiences over time.
- Avoid premature vendor, language, or platform lock-in.
- Preserve privacy and governance rules across adapters.
- Let the founder instance evolve without forcing a product architecture too
  early.

## Consequences

- Framework docs should use runtime-neutral language.
- Runtime-specific tools belong in adapter layers.
- Local scripts under `ops/` are reference machinery, not the PEGO architecture.
- Future LangGraph, Vercel, mobile, Slack, CLI, or custom-service work should
  implement PEGO contracts rather than replace them.
- Runtime evaluation should wait until the contracts for directives, governance,
  memory, and agent coordination are stable enough to test across adapters.
