# Adopt PEGO Name and Boundary

Date: 2026-06-21

## Decision

Use `PEGO` as the name for Personal Executive Governance OS.

Separate the repository into reusable framework material and a private personal instance.

## Rationale

`PEGO` is short, pronounceable, and supports product language better than `PEGOS`. The phrase `Governance OS` already carries the operating-system meaning.

The framework and private instance must be separated now so PEGO can later be open-sourced or monetized without extracting private life details from reusable material.

## Consequences

- `pego/` contains reusable framework material.
- `private/` contains actual personal life material.
- `ops/` contains scripts and integrations.
- `decisions/` records durable architecture and governance choices.

## Revisit If

- A trademark, domain, package, or brand conflict makes `PEGO` impractical.
- The framework becomes a separate public repository.
