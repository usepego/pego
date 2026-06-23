# Tool Contract Template

Use this template when defining a capability agents may call.

Structured runtimes should emit `pego/schemas/tool-contract.schema.json`.

## Tool

Stable tool name.

## Purpose

What the tool does and why an agent would call it.

## Owning Agents

Which agents may call this tool.

## Inputs

Required and optional inputs.

## Outputs

Expected result shape.

## Authority Required

Level 0 / Level 1 / Level 2 / Level 3 / Level 4.

## Operation Type

Observe / Recommend / Direct / Execute / Escalate.

## Private Data Used

What private context may be sent to the tool?

## Third-Party Disclosure

None / Local only / External service / Requires explicit approval.

## Write Locations

Where outputs may be written.

## Governance Review

What review is required before the tool is called?

## Failure Mode

What should PEGO do if the tool fails, returns stale data, or returns low
confidence output?

## Logging Rule

What should be logged, and where?

## Prohibited Uses

What the tool must not be used for.
