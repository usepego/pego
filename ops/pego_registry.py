#!/usr/bin/env python3
"""Inspect the PEGO public system registry.

This command reads only pego/system/registry.json. It does not inspect private
instance files or print private data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "pego" / "system" / "registry.json"


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_FILE.read_text())


def print_agents(registry: dict[str, Any]) -> None:
    print("PEGO agents")
    for agent in registry["agents"]:
        print(
            f"- {agent['id']}: {agent['name']} "
            f"({agent['default_authority']})"
        )
        print(f"  protocol: {agent['protocol']}")
        model_spec = agent.get("model_spec")
        if model_spec:
            print(f"  model_spec: {model_spec}")
        print(f"  purpose: {agent['purpose']}")


def print_operations(registry: dict[str, Any]) -> None:
    print("PEGO operations")
    for operation in registry["operations"]:
        writes_to = operation["writes_to"] or "none"
        print(f"- {operation['id']}: {operation['runner']}")
        print(f"  procedure: {operation['procedure']}")
        print(f"  privacy: {operation['privacy']}")
        print(f"  writes_to: {writes_to}")


def print_governance(registry: dict[str, Any]) -> None:
    governance = registry["governance"]
    print("PEGO governance")
    for key in (
        "constitution_template",
        "authority_levels",
        "compliance_review",
        "repository_access_policy",
    ):
        print(f"- {key}: {governance[key]}")
    print("- required_review_for:")
    for item in governance["required_review_for"]:
        print(f"  - {item}")


def print_templates(registry: dict[str, Any]) -> None:
    print("PEGO templates")
    for template in registry["templates"]:
        print(f"- {template}")


def print_summary(registry: dict[str, Any]) -> None:
    print(f"{registry['name']}: {registry['full_name']}")
    print(registry["description"])
    print()
    print(f"agents: {len(registry['agents'])}")
    print(f"operations: {len(registry['operations'])}")
    print(f"templates: {len(registry['templates'])}")
    print(f"verified paths: {len(registry['verify_paths'])}")
    print()
    print("privacy:")
    print(f"- private instance root: {registry['privacy']['private_instance_root']}")
    print(f"- tracked private files: {', '.join(registry['privacy']['tracked_private_files'])}")
    print(f"- rule: {registry['privacy']['rule']}")


def print_json(registry: dict[str, Any]) -> None:
    print(json.dumps(registry, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "section",
        choices=("summary", "agents", "operations", "governance", "templates", "json"),
        nargs="?",
        default="summary",
    )
    args = parser.parse_args()

    registry = load_registry()
    printers = {
        "summary": print_summary,
        "agents": print_agents,
        "operations": print_operations,
        "governance": print_governance,
        "templates": print_templates,
        "json": print_json,
    }
    printers[args.section](registry)


if __name__ == "__main__":
    main()
