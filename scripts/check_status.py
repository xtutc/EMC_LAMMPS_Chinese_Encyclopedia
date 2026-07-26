#!/usr/bin/env python3
"""Compare STATUS.md completion counts with the Markdown files actually present."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"
STATUS_FILE = PROJECT_ROOT / "STATUS.md"
MODULE_DIR_RE = re.compile(r"^(\d{2})_")
STATUS_MODULE_RE = re.compile(r"^(\d{2}(?:-\d{2})?)\b")
NUMBER_RE = re.compile(r"\d+")


def module_counts(docs_root: Path) -> tuple[Counter[str], int, int, int]:
    """Return module file counts plus total files, lines, and nonblank characters."""

    counts: Counter[str] = Counter()
    file_count = line_count = character_count = 0

    for path in sorted(docs_root.rglob("*.md")):
        relative = path.relative_to(docs_root)
        if len(relative.parts) == 1:
            module = "root"
        else:
            match = MODULE_DIR_RE.match(relative.parts[0])
            module = match.group(1) if match else relative.parts[0]
        counts[module] += 1

        lines = path.read_text(encoding="utf-8").splitlines()
        file_count += 1
        line_count += len(lines)
        character_count += sum(len(line) for line in lines if line.strip())

    return counts, file_count, line_count, character_count


def status_claims(status_file: Path) -> dict[str, tuple[str, int]]:
    """Extract module labels and the numeric '已完成' column from the rate table."""

    claims: dict[str, tuple[str, int]] = {}
    in_table = False
    for line in status_file.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] == "模块" and len(cells) >= 5:
            in_table = True
            continue
        if not in_table:
            continue
        if not line.lstrip().startswith("|"):
            break
        if not cells or re.fullmatch(r"[-:]+", cells[0]):
            continue
        if len(cells) < 3:
            continue
        module_match = STATUS_MODULE_RE.match(cells[0])
        count_match = NUMBER_RE.search(cells[2])
        if module_match and count_match:
            claims[module_match.group(1)] = (cells[0], int(count_match.group()))
    return claims


def actual_for_status_module(module: str, counts: Counter[str]) -> int:
    """Resolve an individual module, or an inclusive range such as ``11-17``."""

    if "-" not in module:
        return counts[module]
    start, end = (int(part) for part in module.split("-", 1))
    return sum(counts[f"{number:02d}"] for number in range(start, end + 1))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="exit 1 when a module count differs")
    args = parser.parse_args(argv)

    try:
        counts, files, lines, characters = module_counts(DOCS_ROOT)
        claims = status_claims(STATUS_FILE)
    except OSError as exc:
        print(f"ERROR: cannot read project files: {exc}", file=sys.stderr)
        return 2

    print(f"INFO: docs/index.md files: {sum(1 for path in DOCS_ROOT.glob('index.md'))}")
    print(f"INFO: docs/00_navigation/ Markdown files: {counts['00']}")
    for module in sorted(key for key in counts if key not in {"00", "root"}):
        print(f"INFO: actual module {module}: {counts[module]} Markdown file(s)")

    differences = 0
    for module, (label, claimed) in claims.items():
        actual = actual_for_status_module(module, counts)
        result = "MATCH" if claimed == actual else "DIFFERENCE"
        if result == "DIFFERENCE":
            differences += 1
        print(
            f"{result}: module {module} ({label}): "
            f"STATUS.md claimed {claimed}, docs/ actual {actual}"
        )

    print(f"INFO: docs/ Markdown files: {files}")
    print(f"INFO: docs/ Markdown lines: {lines}")
    print(f"INFO: docs/ Markdown nonblank characters: {characters}")
    print(f"Checked {len(claims)} STATUS.md module(s): {differences} difference(s).")
    return 1 if args.strict and differences else 0


if __name__ == "__main__":
    sys.exit(main())
