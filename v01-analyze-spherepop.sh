#!/usr/bin/env bash

# analyze-spherepop.sh
#
# Hierarchical, resumable repository analysis using Ollama / Granite.
#
# Pipeline:
#
#   repository
#       ↓
#   extraction
#       ↓
#   individual summaries
#       ↓
#   thematic cluster syntheses
#       ↓
#   cross-corpus synthesis
#       ↓
#   reflexive analysis
#       ↓
#   adversarial critique
#       ↓
#   reconstruction
#       ↓
#   final theory report
#
# LaTeX extraction strategy:
#
#   1. Pandoc directly from TeX
#   2. existing PDF + pdftotext
#   3. compile TeX -> PDF -> pdftotext
#   4. conservative source cleanup
#
# Usage:
#
#   chmod +x analyze-spherepop.sh
#   ./analyze-spherepop.sh
#
# Force regeneration:
#
#   FORCE=1 ./analyze-spherepop.sh
#
# Models may be overridden:
#
#   FAST_MODEL=granite4.1:3b \
#   DEEP_MODEL=granite4.1:8b \
#   ./analyze-spherepop.sh

set -Eeuo pipefail

###############################################################################
# Configuration
###############################################################################

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ANALYSIS="${ROOT}/analysis"

MANIFEST_DIR="${ANALYSIS}/00-manifest"
TEXT_DIR="${ANALYSIS}/01-extracted"
SUMMARY_DIR="${ANALYSIS}/02-document-summaries"
CLUSTER_DIR="${ANALYSIS}/03-cluster-syntheses"
CROSS_DIR="${ANALYSIS}/04-cross-analysis"
REFLECTION_DIR="${ANALYSIS}/05-reflection"
CRITIQUE_DIR="${ANALYSIS}/06-critique"
RECONSTRUCTION_DIR="${ANALYSIS}/07-reconstruction"
FINAL_DIR="${ANALYSIS}/08-final"

CACHE_DIR="${ANALYSIS}/.cache"
LOG_FILE="${ANALYSIS}/analysis.log"

FAST_MODEL="${FAST_MODEL:-granite4.1:3b}"
DEEP_MODEL="${DEEP_MODEL:-granite4.1:8b}"

FORCE="${FORCE:-0}"

# Keep individual chunks comfortably below model context.
CHUNK_CHARS="${CHUNK_CHARS:-45000}"

mkdir -p \
    "$MANIFEST_DIR" \
    "$TEXT_DIR" \
    "$SUMMARY_DIR" \
    "$CLUSTER_DIR" \
    "$CROSS_DIR" \
    "$REFLECTION_DIR" \
    "$CRITIQUE_DIR" \
    "$RECONSTRUCTION_DIR" \
    "$FINAL_DIR" \
    "$CACHE_DIR"

touch "$LOG_FILE"

###############################################################################
# Utilities
###############################################################################

log() {
    printf '[%s] %s\n' \
        "$(date '+%Y-%m-%d %H:%M:%S')" \
        "$*" >> "$LOG_FILE"
}

die() {
    echo "ERROR: $*" >&2
    exit 1
}

slugify() {
    printf '%s' "$1" |
        tr '[:upper:]' '[:lower:]' |
        sed \
            -e 's/[^a-z0-9._-]/-/g' \
            -e 's/--*/-/g' \
            -e 's/^-//' \
            -e 's/-$//'
}

command -v ollama >/dev/null ||
    die "ollama not found"

command -v python3 >/dev/null ||
    die "python3 not found"

###############################################################################
# Ollama
###############################################################################

run_model() {
    local model="$1"
    local prompt_file="$2"
    local output="$3"

    local partial="${output}.partial"

    if [[ -s "$output" && "$FORCE" != 1 ]]; then
        echo "[cached] $output"
        return 0
    fi

    echo
    echo "MODEL:  $model"
    echo "OUTPUT: $output"
    echo

    log "model=${model} output=${output}"

    rm -f "$partial"

    ollama run "$model" < "$prompt_file" |
        tee "$partial"

    if [[ ! -s "$partial" ]]; then
        die "Model produced empty output: $output"
    fi

    mv "$partial" "$output"
}

