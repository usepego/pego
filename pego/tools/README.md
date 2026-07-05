# PEGO Tool Catalog

Runtime-neutral tool contracts for capabilities PEGO agents may call.

This directory does not define a runtime. A tool listed here may later be
implemented as Python, TypeScript, a tool server, graph node, mobile
integration, hosted service, or another adapter.

Agents call tools only when the call supports a directive, council decision,
governance review, evidence update, or outcome review.

## Initial Core Tools

- `calendar.availability`: observe commitments, protected time, and viable time
  windows.
- `food.environment.lookup`: observe food options around the human and convert
  them into comparable food-option artifacts.
- `finance.scenario_model`: recommend financial trajectory scenarios from
  protected assumptions.
- `finance.portfolio_analyze`: recommend portfolio risk, allocation, drift, and
  decision questions without execution authority.
- `governance.preflight`: classify a proposed directive before adoption or
  execution.
- `execution.financial_trade`: high-impact execution tool for future use only
  after explicit authority, review, and account-level permissions.

## Rules

- Tool contracts are public and generic.
- Tool runs that include private facts write only to the protected private
  instance.
- Tools do not decide life strategy; agents and Council do.
- Execution tools are locked unless the private constitution and governance
  review explicitly grant permission.
- Runtime adapters may expose additional private tools, but they must preserve
  the same authority and privacy semantics.
