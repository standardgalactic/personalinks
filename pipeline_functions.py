#!/usr/bin/env python3
"""
pipeline_functions.py

Support library for analyze-spherepop.sh (v2).

Everything that was previously an awkward bash heredoc — prompt
construction, chunking, caching, groundedness checking, batched
rolling synthesis — lives here as plain Python. The shell script
calls this file once per pipeline stage; each stage is a single
subcommand so bash never has to build or parse prompts itself.

Design goals carried over from the review of the v1 script:

  1. Chunks are never summarized blind. Every chunk prompt carries
     the document title, its position ("chunk 3 of 7"), a running
     one-paragraph abstract built from prior chunks, and which
     downstream stage will consume the output.

  2. Every summary claim must cite a quoted span from its source.
     A mechanical (non-LLM) pass checks each quote actually occurs
     in the source text and flags/strips anything that doesn't.

  3. Caching is content-hashed (model + prompt-template version +
     exact prompt text), not existence-only, so editing a prompt
     template invalidates only what it affects.

  4. Draft versions of the same logical document (``X.tex``,
     ``X-v01.tex``, ``X-draft-01.tex``) are canonicalized *before*
     clustering, so draft evolution isn't mistaken for corpus
     contradiction downstream.

  5. Cross-document synthesis happens in ordered batches with an
     explicit "synthesis so far + new batch" merge prompt, rather
     than one single-shot call over the entire corpus.

Every stage that calls the model goes through ``call_model``, which
is the only place ``ollama`` is invoked and the only place caching
happens.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

PROMPT_TEMPLATE_VERSION = "v2.0"

# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower()
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text


def read_text(path: Path) -> str:
    return path.read_text(errors="replace")


def normalize_for_match(text: str) -> str:
    """Collapse whitespace/case so quote-matching survives reflow."""
    return re.sub(r"\s+", " ", text).strip().lower()


# ---------------------------------------------------------------------------
# Stage: canonicalize
#
# Groups files that are drafts/versions of the same logical document
# and picks a canonical one, so downstream clustering doesn't treat
# sequential drafts as independent, mutually contradictory sources.
# ---------------------------------------------------------------------------

# Recognizes trailing version/draft markers so "History as Identity.tex",
# "History as Identity - v01.tex", "History as Identity - v02.tex" are
# grouped under the same stem.
_VERSION_SUFFIX = re.compile(
    r"""
    [\s_-]*
    (?:v|version|draft)
    [\s_-]*
    (\d+)
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _stem_and_version(path: Path) -> tuple[str, int]:
    """Return (grouping stem, version number). Version 0 = no marker
    (treated as the highest/most-finished unless a numbered draft
    exists with a later number)."""
    name = path.stem
    m = _VERSION_SUFFIX.search(name)
    if not m:
        return slugify(name), 0
    version = int(m.group(1))
    stem = name[: m.start()].rstrip(" _-")
    return slugify(stem), version


@dataclass
class LogicalDocument:
    stem: str
    canonical: str
    superseded: list[str] = field(default_factory=list)


def _mtime_or_none(p: Path) -> float | None:
    try:
        return p.stat().st_mtime
    except OSError:
        return None


def canonicalize(file_paths: list[Path]) -> dict:
    """Group draft/version files and pick a canonical one per group.

    Filename version markers ("v01", "v02", "draft-01") are used only
    to *group* files — they are not trustworthy for ordering, since
    "draft-01" means earlier work but "v02" means later work, and a
    naive numeric comparison can't tell those apart. The primary
    ordering signal is real filesystem mtime (most recently modified
    wins); the version number is kept only as a secondary tiebreaker
    when mtimes are unavailable or identical, and every group with
    more than one member is marked ``needs_review`` so a human can
    override the pick in plan.json before the run proceeds.
    """
    groups: dict[str, list[tuple[int, Path]]] = {}
    for p in file_paths:
        stem, version = _stem_and_version(p)
        groups.setdefault(stem, []).append((version, p))

    logical_docs: list[dict] = []
    for stem, members in groups.items():
        if len(members) == 1:
            canonical = members[0][1]
            logical_docs.append(
                {
                    "stem": stem,
                    "canonical": str(canonical),
                    "superseded": [],
                    "reason": "sole member of group",
                    "needs_review": False,
                }
            )
            continue

        enriched = [(v, p, _mtime_or_none(p)) for v, p in members]
        have_mtimes = all(m is not None for _, _, m in enriched)

        if have_mtimes:
            # Most recently modified wins.
            enriched.sort(key=lambda vpm: vpm[2], reverse=True)
            canonical = enriched[0][1]
            reason = "most recent mtime"
            # Flag for review if mtime order disagrees with version-
            # number order, since that's exactly the ambiguous case
            # (e.g. a "draft-01" with a newer mtime than the
            # unversioned file legitimately means the draft IS newer,
            # but it could also mean the draft was merely touched
            # last without being the intended final version).
            by_version = sorted(enriched, key=lambda vpm: vpm[0])
            needs_review = by_version[-1][1] != canonical
        else:
            enriched.sort(key=lambda vpm: vpm[0], reverse=True)
            canonical = enriched[0][1]
            reason = "highest version marker (mtime unavailable)"
            needs_review = True

        superseded = [p for _, p, _ in enriched if p != canonical]

        logical_docs.append(
            {
                "stem": stem,
                "canonical": str(canonical),
                "superseded": [str(p) for p in superseded],
                "reason": reason,
                "needs_review": needs_review,
            }
        )

    logical_docs.sort(key=lambda d: d["stem"])
    return {"logical_documents": logical_docs}


