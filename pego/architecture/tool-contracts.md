# Tool Contracts

PEGO agents may call tools.

A tool is any bounded capability an agent can use to gather evidence, transform
private state, validate an artifact, or execute an approved action.

Tools are not PEGO itself. PEGO is the agent, governance, memory, directive, and
outcome framework that decides when a tool should be called, what authority is
required, how private data is handled, and how the result affects directives.

## Tool Layer

Examples:

- Calendar lookup.
- Grocery, menu, map, nutrition, or price lookup.
- Finance scenario calculation.
- Portfolio analysis.
- Schema validation.
- Privacy scan.
- Compliance preflight.
- Browser automation.
- Document generation.
- Trade execution, only under explicit authority and governance.

The implementation may be Python, TypeScript, a hosted API, a tool server, a
graph node, a mobile integration, a local CLI, or another adapter.

The conceptual contract should stay the same.

## Agent-To-Agent Versus Tool Calls

Agent-to-agent communication is deliberation.

Examples:

- Health Agent asks Finance Agent whether a meal plan affects budget strategy.
- Venture Agent asks Communications Agent whether a public essay creates
  opportunity.
- Governance Agent challenges a Finance Agent recommendation.
- Council asks each domain agent for a position and preserves dissent.

Tool calls are capability use.

Examples:

- Health Agent calls a grocery lookup tool.
- Finance Agent calls a scenario model.
- Governance Agent calls a privacy validator.
- Operations Agent calls a calendar availability tool.

An agent runtime may support both directly. PEGO does not require Python as the
message bus.

## Tool Contract Shape

Every tool should declare:

- Tool name.
- Purpose.
- Owning agent or agents.
- Input schema.
- Output schema.
- Authority required.
- Private data used.
- Third-party disclosure risk.
- Write locations.
- Failure mode.
- Governance review required before use.
- Whether the tool observes, recommends, directs, or executes.

Use `pego/templates/tool-contract.md`.

Structured runtimes should preserve tool contracts using:

```text
pego/schemas/tool-contract.schema.json
```

Initial reusable contracts live in:

```text
pego/tools/
```

These contracts name the capability and authority semantics. They do not require
any specific implementation language or runtime.

## Authority

Tools inherit PEGO authority levels.

- Observe tools may read permitted state or external facts.
- Recommend tools may analyze and propose.
- Direct tools may create or update directive artifacts.
- Execute tools may change the outside world and require explicit permission.
- Escalation tools create review packets or block unsafe actions.

If a tool can move money, trade, publish, message another person, book, buy,
delete, disclose private data, change health treatment, or alter a legal,
career, household, or relationship state, it is not a casual helper. It must be
declared, permissioned, logged, and governed.

## Privacy

Tools must receive the smallest private context needed to complete the call.

They must not leak private financial, health, relationship, household, location,
identity, employer, or preference data to public files, logs, examples,
telemetry, third-party services, or documentation without explicit approval.

Tool outputs that contain private facts belong in the protected private
instance.

## Reference Implementations

The current local Python scripts under `ops/` are reference tool
implementations and validation adapters.

They are useful for:

- CI.
- Smoke tests.
- Private artifact generation.
- Local operation before a polished runtime exists.
- Proving schemas and protocols can be exercised.

They should not define the PEGO product experience or prevent another runtime
from implementing the same contracts.
