#!/usr/bin/env python3
"""Plan and apply public PEGO release files from an explicit allowlist.

This tool is intentionally mechanical: it compares a public base ref with a
source ref, classifies changed paths through a release allowlist, and can apply
the allowed file set into the current branch. The file list should not depend
on an LLM diff review.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PUBLIC_REMOTE = "https://github.com/usepego/pego.git"
DEFAULT_PUBLIC_BRANCH = "main"
DEFAULT_SOURCE_REF = "main"
DEFAULT_RELEASE_REF = "HEAD"

PUBLIC_RELEASE_ALLOWED_FILES = {
    ".gitignore",
    "AGENTS.md",
    "LICENSE",
    "LICENSE.md",
    "README.md",
    "pyproject.toml",
    "src/usepego/cli.py",
    "private/README.md",
}

PUBLIC_RELEASE_ALLOWED_PREFIXES = (
    ".github/workflows/",
    "decisions/",
    "ops/",
    "pego/",
    "site/",
)


class GitError(RuntimeError):
    pass


@dataclass(frozen=True)
class DiffItem:
    status: str
    paths: tuple[str, ...]

    @property
    def target(self) -> str:
        return self.paths[-1]

    @property
    def old_path(self) -> str | None:
        if self.status.startswith("R") and len(self.paths) == 2:
            return self.paths[0]
        return None


def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode != 0:
        output = "\n".join(
            part for part in [completed.stdout.strip(), completed.stderr.strip()] if part
        )
        raise GitError("git " + " ".join(args) + " failed" + (":\n" + output if output else ""))
    return completed


def is_public_release_file(relative: str) -> bool:
    if relative in PUBLIC_RELEASE_ALLOWED_FILES:
        return True
    return relative.startswith(PUBLIC_RELEASE_ALLOWED_PREFIXES)


def parse_name_status(output: str) -> list[DiffItem]:
    items: list[DiffItem] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        paths = tuple(parts[1:])
        if not paths:
            raise ValueError(f"unexpected git diff --name-status line: {line!r}")
        items.append(DiffItem(status=status, paths=paths))
    return items


def diff_items(base: str, source: str) -> list[DiffItem]:
    completed = run_git(["diff", "--name-status", "-M", f"{base}..{source}"])
    return parse_name_status(completed.stdout)


def changed_paths(base: str, source: str) -> set[str]:
    completed = run_git(["diff", "--name-only", f"{base}..{source}"])
    return {line for line in completed.stdout.splitlines() if line}


def resolve_public_ref(args: argparse.Namespace) -> str:
    if args.public_ref:
        return args.public_ref
    run_git(["fetch", args.public_remote, args.public_branch])
    return "FETCH_HEAD"


def clean_worktree() -> bool:
    return run_git(["status", "--porcelain"]).stdout.strip() == ""


def classify(items: list[DiffItem]) -> tuple[list[DiffItem], list[DiffItem]]:
    included = [item for item in items if is_public_release_file(item.target)]
    excluded = [item for item in items if not is_public_release_file(item.target)]
    return included, excluded


def missing_release_paths(public_ref: str, source_ref: str, release_ref: str) -> list[str]:
    source_changed = {
        item.target
        for item in diff_items(public_ref, source_ref)
        if is_public_release_file(item.target)
    }
    release_changed = changed_paths(public_ref, release_ref)
    return sorted(source_changed - release_changed)


def apply_items(source_ref: str, included: list[DiffItem]) -> None:
    delete_paths: list[str] = []
    restore_paths: list[str] = []

    for item in included:
        if item.status == "D":
            delete_paths.append(item.target)
            continue
        if item.old_path:
            delete_paths.append(item.old_path)
        restore_paths.append(item.target)

    if delete_paths:
        run_git(["rm", "--", *delete_paths])
    if restore_paths:
        run_git(["restore", "--source", source_ref, "--", *restore_paths])


def print_plan(included: list[DiffItem], excluded: list[DiffItem], missing: list[str]) -> None:
    print("PEGO public release plan")
    print(f"included: {len(included)}")
    for item in included:
        print(f"  {item.status}\t{item.target}")
    print(f"excluded: {len(excluded)}")
    for item in excluded:
        print(f"  {item.status}\t{', '.join(item.paths)}")
    print(f"missing from release ref: {len(missing)}")
    for path in missing:
        print(f"  {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-ref", default="")
    parser.add_argument("--public-remote", default=DEFAULT_PUBLIC_REMOTE)
    parser.add_argument("--public-branch", default=DEFAULT_PUBLIC_BRANCH)
    parser.add_argument("--source-ref", default=DEFAULT_SOURCE_REF)
    parser.add_argument("--release-ref", default=DEFAULT_RELEASE_REF)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--check-complete", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    public_ref = resolve_public_ref(args)
    source_ref = run_git(["rev-parse", "--verify", args.source_ref]).stdout.strip()
    release_ref = run_git(["rev-parse", "--verify", args.release_ref]).stdout.strip()

    included, excluded = classify(diff_items(public_ref, source_ref))
    missing = missing_release_paths(public_ref, source_ref, release_ref)
    print_plan(included, excluded, missing)

    if excluded:
        print("error: source ref changes files outside the public release allowlist", file=sys.stderr)
        return 1
    if args.check_complete and missing:
        print("error: release ref is missing public-allowed source changes", file=sys.stderr)
        return 1

    if args.apply:
        if not args.allow_dirty and not clean_worktree():
            print("error: working tree is not clean; commit/stash or pass --allow-dirty", file=sys.stderr)
            return 1
        apply_items(source_ref, included)
        print("status: applied")
    else:
        print("status: planned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
