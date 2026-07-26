#!/usr/bin/env python3
"""Check that MkDocs navigation entries and Markdown files stay in sync."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"
MKDOCS_CONFIG = PROJECT_ROOT / "mkdocs.yml"


def collect_nav_entries(node: Any, paths: set[str], groups: list[str]) -> None:
    """Recursively collect Markdown leaves and grouping titles from ``nav``."""

    if isinstance(node, list):
        for item in node:
            collect_nav_entries(item, paths, groups)
        return

    if not isinstance(node, dict):
        return

    for key, value in node.items():
        if isinstance(value, str):
            if value.lower().endswith(".md"):
                paths.add(value.replace("\\", "/"))
            else:
                groups.append(str(key))
        else:
            # A nested list/dict is a visible MkDocs grouping rather than a page.
            groups.append(str(key))
            collect_nav_entries(value, paths, groups)


def is_file_below_docs(nav_path: str, docs_root: Path) -> bool:
    """Return whether a nav path resolves to an existing file below docs_root."""

    docs_root = docs_root.resolve()
    candidate = (docs_root / nav_path).resolve()
    try:
        candidate.relative_to(docs_root)
    except ValueError:
        return False
    return candidate.is_file()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true", help="exit 1 for missing nav files or unlisted files"
    )
    args = parser.parse_args(argv)

    try:
        config = yaml.safe_load(MKDOCS_CONFIG.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot parse {MKDOCS_CONFIG.name}: {exc}", file=sys.stderr)
        return 2

    nav_paths: set[str] = set()
    groups: list[str] = []
    collect_nav_entries(config.get("nav", []), nav_paths, groups)

    missing = sorted(path for path in nav_paths if not is_file_below_docs(path, DOCS_ROOT))
    actual_paths = {
        path.relative_to(DOCS_ROOT).as_posix() for path in DOCS_ROOT.rglob("*.md")
    }
    unlisted = sorted(actual_paths - nav_paths)

    for path in missing:
        print(f"ERROR: nav entry MISSING FILE: {path}")
    for path in unlisted:
        print(f"WARNING: FILE NOT IN NAV: {path}")
    for key in groups:
        print(f"INFO: unmatched nav key (directory): {key}")

    print(
        f"Checked {len(nav_paths)} nav Markdown entry(s) and {len(actual_paths)} docs Markdown file(s): "
        f"{len(missing)} error(s), {len(unlisted)} warning(s)."
    )
    return 1 if missing or (args.strict and unlisted) else 0


if __name__ == "__main__":
    sys.exit(main())
