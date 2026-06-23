# PEGO System Registry

This directory contains the public framework registry for PEGO.

The registry is not the private life instance. It is a machine-readable map of
agents, tool contracts, operating loops, governance controls, templates, and
schemas that are safe to publish with the framework.

The `tools` section lists capabilities agents may call. These are contracts,
not implementations. A runtime may implement a listed tool through Python,
TypeScript, MCP, EVE, LangGraph, Vercel AI SDK, a mobile integration, or another
adapter while preserving the same authority and privacy rules.

Private facts, goals, balances, health details, relationship context, and local
directive outputs belong in the protected private instance under `private/`.