def cmd_resolve_canonical(args: argparse.Namespace) -> None:
    """Map plan.json's canonical/superseded source paths onto the
    already-extracted .txt files in TEXT_DIR (same slugify(rel-path)
    convention the extraction stage uses), so later stages can loop
    over "canonical extracted text files only" without re-deriving
    the naming convention themselves."""
    root = Path(args.root)
    text_dir = Path(args.text_dir)
    plan = json.loads(Path(args.plan).read_text())

    canonical_lines: list[str] = []
    superseded_lines: list[str] = []
    missing: list[str] = []

    for doc in plan["logical_documents"]:
        canon_path = Path(doc["canonical"])
        try:
            rel = canon_path.relative_to(root)
        except ValueError:
            rel = canon_path
        slug = slugify(str(rel))
        txt = text_dir / f"{slug}.txt"
        if txt.exists():
            canonical_lines.append(str(txt))
        else:
            missing.append(str(txt))

        for sup in doc.get("superseded", []):
            sup_path = Path(sup)
            try:
                rel = sup_path.relative_to(root)
            except ValueError:
                rel = sup_path
            slug = slugify(str(rel))
            txt = text_dir / f"{slug}.txt"
            if txt.exists():
                superseded_lines.append(str(txt))

    Path(args.out_canonical).write_text("\n".join(canonical_lines) + ("\n" if canonical_lines else ""))
    Path(args.out_superseded).write_text("\n".join(superseded_lines) + ("\n" if superseded_lines else ""))
    print(f"canonical: {len(canonical_lines)}  superseded: {len(superseded_lines)}  missing: {len(missing)}", file=sys.stderr)
    for m in missing:
        print(f"  missing extracted text for canonical doc: {m}", file=sys.stderr)


def cmd_canonicalize(args: argparse.Namespace) -> None:
    root = Path(args.root)
    paths = [Path(line.strip()) for line in Path(args.file_list).read_text().splitlines() if line.strip()]
    plan = canonicalize(paths)
    plan["root"] = str(root)
    Path(args.out).write_text(json.dumps(plan, indent=2))
    n_canon = len(plan["logical_documents"])
    n_superseded = sum(len(d["superseded"]) for d in plan["logical_documents"])
    print(f"canonicalized: {n_canon} logical documents, {n_superseded} superseded drafts set aside")


# ---------------------------------------------------------------------------
# Stage: model invocation with content-hashed caching
# ---------------------------------------------------------------------------


def cache_key(model: str, prompt: str) -> str:
    h = hashlib.sha256()
    h.update(model.encode())
    h.update(b"\x00")
    h.update(PROMPT_TEMPLATE_VERSION.encode())
    h.update(b"\x00")
    h.update(prompt.encode())
    return h.hexdigest()[:24]


def call_model(model: str, prompt: str, cache_dir: Path, force: bool = False) -> str:
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_key(model, prompt)
    cache_file = cache_dir / f"{key}.txt"

    if cache_file.exists() and not force:
        return cache_file.read_text()

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(
            f"ollama run {model} failed (code {result.returncode}): {result.stderr[:2000]}"
        )

    cache_file.write_text(result.stdout)
    return result.stdout