###############################################################################
# Manifest
###############################################################################

echo "Building repository manifest..."

find "$ROOT" \
    -type f \
    ! -path "${ANALYSIS}/*" \
    ! -path '*/.git/*' \
    ! -path '*/__pycache__/*' \
    ! -name '*.pyc' \
    | sort \
    > "${MANIFEST_DIR}/all-files.txt"

find "$ROOT" \
    -type f \
    -name '*.tex' \
    ! -path "${ANALYSIS}/*" \
    ! -path '*/.git/*' \
    | sort \
    > "${MANIFEST_DIR}/tex-files.txt"

find "$ROOT" \
    -type f \
    \( -name '*.md' -o -name '*.txt' \) \
    ! -path "${ANALYSIS}/*" \
    ! -path '*/.git/*' \
    | sort \
    > "${MANIFEST_DIR}/prose-files.txt"

find "$ROOT/spherepop" "$ROOT/tests" \
    -type f \
    -name '*.py' \
    2>/dev/null |
    sort \
    > "${MANIFEST_DIR}/python-files.txt"

###############################################################################
# LaTeX extraction
###############################################################################

extract_tex() {
    local src="$1"
    local rel="${src#$ROOT/}"
    local slug
    local out

    slug="$(slugify "$rel")"
    out="${TEXT_DIR}/${slug}.txt"

    if [[ -s "$out" && "$FORCE" != 1 ]]; then
        return
    fi

    echo "Extracting: $rel"

    ###########################################################################
    # Method 1 — Pandoc
    ###########################################################################

    if command -v pandoc >/dev/null; then

        if pandoc \
            --from=latex \
            --to=plain \
            --wrap=none \
            "$src" \
            > "${out}.partial" 2>/dev/null
        then
            if [[ -s "${out}.partial" ]]; then
                mv "${out}.partial" "$out"
                printf 'pandoc\t%s\n' "$rel" \
                    >> "${MANIFEST_DIR}/extraction-methods.tsv"
                return
            fi
        fi

    fi

    ###########################################################################
    # Method 2 — existing PDF
    ###########################################################################

    local pdf="${src%.tex}.pdf"

    if [[ -f "$pdf" ]] && command -v pdftotext >/dev/null; then

        if pdftotext -layout "$pdf" "${out}.partial" 2>/dev/null; then
            if [[ -s "${out}.partial" ]]; then
                mv "${out}.partial" "$out"
                printf 'existing-pdf\t%s\n' "$rel" \
                    >> "${MANIFEST_DIR}/extraction-methods.tsv"
                return
            fi
        fi

    fi

    ###########################################################################
    # Method 3 — compile temporary PDF
    ###########################################################################

    if command -v latexmk >/dev/null &&
       command -v pdftotext >/dev/null
    then

        local build="${CACHE_DIR}/pdf-${slug}"

        mkdir -p "$build"

        if latexmk \
            -pdf \
            -interaction=nonstopmode \
            -halt-on-error \
            -output-directory="$build" \
            "$src" \
            >/dev/null 2>&1
        then

            local generated="${build}/$(basename "${src%.tex}.pdf")"

            if [[ -f "$generated" ]]; then

                if pdftotext \
                    -layout \
                    "$generated" \
                    "${out}.partial"
                then
                    if [[ -s "${out}.partial" ]]; then
                        mv "${out}.partial" "$out"
                        printf 'compiled-pdf\t%s\n' "$rel" \
                            >> "${MANIFEST_DIR}/extraction-methods.tsv"
                        return
                    fi
                fi

            fi

        fi

    fi

    ###########################################################################
    # Method 4 — source fallback
    ###########################################################################

    sed \
        -e 's/%.*$//' \
        -e 's/\\section{\([^}]*\)}/\n\1\n/g' \
        -e 's/\\subsection{\([^}]*\)}/\n\1\n/g' \
        -e 's/\\subsubsection{\([^}]*\)}/\n\1\n/g' \
        "$src" \
        > "$out"

    printf 'source-fallback\t%s\n' "$rel" \
        >> "${MANIFEST_DIR}/extraction-methods.tsv"
}

