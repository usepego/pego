# Runtime Roadmap

This roadmap captures PEGO's near-term operating path and future runtime
options.

PEGO remains runtime-neutral. The current practical path is to continue using
Codex as the operating runtime while PEGO's agent contracts, private-instance
boundary, council flow, and day-one user experience become coherent.

## Near-Term Runtime: Codex

Assumption for the next phase:

```text
The user installs PEGO with uv, then launches a Codex session in or against the
installed PEGO workspace. When the user says "Start PEGO", Codex discovers the
framework, private instance, tools, governance rules, and agent protocols.
```

This keeps costs low:

- No hosted always-on agent service.
- No production database dependency.
- No background schedules.
- No Vercel or cloud runtime required for early operation.
- LLM calls happen only when the user opens a session and asks PEGO to operate.

Codex is therefore the first operational adapter, not the permanent product
runtime.

## Expected Installed Shape

A future user-facing install path may look like:

```sh
uv tool install usepego
pegoctl init
```

Then the user opens Codex in the PEGO workspace or points Codex at the installed
PEGO framework and private instance.

The installed package should make discoverability straightforward:

- Public framework files are available under a known PEGO root.
- `AGENTS.md` or equivalent runtime instructions tell Codex how to operate.
- `pego/operations/first-run.md` defines session start.
- `pego/operations/runtime-agent-protocol.md` selects Operator, Council,
  Governance, or Domain Agent roles.
- `pego/system/registry.json` declares framework files, schemas, tools, and
  reference scripts.
- The private instance root is explicit and protected.

## Codex Start PEGO Flow

When the user says:

```text
Start PEGO.
```

Codex should:

1. Read repository/runtime instructions.
2. Select USER mode unless the user explicitly asks for Engineering or UX mode.
3. Check whether the private instance is usable.
4. Run safe local readiness/bootstrap checks if needed.
5. Load active private operating state.
6. Discover available PEGO tools from `pego/system/registry.json`, `pegoctl`,
   and local adapter scripts.
7. Load relevant agent protocols.
8. Ask one targeted missing-fact question or issue one directive.
9. Hide adapter mechanics, command output, diffs, file paths, and internal
   setup work from the user-facing response.

The visible output should remain:

```text
State update.
Next directive or targeted question.
Time box.
Start condition.
Do this.
Reason.
Fallback.
Deferred.
Stop condition.
Next check-in.
```

## Agent And Tool Discovery

Codex should treat PEGO framework files as prompts and policy, not as ordinary
documentation.

Agent guidance comes from:

- `pego/agents/*.md`
- `pego/agents/council-protocol.md`
- `pego/operations/runtime-agent-protocol.md`
- `pego/operations/operator-interface.md`
- `pego/governance/*.md`

Tool capability comes from:

- `pego/system/registry.json`
- `pego/tools/*.md`
- `pegoctl`
- `ops/` reference scripts

Python tools are adapter tools. They may create, validate, transform, or review
artifacts. They are not the conceptual PEGO runtime.

## Council Flow In Codex

In the Codex runtime, the LLM should act as the orchestrator:

1. Operations frames the decision.
2. Relevant domain-agent prompts are loaded.
3. Codex produces or requests structured agent recommendations.
4. Governance reviews authority, privacy, risk, reversibility, and protected
   time.
5. Council reconciles recommendations into one decision.
6. The decision becomes a directive candidate, targeted question, escalation, or
   stop condition.
7. The user sees only the command response.

The current Python council scripts are reference tools for artifact synthesis:

- `ops/council/synthesize_decision.py`
- `ops/council/decision_to_candidate.py`

Codex may call them, but should not treat them as the whole council brain.

## Future MCP Product Layer

PEGO may later expose an MCP server so multiple agent hosts can use the same
governed private instance.

Potential MCP tools:

- `pego.start`
- `pego.brief`
- `pego.next_directive`
- `pego.record_outcome`
- `pego.domain_scan`
- `pego.generate_agent_recommendations`
- `pego.synthesize_council_decision`
- `pego.governance_review`
- `pego.create_decision_packet`
- `pego.update_context`

Potential MCP resources:

- `pego://constitution`
- `pego://current-state`
- `pego://active-operating-brief`
- `pego://directive-queue`
- `pego://recent-outcomes`
- `pego://agent-protocols`
- `pego://council-decision/latest`

MCP should be permissioned, private-root scoped, auditable, and conservative.
It should default to read-only or Level 1 recommendation flows unless authority
is explicit.

MCP is an integration layer, not the whole PEGO product.

## Future Vercel AI SDK Reference Runtime

When the product surface is ready, PEGO may add a TypeScript reference runtime
using Vercel AI SDK.

In that architecture:

- The web/mobile product is TypeScript/Next.js.
- PEGO agents become AI SDK agents or subagents.
- Council orchestration is agent-first.
- Python remains for local validation, migration, scaffolding, and optional
  backend utilities.
- The runtime calls PEGO tools and writes PEGO-compatible artifacts.

This should not be built before the local Codex runtime proves the governance
loop:

```text
state -> agent recommendations -> council -> directive -> outcome -> updated state
```

## Cost Discipline

Do not incur significant hosted runtime cost until manual USER-mode operation
is useful.

Near-term rules:

- No always-on hosted agents.
- No autonomous background schedules.
- No recurring cloud database dependency for the founder instance.
- No multi-agent fanout unless needed for a real directive.
- Prefer user-triggered Codex sessions.
- Prefer local files and protected private state.
- Use Python reference tools where deterministic artifact work is enough.

## Open Work

1. Make `pegoctl init` prepare a Codex-discoverable PEGO workspace.
2. Add explicit Codex runtime instructions for installed-package operation, not
   only repository development.
3. Make `Start PEGO` run as a USER-mode facade that hides adapter telemetry.
4. Add domain-scan-to-agent-recommendation generation.
5. Route agent recommendations through council synthesis during first use.
6. Add tests that simulate a Codex USER-mode session without private facts.
7. Design a PEGO MCP interface after the core lifecycle stabilizes.
8. Defer Vercel AI SDK implementation until the local loop is compelling.
