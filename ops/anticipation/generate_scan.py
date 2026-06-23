#!/usr/bin/env python3
"""Generate one protected PEGO anticipation scan.

The runner reads the private operating register and writes one scan packet into
private/anticipation/scans/. It prints only the output path because scan content
may contain private facts.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


@dataclass(frozen=True)
class RegisterItem:
    section: str
    cells: list[str]


SECTION_DOMAIN = {
    "Upcoming Events": "Event",
    "Recurring Annoyances": "Environment",
    "Supply Gaps": "Food and health",
    "Wardrobe and Presentation Prep": "Event",
    "Home and Environment Watchlist": "Environment",
    "Strategic Dependencies": "Strategy",
    "Fears and Concerns": "Finance and admin",
    "Questions to Ask": "Other",
}


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_data_row(line: str) -> bool:
    if not line.startswith("|"):
        return False
    return "---" not in line


def parse_register(register_text: str) -> list[RegisterItem]:
    items: list[RegisterItem] = []
    section = ""
    header: list[str] | None = None

    for line in register_text.splitlines():
        if line.startswith("## "):
            section = line.removeprefix("## ").strip()
            header = None
            continue
        if not section or not is_data_row(line):
            continue
        cells = parse_table_cells(line)
        if not cells or cells[0] == "TBD":
            continue
        if header is None:
            header = cells
            continue
        if cells == header:
            continue
        items.append(RegisterItem(section=section, cells=cells))

    return items


def item_domain(item: RegisterItem) -> str:
    return SECTION_DOMAIN.get(item.section, "Other")


def status_text(item: RegisterItem) -> str:
    if item.cells:
        return item.cells[-1].lower()
    return ""


def item_priority(item: RegisterItem) -> int:
    status = status_text(item)
    if "blocked" in status or "urgent" in status:
        return 0
    if "open" in status or "needed" in status or "todo" in status:
        return 1
    if "pending" in status or "unknown" in status:
        return 2
    return 3


def matches_domain(item: RegisterItem, domain: str | None) -> bool:
    if not domain:
        return True
    normalized = domain.lower()
    return normalized in item_domain(item).lower() or any(
        normalized in cell.lower() for cell in item.cells
    )


def choose_item(items: list[RegisterItem], domain: str | None) -> RegisterItem | None:
    viable = [item for item in items if matches_domain(item, domain)]
    if not viable:
        return None
    return sorted(viable, key=item_priority)[0]


def cell(item: RegisterItem, index: int, fallback: str = "Unknown") -> str:
    if index < len(item.cells) and item.cells[index]:
        return item.cells[index]
    return fallback


def sentence(value: str) -> str:
    value = value.strip()
    if not value:
        return "Unknown."
    if value.endswith((".", "?", "!")):
        return value
    return value + "."


def section_known_facts(item: RegisterItem) -> str:
    if item.section == "Upcoming Events":
        return f"Event: {cell(item, 0)}. Date/window: {cell(item, 1)}. Prep needed: {cell(item, 2)}."
    if item.section == "Recurring Annoyances":
        return f"Annoyance: {cell(item, 0)}. Trigger: {cell(item, 2)}. Preventive action: {cell(item, 3)}."
    if item.section == "Supply Gaps":
        return f"Supply: {cell(item, 0)}. Needed for: {cell(item, 2)}. Consequence: {cell(item, 3)}."
    if item.section == "Wardrobe and Presentation Prep":
        return f"Use case: {cell(item, 0)}. Current options: {cell(item, 1)}. Gap: {cell(item, 2)}."
    if item.section == "Home and Environment Watchlist":
        return f"Area: {cell(item, 0)}. Condition: {cell(item, 1)}. Useful action: {cell(item, 2)}."
    if item.section == "Strategic Dependencies":
        return f"Goal/program: {cell(item, 0)}. Dependency: {cell(item, 1)}. Blocking risk: {cell(item, 2)}."
    if item.section == "Fears and Concerns":
        return f"Concern: {cell(item, 0)}. Trigger/evidence: {cell(item, 2)}. Action needed: {cell(item, 3)}."
    if item.section == "Questions to Ask":
        return f"Question: {cell(item, 0)}. Why it matters: {cell(item, 1)}."
    return "Register item: " + "; ".join(item.cells)


def targeted_question(item: RegisterItem) -> str:
    if item.section == "Questions to Ask":
        return cell(item, 0)
    if item.section == "Upcoming Events":
        return f"What is the next missing prep item for {cell(item, 0)}?"
    if item.section == "Recurring Annoyances":
        return f"Has {cell(item, 0)} started to show up again, and can the smallest preventive action happen this week?"
    if item.section == "Supply Gaps":
        return f"Is {cell(item, 0)} currently stocked enough for {cell(item, 2)}?"
    if item.section == "Wardrobe and Presentation Prep":
        return f"What do you already own that works for {cell(item, 0)}, and what must be bought, cleaned, or tailored?"
    if item.section == "Home and Environment Watchlist":
        return f"Is {cell(item, 0)} visibly degrading the home environment right now?"
    if item.section == "Strategic Dependencies":
        return f"What is the smallest evidence action for {cell(item, 1)}?"
    if item.section == "Fears and Concerns":
        return f"What fact would reduce uncertainty about {cell(item, 0)}?"
    return "What decision-grade fact is needed before PEGO can turn this into a directive?"


def candidate_directive(item: RegisterItem) -> str:
    if item.section == "Upcoming Events":
        return cell(item, 2, "Identify prep needed")
    if item.section == "Recurring Annoyances":
        return cell(item, 3, "Perform smallest preventive action")
    if item.section == "Supply Gaps":
        return cell(item, 4, "Add missing supply to purchase list")
    if item.section == "Wardrobe and Presentation Prep":
        return cell(item, 3, "Decide, clean, tailor, or buy")
    if item.section == "Home and Environment Watchlist":
        return cell(item, 2, "Perform smallest useful action")
    if item.section == "Strategic Dependencies":
        return cell(item, 3, "Take next evidence action")
    if item.section == "Fears and Concerns":
        return cell(item, 3, "Gather one decision-grade fact")
    return "Ask targeted question"


def governance_status(item: RegisterItem) -> str:
    directive = candidate_directive(item).lower()
    if any(word in directive for word in ["buy", "purchase", "spend", "book", "hire"]):
        return "Level 1 recommendation unless spending is material; spending or stakeholder impact requires governance review."
    if item.section in {"Fears and Concerns", "Strategic Dependencies"}:
        return "Level 1 information-gathering only; escalate before career, financial, privacy, or relationship impact."
    return "Level 1 recommendation; proceed only if protected time, privacy, and stakeholder constraints still fit."


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "anticipation-scan"


def build_scan(item: RegisterItem | None, args: argparse.Namespace) -> str:
    if item is None:
        known_facts = "No actionable operating-register item matched the requested horizon/domain."
        question = "What upcoming event, supply gap, household issue, or strategic dependency should PEGO track next?"
        directive = "Add one concrete item to the operating register."
        domain = args.domain or "Other"
        trigger = "No matching register item"
        lead_time = "Unknown"
        consequence = "PEGO may miss preventable friction."
        status = "Level 1 question only."
    else:
        domain = item_domain(item)
        trigger = item.section
        known_facts = section_known_facts(item)
        question = targeted_question(item)
        directive = candidate_directive(item)
        lead_time = cell(item, 3, "This week") if item.section == "Upcoming Events" else "Before this becomes urgent."
        consequence = "Friction, delay, scrambling, or avoidable irritation may increase."
        status = governance_status(item)

    return "\n".join(
        [
            "# Anticipation Scan",
            "",
            "## Date",
            "",
            args.date,
            "",
            "## Horizon",
            "",
            args.horizon,
            "",
            "## Trigger",
            "",
            trigger,
            "",
            "## Domain",
            "",
            domain,
            "",
            "## Known Facts",
            "",
            sentence(known_facts),
            "",
            "## Unknowns",
            "",
            "The next decision-grade fact needed before PEGO schedules or escalates the candidate.",
            "",
            "## Targeted Question",
            "",
            question,
            "",
            "## Candidate Directive",
            "",
            directive,
            "",
            "## Lead Time",
            "",
            lead_time,
            "",
            "## Dependencies",
            "",
            "Schedule, supplies, weather, money, tools, another person, or external availability if applicable.",
            "",
            "## Priority",
            "",
            "Medium",
            "",
            "## Consequence of Deferral",
            "",
            consequence,
            "",
            "## Governance Status",
            "",
            status,
            "",
            "## Next Step",
            "",
            "Ask targeted question or add the candidate to directive synthesis.",
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--horizon", default="14 days")
    parser.add_argument("--domain")
    parser.add_argument("--register", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)
    args.register = args.register or private / "operator" / "operating-register.md"

    register_text = args.register.read_text() if args.register.exists() else ""
    items = parse_register(register_text)
    item = choose_item(items, args.domain)
    scan = build_scan(item, args)

    if args.output:
        output = args.output
    else:
        suffix = slugify(item.cells[0] if item else args.domain or "scan")
        output = private / "anticipation" / "scans" / f"{args.date}-{suffix}.md"

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(scan)
    print(f"wrote: {output}")


if __name__ == "__main__":
    main_with_args()
