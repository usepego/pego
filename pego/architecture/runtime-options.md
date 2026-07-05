# Runtime Options

PEGO should keep runtime choices open until the framework contracts are stable.
The first architectural commitment is runtime neutrality.

## Evaluation Criteria

Evaluate any runtime by asking:

- Can it run long-lived, stateful agent work?
- Can it preserve private memory without leaking protected subject data?
- Can it support human-in-the-loop governance and explicit approval gates?
- Can it schedule, resume, retry, and audit agent work?
- Can it expose a good user experience for directives throughout the day?
- Can it keep PEGO artifacts portable and understandable to engineers?
- Can it avoid locking PEGO's concepts into one vendor, language, or UI?

## Current Local Adapter

The current repository uses markdown protocols, templates, private instance
files, and small local scripts as a reference adapter. This is useful for early
design because it keeps PEGO inspectable, versioned, and private.

This adapter is not the long-term product architecture by itself.

Python is acceptable and useful as engineering infrastructure: CI checks,
privacy validation, repository hygiene, scaffolding, data migrations, tests, and
local developer utilities. The constraint is conceptual, not anti-Python: PEGO's
runtime model should not be defined as "a Python app" unless a future runtime
decision explicitly says so.

Core PEGO behavior should remain prompt/protocol-based agent governance. Python
may provide reference runners and local adapters, but the governing behavior
must be expressible through public-safe agent protocols, templates, schemas, and
tool contracts so another runtime can implement the same PEGO lifecycle.

## Stateful Agent Orchestrator

A stateful agent orchestrator is a plausible runtime category for PEGO because
PEGO needs long-running agent work, persistence, human-in-the-loop flows,
durable execution, and resumability.

LangGraph is one plausible example in this category because it is designed for
long-running, stateful agents, persistence, human-in-the-loop flows, durable
execution, and streaming.

Potential fit:

- Stateful multi-agent orchestration.
- Durable execution and resumability.
- Explicit graph structure for governance gates.
- Human review points before high-impact actions.

Potential concerns:

- Added framework complexity.
- Possible language, vendor, or ecosystem gravity.
- Need to verify privacy, deployment, and local-first options before using it
  for sensitive personal data.

## Hosted Product Interface Layer

A hosted product interface layer is a plausible surface for PEGO, especially
for web, mobile-web, streaming responses, model/provider routing, tool calls,
and polished user experiences.

Vercel AI SDK and AI Cloud are plausible examples in this category for web and
mobile-web product surfaces, model/provider routing, tool calling, and polished
streaming experiences.

Potential fit:

- Web and mobile-facing PEGO interfaces.
- Streaming directive sessions.
- Tool calling and provider abstraction.
- Fast product iteration if PEGO becomes a general-user product.

Potential concerns:

- It may be better as the user experience layer than the durable governance
  runtime.
- Hosting sensitive private PEGO data requires a separate privacy and security
  review.
- Product UI convenience should not define PEGO's agent contracts.

## Custom Runtime

A custom runtime may eventually be justified if PEGO needs concepts that general
agent frameworks do not model cleanly: constitutional authority, personal privacy
boundaries, directive synthesis, dissent preservation, and operating-memory
governance.

Potential fit:

- Maximum control over PEGO-specific concepts.
- Strong privacy boundaries.
- Runtime-neutral contracts remain first-class.

Potential concerns:

- Higher engineering cost.
- More reliability, observability, and scheduling work.
- Slower path to polished user experience.

## Near-Term Position

Do not choose a permanent runtime yet.

Build PEGO as a protocol and framework first. Keep the local repo adapter useful
for the founder instance. When the contracts stabilize, test at least two runtime
adapters against the same PEGO artifacts before committing to a product
architecture.

For the next phase, use Codex or another practical low-cost agent workspace
after a `uv`/`pegoctl` install prepares a discoverable PEGO workspace and
protected private instance. Treat MCP, tool servers, and hosted product
interfaces as future product integration and reference-runtime layers, not
immediate requirements.

See `pego/architecture/runtime-roadmap.md`.
