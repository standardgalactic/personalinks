#!/usr/bin/env python3
"""Analyze a corpus of .tex files: inventory, duplicate/version clustering,
and rough structural stats. Read-only -- never writes into the corpus
itself, only to the report path given on the command line.

Three passes:

1. Exact duplicates: sha256 of raw file content. Catches byte-identical
   copies regardless of filename or directory (e.g. the same file
   checked into two places under different paths).

2. Near-duplicate / version clusters: group files by a normalized title
   derived from the filename (lowercased, extension stripped, common
   version/draft suffixes like "- v01", "draft-01", "_v2" removed, and
   underscores/hyphens folded to spaces). This is a filename heuristic,
   not a content diff -- two files landing in the same cluster share a
   title lineage, not necessarily near-identical text, and the reverse
   (a real revision under an unrelated name) won't be caught. Clusters
   report each member's size and mtime so the likely-canonical version
   (usually largest/newest) is visible at a glance, but this script does
   not guess which one that is.

3. Structural stats per file: an approximate word count (comments and
   command markup stripped by regex, not a real TeX parser, so this is
   an estimate -- true word counts need something like texcount), plus
   counts of \\section-family commands, \\label, \\cite, and the set of
   \\usepackage names.

Usage:
    python3 analyze_tex_corpus.py CORPUS_ROOT [--report OUT.md]
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

VERSION_SUFFIX_RE = re.compile(
    r"""
    \s*[-_]\s*v\d+$          |  # "- v01", "_v2", "-v1"
    \s*[-_]?\s*draft[\s-]?\d+$    # "draft-01", "-draft-01", " draft 01"
    """,
    re.IGNORECASE | re.VERBOSE,
)

COMMENT_RE = re.compile(r"(?<!\\)%.*$", re.MULTILINE)
COMMAND_RE = re.compile(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?")
BRACE_RE = re.compile(r"[{}]")
SECTION_RE = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\{")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z]*\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref)\{([^}]*)\}")
PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}")
TITLE_RE = re.compile(r"\\title\{([^}]*)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}")


@dataclass
class FileStats:
    path: Path
    size: int
    mtime: float
    content_hash: str
    word_count: int
    section_count: int
    labels: set[str] = field(default_factory=set)
    cite_keys: set[str] = field(default_factory=set)
    ref_keys: set[str] = field(default_factory=set)
    bibitem_keys: set[str] = field(default_factory=set)
    packages: set[str] = field(default_factory=set)
    declared_title: str | None = None


def normalize_title(path: Path) -> str:
    stem = path.stem
    stem = VERSION_SUFFIX_RE.sub("", stem)
    stem = stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\s+", " ", stem).strip().lower()
    return stem


def approx_word_count(text: str) -> int:
    text = COMMENT_RE.sub("", text)
    # Strip commands repeatedly: \foo[opt]{arg} can nest one level of
    # braces removal per pass (e.g. \textbf{\emph{x}}), so iterate until
    # stable rather than assuming one pass is enough.
    prev = None
    while prev != text:
        prev = text
        text = COMMAND_RE.sub(" ", text)
    text = BRACE_RE.sub(" ", text)
    words = [w for w in text.split() if any(c.isalpha() for c in w)]
    return len(words)


def analyze_file(path: Path) -> FileStats:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    title_match = TITLE_RE.search(text)
    stat = path.stat()
    return FileStats(
        path=path,
        size=stat.st_size,
        mtime=stat.st_mtime,
        content_hash=hashlib.sha256(raw).hexdigest(),
        word_count=approx_word_count(text),
        section_count=len(SECTION_RE.findall(text)),
        labels=set(LABEL_RE.findall(text)),
        cite_keys={k.strip() for group in CITE_RE.findall(text) for k in group.split(",")},
        ref_keys={k.strip() for group in REF_RE.findall(text) for k in group.split(",")},
        bibitem_keys=set(BIBITEM_RE.findall(text)),
        packages={p.strip() for group in PACKAGE_RE.findall(text) for p in group.split(",")},
        declared_title=title_match.group(1) if title_match else None,
    )


def build_report(root: Path, stats: list[FileStats]) -> str:
    lines: list[str] = []
    lines.append(f"# TeX corpus analysis: {root}")
    lines.append("")
    lines.append(f"{len(stats)} .tex files, {sum(s.word_count for s in stats):,} words (approx).")
    lines.append("")

    # --- exact duplicates ---
    by_hash: dict[str, list[FileStats]] = defaultdict(list)
    for s in stats:
        by_hash[s.content_hash].append(s)
    exact_dupes = {h: fs for h, fs in by_hash.items() if len(fs) > 1}
    lines.append(f"## Exact duplicates ({len(exact_dupes)} group(s))")
    lines.append("")
    if not exact_dupes:
        lines.append("None found.")
    for h, fs in sorted(exact_dupes.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"- {len(fs)} identical copies ({fs[0].size:,} bytes, sha256 {h[:12]}...):")
        for f in sorted(fs, key=lambda f: str(f.path)):
            lines.append(f"  - `{f.path.relative_to(root)}`")
    lines.append("")

    # --- near-duplicate / version clusters ---
    by_title: dict[str, list[FileStats]] = defaultdict(list)
    for s in stats:
        by_title[normalize_title(s.path)].append(s)
    clusters = {t: fs for t, fs in by_title.items() if len(fs) > 1}
    lines.append(f"## Title/version clusters ({len(clusters)} cluster(s))")
    lines.append("")
    lines.append(
        "Grouped by filename after stripping version/draft suffixes -- a "
        "naming heuristic, not a content diff. Largest file per cluster "
        "is bolded as a size-based guess only, not a canonicalization claim."
    )
    lines.append("")
    for title, fs in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"- **{title}** ({len(fs)} files):")
        biggest = max(fs, key=lambda f: f.size)
        for f in sorted(fs, key=lambda f: str(f.path)):
            marker = "**" if f is biggest else ""
            lines.append(
                f"  - {marker}`{f.path.relative_to(root)}`{marker} "
                f"-- {f.size:,} bytes, {f.word_count:,} words"
            )
    lines.append("")

    # --- per-file structural stats ---
    lines.append("## Per-file stats")
    lines.append("")
    lines.append("| file | words | sections | labels | cites | packages |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for s in sorted(stats, key=lambda f: str(f.path)):
        lines.append(
            f"| `{s.path.relative_to(root)}` | {s.word_count:,} | {s.section_count} "
            f"| {len(s.labels)} | {len(s.cite_keys)} | {len(s.packages)} |"
        )
    lines.append("")

    # --- package census ---
    package_counts: dict[str, int] = defaultdict(int)
    for s in stats:
        for p in s.packages:
            package_counts[p] += 1
    lines.append(f"## Package usage ({len(package_counts)} distinct package(s))")
    lines.append("")
    for pkg, count in sorted(package_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{pkg}`: {count} file(s)")
    lines.append("")

    # --- dangling references (corpus-wide) ---
    all_labels = {lbl for s in stats for lbl in s.labels} | {
        k for s in stats for k in s.bibitem_keys
    }
    lines.append("## Possibly-dangling references")
    lines.append("")
    lines.append(
        "A \\ref/\\cite key with no \\label/\\bibitem *anywhere in this corpus* "
        "-- real if each file is self-contained, a false positive if targets "
        "live in an external/shared .bib or a file outside this scan."
    )
    lines.append("")
    any_dangling = False
    for s in sorted(stats, key=lambda f: str(f.path)):
        dangling = (s.ref_keys | s.cite_keys) - all_labels
        if dangling:
            any_dangling = True
            lines.append(f"- `{s.path.relative_to(root)}`: {', '.join(sorted(dangling))}")
    if not any_dangling:
        lines.append("None found.")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("corpus_root", type=Path)
    ap.add_argument("--report", type=Path, default=None, help="write markdown report here")
    args = ap.parse_args()

    root = args.corpus_root.resolve()
    tex_files = sorted(root.rglob("*.tex"))
    if not tex_files:
        print("No .tex files found.", file=sys.stderr)
        return 1

    stats = [analyze_file(p) for p in tex_files]
    report = build_report(root, stats)

    if args.report:
        report_path = args.report.resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        print(f"Report written to {report_path} ({len(tex_files)} files analyzed).")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
