#!/usr/bin/env python3
"""Check inline Markdown links below docs/ without requiring MkDocs.

The normal mode is a reporting mode so it can be used while broken links are
being repaired.  Add ``--strict`` to make broken file or anchor links fail
the command.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"
LINK_RE = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^\n)]*)\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
EXPLICIT_ID_RE = re.compile(r"\{#([^}\s]+)\}")
HTML_ID_RE = re.compile(
    r"<a\s+[^>]*\bid\s*=\s*['\"]([^'\"]+)['\"][^>]*>", re.IGNORECASE
)
EXTERNAL_SCHEMES = {"http", "https", "mailto", "ftp", "tel", "data"}


@dataclass(frozen=True)
class Finding:
    source: Path
    line: int
    target: str
    reason: str
    severity: str = "ERROR"


def markdown_slug(text: str) -> str:
    """Produce the conventional Unicode-preserving Markdown heading slug."""

    text = html.unescape(text)
    text = re.sub(r"\{#[^}]+\}", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\-\s]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s\-]+", "-", text).strip("-")


def anchors_in(path: Path) -> set[str]:
    """Return explicit and heading-generated anchors found in a Markdown file."""

    anchors: set[str] = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        anchors.update(EXPLICIT_ID_RE.findall(line))
        anchors.update(HTML_ID_RE.findall(line))
        heading = HEADING_RE.match(line)
        if heading:
            slug = markdown_slug(heading.group(1))
            if slug:
                anchors.add(slug)
    return anchors


def destination(raw_target: str) -> str | None:
    """Extract a Markdown destination and ignore external URLs."""

    target = raw_target.strip()
    if not target:
        return None
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    parsed = urlsplit(target)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or target.startswith("//"):
        return None
    return unquote(target)


def links_in(path: Path):
    """Yield ``(line_number, destination)`` for inline links outside fences."""

    in_fence = False
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK_RE.finditer(line):
            target = destination(match.group(1))
            if target is not None:
                yield line_number, target


def check_links(docs_root: Path = DOCS_ROOT) -> list[Finding]:
    findings: list[Finding] = []
    anchors_cache: dict[Path, set[str]] = {}

    for source in sorted(docs_root.rglob("*.md")):
        for line, target in links_in(source):
            parsed = urlsplit(target)
            target_path = unquote(parsed.path)
            fragment = unquote(parsed.fragment)
            resolved = (source.parent / target_path).resolve() if target_path else source

            if not resolved.exists():
                findings.append(Finding(source, line, target, "target does not exist"))
                continue
            if resolved.is_dir():
                findings.append(
                    Finding(source, line, target, "target is a directory", severity="INFO")
                )
                continue
            if fragment:
                if resolved.suffix.lower() != ".md":
                    findings.append(
                        Finding(source, line, target, "anchor target is not a Markdown file")
                    )
                    continue
                anchors = anchors_cache.setdefault(resolved, anchors_in(resolved))
                if fragment not in anchors:
                    findings.append(Finding(source, line, target, "anchor does not exist"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="exit 1 when broken links are found")
    args = parser.parse_args(argv)

    findings = check_links()
    errors = [finding for finding in findings if finding.severity == "ERROR"]
    for finding in findings:
        try:
            source = finding.source.relative_to(PROJECT_ROOT)
        except ValueError:
            source = finding.source
        print(f"{finding.severity}: {source}:{finding.line}: broken link {finding.target} → {finding.reason}")

    print(f"Checked {sum(1 for _ in DOCS_ROOT.rglob('*.md'))} Markdown files: {len(errors)} error(s), "
          f"{len(findings) - len(errors)} info message(s).")
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    sys.exit(main())