def cmd_call_model(args: argparse.Namespace) -> None:
    prompt = read_text(Path(args.prompt_file))
    output = call_model(
        args.model,
        prompt,
        Path(args.cache_dir),
        force=args.force,
    )
    Path(args.output).write_text(output)
    print(f"wrote {args.output} ({len(output)} chars, key={cache_key(args.model, prompt)})")


# ---------------------------------------------------------------------------
# Stage: chunking (paragraph-based, same limit strategy as v1)
# ---------------------------------------------------------------------------


def chunk_text(text: str, limit: int) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for para in paragraphs:
        addition = len(para) + 2
        if current and size + addition > limit:
            chunks.append("\n\n".join(current))
            current = []
            size = 0
        current.append(para)
        size += addition
    if current:
        chunks.append("\n\n".join(current))
    return chunks


# ---------------------------------------------------------------------------
# Stage: position-aware document summarization
#
# This is the direct fix for "chunks summarized in isolation." Every
# chunk prompt is built with the document title, its position, a
# running abstract carried forward from earlier chunks, and the name
# of the pipeline stage that will consume the final summary. The
# running abstract is itself model-generated but kept short
# (~120 words) specifically so it's cheap to regenerate each step.
# ---------------------------------------------------------------------------

ABSTRACT_PROMPT_TMPL = """\
You are building a running abstract of one document from the Spherepop
research corpus, incrementally, one chunk at a time.

Existing running abstract (empty if this is the first chunk):
{running_abstract}

New chunk text follows. Update the running abstract to roughly 120
words, integrating anything genuinely new from this chunk: new
primitives, new claims, new definitions. Do not include filler
commentary about the update process itself. Output only the updated
abstract, nothing else.

DOCUMENT TITLE: {title}

NEW CHUNK
=========

{chunk_text}
"""

CHUNK_SUMMARY_PROMPT_TMPL = """\
You are analyzing chunk {index} of {total} of a document called
"{title}", part of a large theoretical/computational research
repository called Spherepop.

This chunk's summary will feed into: {stage_context}

Running abstract of the document so far (built from earlier chunks;
use it for context, but summarize ONLY the new chunk below — do not
re-summarize material already captured in the running abstract):

{running_abstract}

For the NEW CHUNK below, extract:

1. definitions and primitive concepts introduced here;
2. mathematical claims and formal structures;
3. mechanisms and processes;
4. connections to concepts named in the running abstract above;
5. unresolved questions or contradictions visible within this chunk.

CRITICAL — groundedness requirement:
For every substantive claim, append a short verbatim quotation from
this chunk in the form [source: "..."] immediately after the claim,
using an exact quote no longer than ~20 words. If a claim cannot be
tied to an exact quote from this chunk, do not include it.

Do not invent claims absent from this chunk. Do not describe prose
style. Do not say "this is only a fragment."

NEW CHUNK
=========

{chunk_text}
"""

REDUCTION_PROMPT_TMPL = """\
The following are groundedness-checked analytical summaries of
consecutive fragments of one research document titled "{title}".

This document's synthesis will feed into: {stage_context}

Reconstruct the document as a unified theoretical object. Produce a
dense scholarly synthesis covering: thesis, primitives/definitions,
formalism, mechanisms, major arguments, dependencies between
concepts, implications, unresolved problems, internal tensions.

Preserve every [source: "..."] citation attached to a claim you keep.
Remove repetition introduced by chunking. Do not flatten genuine
distinctions. Do not add any claim that did not appear, with its
citation, in the fragment summaries below.

FRAGMENT SUMMARIES
===================

{fragment_summaries}
"""


def cmd_build_abstract_prompt(args: argparse.Namespace) -> None:
    running = Path(args.running_abstract_file).read_text() if Path(args.running_abstract_file).exists() else "(none yet)"
    chunk = read_text(Path(args.chunk_file))
    prompt = ABSTRACT_PROMPT_TMPL.format(
        running_abstract=running.strip(),
        title=args.title,
        chunk_text=chunk,
    )
    Path(args.out).write_text(prompt)


def cmd_build_chunk_prompt(args: argparse.Namespace) -> None:
    running = Path(args.running_abstract_file).read_text() if Path(args.running_abstract_file).exists() else "(none yet — this is the first chunk)"
    chunk = read_text(Path(args.chunk_file))
    prompt = CHUNK_SUMMARY_PROMPT_TMPL.format(
        index=args.index,
        total=args.total,
        title=args.title,
        stage_context=args.stage_context,
        running_abstract=running.strip(),
        chunk_text=chunk,
    )
    Path(args.out).write_text(prompt)


