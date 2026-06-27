#!/usr/bin/env python3
"""Generate a protected PEGO compliance review packet.

The output is written into the private instance under private/governance/reviews/.
The runner intentionally does not print private directive content.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "review"


def read_text(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"missing directive: {path}")
    return path.read_text()


def infer_authority_level(text: str) -> str:
    explicit = re.search(r"Authority level:\s*(Level\s+[1-4][^\n.]*)", text, re.IGNORECASE)
    if explicit:
        value = explicit.group(1).strip()
        level = re.search(r"Level\s+([1-4])", value, re.IGNORECASE)
        if level:
            return level_label(level.group(1))

    for level in ("4", "3", "2", "1"):
        if re.search(rf"(?<!No\s)Level\s+{level}\b", text, re.IGNORECASE):
            return level_label(level)
    return "Level 1: Recommend"


def level_label(level: str) -> str:
    return {
        "1": "Level 1: Recommend",
        "2": "Level 2: Direct",
        "3": "Level 3: Execute",
        "4": "Level 4: Escalate",
    }[level]


def infer_decision(authority_level: str) -> str:
    if authority_level.startswith("Level 1"):
        return "Approve with constraints"
    return "Request more information"


def build_review(directive_path: Path, review_date: str, slug: str) -> str:
    directive_text = read_text(directive_path)
    authority = infer_authority_level(directive_text)
    decision = infer_decision(authority)

    return f"""# Compliance Review: {slug}

Date: {review_date}

## Decision

{decision}

## Directive or Recommendation

Source directive:

```text
{directive_path}
```

Private directive content is not copied into this review by the runner.

## Authority Level

{authority}

## Constitutional Alignment

Pending local review.

Default assumption: proceed only if the directive preserves privacy, protected time, and existing constraints.

## Goal Alignment

Pending local review.

Confirm the directive advances at least one active goal without optimizing a proxy at the expense of the desired life.

## Constraint Fit

Pending local review.

Confirm the directive is feasible with current time, energy, resources, and local constraints.

## Evidence Quality

Initial classification: Agent inference or local directive synthesis.

Upgrade this if the directive is supported by telemetry, financial model output, repeated observed patterns, or expert sources.

## Risks

Default risks to check:

- Privacy.
- Time.
- Energy.
- Relationship/protected stakeholder impact.
- Financial.
- Health.
- Career.
- Opportunity cost.

## Reversibility

Pending local review.

Level 1 recommendations should generally be reversible. Escalate if the directive is hard to reverse.

## Privacy Impact

Private-only.

No public disclosure, third-party sharing, or framework-layer private instance data is approved.

## Dissent

Governance dissent: do not let a generated local directive silently become higher authority. Keep it at the inferred authority level unless explicitly adopted and reviewed.

## Conditions

- Do not commit private directive or review contents.
- Do not execute financial, medical, legal, career, relationship, or privacy-impacting actions without the required review level.
- Stop if protected time or privacy would be compromised.

## Review Date or Stop Condition

Review before execution if authority is above Level 1, or at end of day for a Level 1 daily directive.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--directive", required=True, type=Path)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--slug")
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    private = private_root_config.resolve_private_root(args.private_root)

    directive_path = args.directive
    slug = slugify(args.slug or directive_path.stem)
    target = private / "governance" / "reviews" / f"{args.date}-{slug}.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {target}")

    target.write_text(build_review(directive_path, args.date, slug))
    print(f"wrote: {target}")
    return target


if __name__ == "__main__":
    main_with_args()
