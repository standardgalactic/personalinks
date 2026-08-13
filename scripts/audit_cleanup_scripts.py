#!/usr/bin/env python3
"""Dry-run auditor for scripts/clean_tex_artifacts.sh (and any script using
the same `find ... -delete` idiom).

Core idea: don't reimplement find's boolean/grouping/negation logic in
Python -- that's fragile and easy to get subtly wrong for -o/!/\\( \\)
precedence, and a subtly-wrong auditor is worse than none. Instead, extract
each `find ... -delete` command verbatim from the shell script, substitute
its ${ROOT_DIR}/${OUT_ROOT} references with real paths, swap the trailing
`-delete` for `-print`, and actually run it -- the real `find` binary
evaluates the expression exactly as the cleanup script would, but this only
ever prints matches. Nothing is deleted.

Scope: this only understands `find ... -delete` blocks (the only deletion
idiom either script uses). It does not parse arbitrary shell -- a bare
`rm -rf $SOMETHING` elsewhere would not be caught, and this tool does not
claim otherwise.

Usage:
    python3 audit_cleanup_scripts.py REPO_ROOT [--script PATH] [--build-only]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

FIND_DELETE_RE = re.compile(r'find\s+"\$\{(\w+)\}"(.*?)-delete', re.DOTALL)


def extract_blocks(script_text: str):
    """Yield (root_var, find_expression_text) for each `find ... -delete`
    invocation in the script, in source order."""
    for m in FIND_DELETE_RE.finditer(script_text):
        # Collapse shell line-continuations ("\\" + newline) to a single
        # space *before* stripping -- stripping first can orphan a
        # trailing "\\" (not whitespace itself) right before the "-print"
        # this tool appends, producing a malformed command.
        expr = re.sub(r"\\[ \t]*\n", " ", m.group(2))
        expr = re.sub(r"\\\s*$", "", expr).strip()
        yield m.group(1), expr


def run_dry_run(root_var: str, expr: str, root_dir: Path, out_root: Path) -> list[str]:
    roots = {"ROOT_DIR": root_dir, "OUT_ROOT": out_root}
    if root_var not in roots:
        raise ValueError(
            f"unknown root variable {root_var!r} -- extend `roots` to audit this script"
        )

    real_root = roots[root_var]
    if not real_root.exists():
        # Mirrors this script's own `if [[ -d "${OUT_ROOT}" ]]` guard: a
        # find against a directory that doesn't exist yet matches nothing.
        return []

    # The expression body can itself reference ${ROOT_DIR}/${OUT_ROOT} (the
    # exclusion clauses do), not just the find root -- substitute both
    # everywhere, not only where the command starts.
    resolved_expr = expr
    for var, value in roots.items():
        resolved_expr = resolved_expr.replace("${" + var + "}", str(value))

    cmd = f'find "{real_root}" {resolved_expr} -print'
    result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line]


def git_tracked(repo_root: Path, paths: list[str]) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"], cwd=repo_root, capture_output=True, text=True, check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()

    tracked = {str((repo_root / p).resolve()) for p in result.stdout.splitlines()}
    return {p for p in paths if str(Path(p).resolve()) in tracked}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo_root", type=Path)
    ap.add_argument("--script", default="scripts/clean_tex_artifacts.sh")
    ap.add_argument(
        "--build-only",
        action="store_true",
        help="mirror the shell script's own --build-only: only audit OUT_ROOT-scoped blocks",
    )
    args = ap.parse_args()

    repo_root = args.repo_root.resolve()
    script_path = repo_root / args.script
    out_root = repo_root / "build" / "pdfs"

    if not script_path.exists():
        print(f"error: {script_path} not found", file=sys.stderr)
        return 1

    blocks = list(extract_blocks(script_path.read_text()))
    if not blocks:
        print("No `find ... -delete` blocks found -- nothing to audit.")
        return 0

    total_matches = 0
    ext_counter: Counter[str] = Counter()

    for i, (root_var, expr) in enumerate(blocks, start=1):
        # In this script pair, OUT_ROOT-scoped blocks always run and
        # ROOT_DIR-scoped blocks are the ones gated by BUILD_ONLY==0 --
        # a mapping specific to how this script happens to be structured,
        # not a general parse of its `if` conditionals.
        if args.build_only and root_var != "OUT_ROOT":
            continue
        try:
            matches = run_dry_run(root_var, expr, repo_root, out_root)
        except ValueError as e:
            print(f"block {i}: skipped -- {e}")
            continue
        except subprocess.CalledProcessError as e:
            print(f"block {i}: find failed -- {e.stderr}", file=sys.stderr)
            continue

        real_root = out_root if root_var == "OUT_ROOT" else repo_root
        if not real_root.exists():
            print(f"\nblock {i} (root=${{{root_var}}}): directory does not exist yet -- 0 matches")
            continue

        print(f"\nblock {i} (root=${{{root_var}}}): {len(matches)} file(s) would be deleted")
        tracked = git_tracked(repo_root, matches)
        for m in matches:
            ext = Path(m).suffix or "(no extension)"
            ext_counter[ext] += 1
            flag = "  [GIT-TRACKED]" if m in tracked else ""
            print(f"  {m}{flag}")
        total_matches += len(matches)

    print("\n--- summary ---")
    print(f"total files that would be deleted: {total_matches}")
    for ext, count in ext_counter.most_common():
        print(f"  {ext}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