def cmd_build_reduction_prompt(args: argparse.Namespace) -> None:
    fragments = []
    for f in sorted(Path(args.fragments_dir).glob("chunk-*-summary.md")):
        fragments.append(f"--- {f.name} ---\n{read_text(f)}")
    prompt = REDUCTION_PROMPT_TMPL.format(
        title=args.title,
        stage_context=args.stage_context,
        fragment_summaries="\n\n".join(fragments),
    )
    Path(args.out).write_text(prompt)


# ---------------------------------------------------------------------------
# Stage: groundedness check
#
# Mechanical (no LLM) verification that every [source: "..."] quote
# attached to a claim actually appears in the source text. Claims
# whose quote doesn't match are stripped and logged, not silently
# kept. This runs after every chunk summary and after every
# reduction, and is what turns "do not invent claims" from an
# instruction into an enforced constraint.
# ---------------------------------------------------------------------------

CLAIM_LINE_RE = re.compile(r"^(?P<claim>.*?)\[source:\s*\"(?P<quote>.*?)\"\]\s*$", re.MULTILINE)


def check_groundedness(summary_text: str, source_text: str) -> tuple[str, list[str]]:
    normalized_source = normalize_for_match(source_text)
    kept_lines: list[str] = []
    flagged: list[str] = []

    for line in summary_text.splitlines():
        m = CLAIM_LINE_RE.match(line)
        if not m:
            # No citation on this line at all (headers, bullets w/o a
            # standalone claim, blank lines) — pass through unchanged.
            kept_lines.append(line)
            continue

        quote = m.group("quote")
        if normalize_for_match(quote) in normalized_source:
            kept_lines.append(line)
        else:
            flagged.append(line.strip())
            kept_lines.append(
                f"[UNGROUNDED — quote not found in source, claim removed: {m.group('claim').strip()[:120]}]"
            )

    return "\n".join(kept_lines), flagged


def cmd_check_groundedness(args: argparse.Namespace) -> None:
    summary = read_text(Path(args.summary_file))
    source = read_text(Path(args.source_file))
    cleaned, flagged = check_groundedness(summary, source)
    Path(args.out).write_text(cleaned)
    report_path = Path(args.out).with_suffix(".groundedness-report.txt")
    if flagged:
        report_path.write_text(
            "Claims removed for failing groundedness check:\n\n" + "\n\n".join(flagged) + "\n"
        )
    elif report_path.exists():
        report_path.unlink()
    print(f"groundedness: {len(flagged)} claim(s) flagged and removed")


# ---------------------------------------------------------------------------
# Stage: batched rolling cross-document synthesis
#
# Replaces the single-shot "cram every cluster summary into one
# prompt" step. Documents (or cluster summaries) are processed in
# ordered batches; each batch is merged into a running synthesis with
# an explicit "you are integrating batch K of N" framing, so context
# stays bounded and intermediate state is inspectable.
# ---------------------------------------------------------------------------

BATCH_MERGE_PROMPT_TMPL = """\
You are incrementally building a corpus-level synthesis of the
Spherepop research repository, {batch_label}, by merging new material
into a running synthesis. This is batch {batch_num} of {batch_total}.

Do not discard anything correct in the running synthesis below just
because the new batch doesn't mention it. Only revise the running
synthesis where the new batch adds, refines, or genuinely conflicts
with it. If it conflicts, note the conflict explicitly rather than
silently picking one side.

RUNNING SYNTHESIS SO FAR
=========================

{running_synthesis}

NEW BATCH ({batch_num} of {batch_total})
=========================================

{batch_content}
"""


def plan_batches(summary_files: list[Path], batch_size: int) -> list[list[Path]]:
    return [summary_files[i : i + batch_size] for i in range(0, len(summary_files), batch_size)]


def cmd_batch_plan(args: argparse.Namespace) -> None:
    """Read a plain newline-delimited file list and write it out as
    numbered batch files (out_dir/0001.txt, 0002.txt, ...), each
    containing the member paths for that batch, one per line. Plain
    text end to end — no JSON, no jq dependency for the shell side."""
    files = [Path(line.strip()) for line in Path(args.file_list).read_text().splitlines() if line.strip()]
    batches = plan_batches(files, args.batch_size)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.txt"):
        old.unlink()
    for i, batch in enumerate(batches, 1):
        (out_dir / f"{i:04d}.txt").write_text("\n".join(str(p) for p in batch) + "\n")
    print(len(batches))