: > "${MANIFEST_DIR}/extraction-methods.tsv"

while IFS= read -r file; do
    extract_tex "$file"
done < "${MANIFEST_DIR}/tex-files.txt"

###############################################################################
# Copy prose
###############################################################################

while IFS= read -r src; do

    rel="${src#$ROOT/}"
    slug="$(slugify "$rel")"
    out="${TEXT_DIR}/${slug}.txt"

    if [[ ! -s "$out" || "$FORCE" == 1 ]]; then
        cp "$src" "$out"
    fi

done < "${MANIFEST_DIR}/prose-files.txt"

###############################################################################
# Python/code corpus
###############################################################################

CODE_CORPUS="${TEXT_DIR}/implementation-python.txt"

if [[ ! -s "$CODE_CORPUS" || "$FORCE" == 1 ]]; then

    : > "$CODE_CORPUS"

    while IFS= read -r src; do

        echo
        echo "============================================================"
        echo "FILE: ${src#$ROOT/}"
        echo "============================================================"
        echo

        cat "$src"

    done < "${MANIFEST_DIR}/python-files.txt" \
        > "$CODE_CORPUS"

fi

###############################################################################
# Chunk + summarize one document
###############################################################################

summarize_document() {

    local src="$1"
    local base
    local size

    base="$(basename "$src" .txt)"
    size="$(wc -c < "$src")"

    local doc_dir="${SUMMARY_DIR}/${base}"
    mkdir -p "$doc_dir"

    ###########################################################################
    # Small document
    ###########################################################################

    if (( size <= CHUNK_CHARS )); then

        local prompt="${doc_dir}/prompt.txt"
        local output="${doc_dir}/summary.md"

        {
            cat <<'PROMPT'
You are analyzing one document from a large theoretical and
computational research repository called Spherepop.

Produce a dense scholarly summary.

Identify:

1. the central thesis;
2. definitions and primitive concepts;
3. mathematical claims;
4. important equations or formal structures;
5. mechanisms and processes;
6. philosophical commitments;
7. connections to computation;
8. connections to other likely parts of Spherepop;
9. unresolved questions;
10. contradictions, ambiguities, or weaknesses;
11. concepts that appear unusually important and should survive
    later compression.

Do not merely paraphrase section by section.

Preserve technical distinctions. Do not invent claims absent from
the source.

SOURCE DOCUMENT
===============

PROMPT
            cat "$src"
        } > "$prompt"

        run_model "$FAST_MODEL" "$prompt" "$output"

        return
    fi

    ###########################################################################
    # Large document — chunk it
    ###########################################################################

    local chunks="${doc_dir}/chunks"

    mkdir -p "$chunks"

    python3 - "$src" "$chunks" "$CHUNK_CHARS" <<'PY'
import pathlib
import sys

source = pathlib.Path(sys.argv[1])
destination = pathlib.Path(sys.argv[2])
limit = int(sys.argv[3])

text = source.read_text(errors="replace")

paragraphs = text.split("\n\n")

chunks = []
current = []

size = 0

for paragraph in paragraphs:
    addition = len(paragraph) + 2

    if current and size + addition > limit:
        chunks.append("\n\n".join(current))
        current = []
        size = 0

    current.append(paragraph)
    size += addition

if current:
    chunks.append("\n\n".join(current))

for number, chunk in enumerate(chunks, 1):
    path = destination / f"{number:04d}.txt"
    path.write_text(chunk)
PY

    ###########################################################################
    # Summarize chunks
    ###########################################################################

    for chunk in "$chunks"/*.txt; do

        chunk_name="$(basename "$chunk" .txt)"
        prompt="${doc_dir}/chunk-${chunk_name}-prompt.txt"
        summary="${doc_dir}/chunk-${chunk_name}-summary.md"

        {
            cat <<'PROMPT'
Analyze this fragment of a larger Spherepop document.

Extract the durable theoretical information from it.

Preserve definitions, equations, distinctions, mechanisms,
arguments, conjectures, dependencies, and unresolved questions.

Do not waste space describing prose style or saying that this is
only a fragment.

TEXT
====

PROMPT
            cat "$chunk"
        } > "$prompt"

        run_model "$FAST_MODEL" "$prompt" "$summary"

    done

    ###########################################################################
    # Reduce chunk summaries into document summary
    ###########################################################################

    local reduction_prompt="${doc_dir}/reduction-prompt.txt"
    local output="${doc_dir}/summary.md"

    {
        cat <<'PROMPT'
The following are analytical summaries of consecutive fragments
of one research document.

Reconstruct the document as a unified theoretical object.

Produce a dense scholarly synthesis covering:

- thesis;
- primitives and definitions;
- formalism;
- mechanisms;
- major arguments;
- dependencies between concepts;
- implications;
- unresolved problems;
- internal tensions;
- connections likely to matter elsewhere in Spherepop.

Remove repetition introduced by chunking.

Do not flatten genuine distinctions.

FRAGMENT SUMMARIES
==================

PROMPT

        cat "$doc_dir"/chunk-*-summary.md

    } > "$reduction_prompt"

    run_model "$FAST_MODEL" "$reduction_prompt" "$output"
}

###############################################################################
# Document summaries
###############################################################################

echo
echo "============================================================"
echo " DOCUMENT ANALYSIS"
echo "============================================================"
echo

for src in "$TEXT_DIR"/*.txt; do
    summarize_document "$src"
done

###############################################################################
# Construct thematic corpora from summaries
###############################################################################

make_cluster() {

    local name="$1"
    local regex="$2"

    local corpus="${CLUSTER_DIR}/${name}-corpus.md"
    local prompt="${CLUSTER_DIR}/${name}-prompt.txt"
    local output="${CLUSTER_DIR}/${name}.md"

    : > "$corpus"

    find "$SUMMARY_DIR" \
        -type f \
        -name summary.md \
        | sort \
        | grep -Ei "$regex" \
        | while IFS= read -r summary; do

            echo
            echo "============================================================"
            echo "SOURCE: $summary"
            echo "============================================================"
            echo

            cat "$summary"

        done >> "$corpus" || true

    [[ -s "$corpus" ]] || return 0

    {
        cat <<PROMPT
You are performing a second-order synthesis of the Spherepop
research corpus.

This cluster is:

    ${name}

The inputs are already document-level analytical summaries.

Determine the shared conceptual architecture rather than simply
summarizing them again.

Identify:

- recurring primitives;
- changing terminology for equivalent concepts;
- genuinely different concepts that must not be conflated;
- mathematical structures;
- causal or operational mechanisms;
- chronological development where visible;
- contradictions between documents;
- abandoned versus mature ideas;
- strongest theoretical claims;
- missing lemmas or bridges;
- implications not explicitly stated by individual documents.

End with a compact statement of what this cluster contributes to
Spherepop as a whole.

CORPUS
======

PROMPT

        cat "$corpus"

    } > "$prompt"

    run_model "$DEEP_MODEL" "$prompt" "$output"
}

###############################################################################
# Thematic synthesis
###############################################################################

echo
echo "============================================================"
echo " THEMATIC SYNTHESIS"
echo "============================================================"
echo

make_cluster \
    "identity-history" \
    'identity|history|event-history|execution-history|forkability'

make_cluster \
    "admissibility-refusal" \
    'admissib|refus|commitment|irreversib|collapse'

make_cluster \
    "geometry-dynamics" \
    'geodesic|geometry|scope|trajectory|rotation|dynamics'

make_cluster \
    "computation" \
    'comput|spherepop-os|specification|python|haskell|racket|implementation'

make_cluster \
    "memory-attention-intelligence" \
    'memory|attention|intelligence|thought|semantic'

make_cluster \
    "textbook-foundations" \
    'textbook|foundation|ecology|truth|logic|language|distinction'

make_cluster \
    "adaptive-trust" \
    'adaptive-trust|cycle1|cycle2|renewal|diagnosis'

make_cluster \
    "history-development" \
    'history-of-spherepop|changelog|future|improvement|theory-status'

###############################################################################
# Cross-corpus synthesis
###############################################################################

CROSS_PROMPT="${CROSS_DIR}/prompt.txt"
CROSS_OUTPUT="${CROSS_DIR}/spherepop-synthesis.md"

{
    cat <<'PROMPT'
You are now analyzing several thematic syntheses produced from a
large research repository.

Construct a unified account of Spherepop.

Do not merely concatenate the syntheses.

Determine the smallest conceptual architecture capable of
explaining the corpus.

Specifically determine:

1. primitive entities or distinctions;
2. primitive operations;
3. state and history;
4. identity;
5. admissibility;
6. refusal;
7. binding;
8. collapse;
9. observers and derived views;
10. trajectory structure;
11. geometry;
12. irreversibility;
13. memory;
14. computation;
15. semantics;
16. multi-timescale continuation;
17. the relation between implementation and theory.

Explicitly distinguish:

- foundational claims;
- derived results;
- metaphors;
- conjectures;
- implementation choices;
- historical artifacts;
- unresolved inconsistencies.

Search for latent equivalences between terminology used in
different parts of the corpus.

Also identify places where apparent equivalence is dangerous.

THEMATIC SYNTHESES
==================

PROMPT

    for file in "$CLUSTER_DIR"/*.md; do
        [[ "$file" == *-corpus.md ]] && continue
        [[ "$file" == *-prompt.txt ]] && continue

        echo
        echo "============================================================"
        echo "CLUSTER: $(basename "$file")"
        echo "============================================================"
        echo

        cat "$file"
    done

} > "$CROSS_PROMPT"

run_model \
    "$DEEP_MODEL" \
    "$CROSS_PROMPT" \
    "$CROSS_OUTPUT"

###############################################################################
# Reflexive pass
###############################################################################

REFLECTION_PROMPT="${REFLECTION_DIR}/prompt.txt"
REFLECTION_OUTPUT="${REFLECTION_DIR}/reflexive-analysis.md"

{
    cat <<'PROMPT'
Read the following attempted synthesis of Spherepop reflexively.

Do not ask merely whether it is correct.

Ask what conceptual machinery the synthesis itself had to use in
order to make the corpus coherent.

Identify:

- concepts functioning as hidden primitives;
- circular definitions;
- concepts doing several incompatible jobs;
- structures that recur at multiple scales;
- operations that appear more fundamental than the nouns used
  to describe them;
- distinctions lost during synthesis;
- ideas that become clearer only when documents are considered
  historically;
- ideas that become weaker when considered historically;
- places where the implementation provides a more precise theory
  than the prose;
- places where the prose contains theoretical commitments absent
  from the implementation.

Then propose a more economical conceptual basis for Spherepop.

SYNTHESIS
=========

PROMPT

    cat "$CROSS_OUTPUT"

} > "$REFLECTION_PROMPT"

run_model \
    "$DEEP_MODEL" \
    "$REFLECTION_PROMPT" \
    "$REFLECTION_OUTPUT"

###############################################################################
# Adversarial critique
###############################################################################

CRITIQUE_PROMPT="${CRITIQUE_DIR}/prompt.txt"
CRITIQUE_OUTPUT="${CRITIQUE_DIR}/critique.md"

{
    cat <<'PROMPT'
Act as a technically serious skeptical reviewer of the following
Spherepop synthesis and reflexive analysis.

Do not dismiss the project merely because its terminology is
unusual.

Instead identify exact failure modes.

Look especially for:

- undefined primitives;
- equivocation;
- circularity;
- category errors;
- claims stronger than their formal support;
- mathematical statements lacking necessary assumptions;
- accidental rediscovery of known structures;
- implementation behavior contradicting prose;
- examples that do not establish the claimed general result;
- terminology that obscures simpler formulations;
- unfalsifiable claims;
- missing counterexamples;
- missing invariants;
- places where multiple theories have been joined without a
  demonstrated bridge.

For each substantial criticism, state what would be required to
repair it.

SYNTHESIS
=========

PROMPT

    cat "$CROSS_OUTPUT"

    echo
    echo
    echo "REFLEXIVE ANALYSIS"
    echo "=================="
    echo

    cat "$REFLECTION_OUTPUT"

} > "$CRITIQUE_PROMPT"

run_model \
    "$DEEP_MODEL" \
    "$CRITIQUE_PROMPT" \
    "$CRITIQUE_OUTPUT"

###############################################################################
# Reconstruction
###############################################################################

RECON_PROMPT="${RECONSTRUCTION_DIR}/prompt.txt"
RECON_OUTPUT="${RECONSTRUCTION_DIR}/reconstruction.md"

{
    cat <<'PROMPT'
Reconstruct the Spherepop theory after criticism.

You have three inputs:

1. a corpus-level synthesis;
2. a reflexive analysis;
3. an adversarial critique.

Produce the strongest version of the theory justified by the
available material.

Do not defend every historical claim.

Discard weak formulations where necessary.

Separate:

- axioms or primitives;
- definitions;
- operations;
- invariants;
- derived propositions;
- conjectures;
- empirical or computational observations;
- philosophical interpretations.

Where the critique exposes a genuine gap, preserve the gap
explicitly rather than inventing a solution.

Where several terms can be unified, propose canonical
terminology.

Where terms must remain distinct, explain why.

The objective is conceptual compression without conceptual loss.

CORPUS SYNTHESIS
================

PROMPT

    cat "$CROSS_OUTPUT"

    echo
    echo
    echo "REFLEXIVE ANALYSIS"
    echo "=================="
    echo

    cat "$REFLECTION_OUTPUT"

    echo
    echo
    echo "ADVERSARIAL CRITIQUE"
    echo "===================="
    echo

    cat "$CRITIQUE_OUTPUT"

} > "$RECON_PROMPT"

run_model \
    "$DEEP_MODEL" \
    "$RECON_PROMPT" \
    "$RECON_OUTPUT"

###############################################################################
# Final report
###############################################################################

FINAL_PROMPT="${FINAL_DIR}/prompt.txt"
FINAL_OUTPUT="${FINAL_DIR}/spherepop-theory-report.md"

{
    cat <<'PROMPT'
Produce the final research report on the Spherepop repository.

This report should be useful to the author as a map of the entire
research program.

Write substantial, precise prose.

Include:

EXECUTIVE SYNTHESIS

Explain what Spherepop appears to be at its deepest level.

THEORETICAL ARCHITECTURE

Give the minimal coherent conceptual architecture.

FORMAL CORE

State the important primitives, operations, relations,
invariants, equations, and formal claims.

THEORY / IMPLEMENTATION RELATION

Explain what the Python implementation establishes, what it only
illustrates, and what remains purely theoretical.

INTELLECTUAL DEVELOPMENT

Explain major conceptual changes visible across drafts, histories,
experiments, and mature documents.

TERMINOLOGY

Identify synonyms, near-synonyms, overloaded terms, and concepts
that should remain sharply distinct.

STRONGEST RESULTS

Identify the portions of the project that appear most rigorous or
most conceptually distinctive.

WEAKEST LINKS

Identify unresolved gaps without rhetorical softening.

OPEN PROBLEMS

Construct a prioritized research agenda.

CANONICALIZATION

Recommend which documents appear canonical, which are historical,
which are exploratory, and which appear superseded.

COMPRESSION

End with three increasingly compressed descriptions:

1. approximately 1000 words;
2. approximately 250 words;
3. one paragraph.

Do not introduce unsupported claims merely to make the theory
appear unified.

RECONSTRUCTED THEORY
====================

PROMPT

    cat "$RECON_OUTPUT"

    echo
    echo
    echo "ADVERSARIAL CRITIQUE"
    echo "===================="
    echo

    cat "$CRITIQUE_OUTPUT"

} > "$FINAL_PROMPT"

run_model \
    "$DEEP_MODEL" \
    "$FINAL_PROMPT" \
    "$FINAL_OUTPUT"

###############################################################################
# Done
###############################################################################

echo
echo "============================================================"
echo " SPHEREPOP REPOSITORY ANALYSIS COMPLETE"
echo "============================================================"
echo

echo "Final report:"
echo
echo "    $FINAL_OUTPUT"
echo

echo "Intermediate reasoning:"
echo
echo "    $ANALYSIS"
echo

echo "The analysis tree preserves every reflexive stage."
echo