def cmd_build_batch_merge_prompt(args: argparse.Namespace) -> None:
    running = read_text(Path(args.running_synthesis_file)) if Path(args.running_synthesis_file).exists() else "(none yet — this is the first batch)"
    batch_paths = [Path(line.strip()) for line in Path(args.batch_file_list).read_text().splitlines() if line.strip()]
    batch_content = []
    for p in batch_paths:
        batch_content.append(f"--- {p.name} ---\n{read_text(p)}")
    prompt = BATCH_MERGE_PROMPT_TMPL.format(
        batch_label=args.batch_label,
        batch_num=args.batch_num,
        batch_total=args.batch_total,
        running_synthesis=running.strip(),
        batch_content="\n\n".join(batch_content),
    )
    Path(args.out).write_text(prompt)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("canonicalize", help="Group draft versions and pick canonical files.")
    c.add_argument("root")
    c.add_argument("file_list", help="Text file, one path per line.")
    c.add_argument("out", help="Output plan.json")
    c.set_defaults(func=cmd_canonicalize)

    c = sub.add_parser("resolve-canonical", help="Map plan.json onto extracted .txt filenames.")
    c.add_argument("plan")
    c.add_argument("root")
    c.add_argument("text_dir")
    c.add_argument("out_canonical")
    c.add_argument("out_superseded")
    c.set_defaults(func=cmd_resolve_canonical)

    c = sub.add_parser("call-model", help="Run a prompt through ollama with content-hash caching.")
    c.add_argument("model")
    c.add_argument("prompt_file")
    c.add_argument("output")
    c.add_argument("--cache-dir", required=True)
    c.add_argument("--force", action="store_true")
    c.set_defaults(func=cmd_call_model)

    c = sub.add_parser("build-abstract-prompt")
    c.add_argument("title")
    c.add_argument("chunk_file")
    c.add_argument("running_abstract_file")
    c.add_argument("out")
    c.set_defaults(func=cmd_build_abstract_prompt)

    c = sub.add_parser("build-chunk-prompt")
    c.add_argument("title")
    c.add_argument("index", type=int)
    c.add_argument("total", type=int)
    c.add_argument("stage_context")
    c.add_argument("chunk_file")
    c.add_argument("running_abstract_file")
    c.add_argument("out")
    c.set_defaults(func=cmd_build_chunk_prompt)

    c = sub.add_parser("build-reduction-prompt")
    c.add_argument("title")
    c.add_argument("stage_context")
    c.add_argument("fragments_dir")
    c.add_argument("out")
    c.set_defaults(func=cmd_build_reduction_prompt)

    c = sub.add_parser("check-groundedness")
    c.add_argument("summary_file")
    c.add_argument("source_file")
    c.add_argument("out")
    c.set_defaults(func=cmd_check_groundedness)

    c = sub.add_parser("batch-plan", help="Split a plain file list into numbered batch files.")
    c.add_argument("file_list", help="Text file, one member path per line.")
    c.add_argument("batch_size", type=int)
    c.add_argument("out_dir", help="Directory to write 0001.txt, 0002.txt, ...")
    c.set_defaults(func=cmd_batch_plan)

    c = sub.add_parser("build-batch-merge-prompt")
    c.add_argument("batch_label")
    c.add_argument("batch_num", type=int)
    c.add_argument("batch_total", type=int)
    c.add_argument("running_synthesis_file")
    c.add_argument("batch_file_list", help="Plain text file, one member path per line.")
    c.add_argument("out")
    c.set_defaults(func=cmd_build_batch_merge_prompt)

    c = sub.add_parser("chunk-file", help="Split a text file into paragraph-bounded chunks under a limit.")
    c.add_argument("source_file")
    c.add_argument("out_dir")
    c.add_argument("--chunk-chars", type=int, default=45000)
    c.set_defaults(func=lambda a: _cmd_chunk_file(a))
    return p


def _cmd_chunk_file(args: argparse.Namespace) -> None:
    text = read_text(Path(args.source_file))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks = chunk_text(text, args.chunk_chars)
    for i, c in enumerate(chunks, 1):
        (out_dir / f"{i:04d}.txt").write_text(c)
    print(len(chunks))


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
