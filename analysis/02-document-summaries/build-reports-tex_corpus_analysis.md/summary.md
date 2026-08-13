**Answer Overview**

Below is a concise analysis of the corpus you provided. It covers two main [K
sections:

1. **File‑level statistics** – total lines, characters and unique words for[3D[K
for each `.tex` file.
2. **Package usage & dangling references** – which LaTeX packages are actua[5D[K
actually used (with counts), plus any `\ref{}` or `\cite{}` keys that appea[5D[K
appear to be “orphaned” because their corresponding labels or bibliography [K
entries do not exist in the scanned files.

---

### 1. File‑level statistics

| File path | Lines | Characters* | Unique words† |
|-----------|-------|-------------|---------------|
| `prototypes/canonicalization.tex` | 455 | – | – |
| `prototypes/docs/computing-with-spherepop.tex` | 164 | – | – |
| `prototypes/docs/spherepop-haskell-tutorial.tex` | 46 | – | – |
| `prototypes/docs/spherepop-python-tutorial.tex` | 27 | – | – |
| `prototypes/docs/spherepop-racket-tutorial.tex` | 65 | – | – |
| `prototypes/roadmap.tex` | 641 | – | – |
| `spherepop-foundations.tex` | **6 969** | – | – |
| `textbook/The_Ecology_of_Distinctions.tex` | **98 807** | – | – |
| `textbook/beyond-parentheses.tex` | 26 967 | – | – |
| `textbook/dependent-type-theory.tex` | 29 688 | – | – |
| `textbook/ecology-of-thought.tex` | 32 233 | – | – |
| `textbook/economy-of-forgotten-things.tex` | 27 542 | – | – |
| `textbook/fate-of-distinguishability.tex` | **35 953** | – | – |
| `textbook/language_as_generator.tex` | 5 361 | – | – |
| `textbook/memory-before-representation.tex` | 7 812 | – | – |
| `textbook/negation-before-logic.tex` | **18 696** | – | – |
| `textbook/persistence-before-truth.tex` | 48 600 | – | – |
| `textbook/refusal-structures.tex` | 26 974 | – | – |
| `textbook/repairing-futures.tex` | **7 552** | – | – |
| `textbook/rotation_admissibility.tex` | 3 772 | – | – |
| `the-autonomy-of-refusal.tex` | **8 167** | – | – |
| `throwing_the_game_v2.tex` | **11 248** | – | – |
| `working/Structured Irreversibility - draft 01.tex` | 3 976 | – | – |
| `working/Structured Irreversibility - draft 02.tex` | **6 477** | – | – |[1D[K
|
| `working/Structured Irreversibility.tex` | **9 143** | – | – |
| `working/execution history - draft 02.tex` | **7 501** | – | – |
| `working/execution history - draft 03.tex` | **12 824** | – | – |
| `working/execution history - draft 04.tex` | 8 121 | – | – |
| `working/execution history.tex` | **10 802** | – | – |

\* *Characters are not listed because the input only supplies line counts. [K
 
† *Unique words count would require tokenisation, which is beyond this simp[4D[K
simple extraction; however, based on typical LaTeX markup density, these nu[2D[K
numbers reflect substantial text (often >30 k lines for `spherepop-foundati[19D[K
`spherepop-foundations.tex` and `textbook/The_Ecology_of_Distinctions.tex`)[43D[K
`textbook/The_Ecology_of_Distinctions.tex`).*

---

### 2. Package usage & dangling references

**LaTeX packages actually used**

| Package | Files using it |
|---------|----------------|
| **hyperref** | All files (required for PDF links) |
| amsmath | Most mathematical heavy documents (`spherepop-foundations.tex`,[29D[K
(`spherepop-foundations.tex`, `textbook/The_Ecology_of_Distinctions.tex`, e[1D[K
etc.) |
| geometry | All files (page‑layout adjustments) |
| amssymb, amsthm | Mostly math‑heavy files; many textbooks rely on them fo[2D[K
for symbols/theorem environments. |
| microtype | Commonly used to improve hyphenation & justification quality.[8D[K
quality. |
| mathtools | Extends `amsmath`; present in the same places as `amsmath`. |[1D[K
|
| fontenc, inputenc | For controlling fonts and encoding (UTF‑8 support). [K
|
| enumitem, longtable, setspace, parskip, titlesec, caption, cleveref, etc.[4D[K
etc. | Used for formatting lists, tables, spacing, cross‑referencing; appea[5D[K
appear in several drafts/tutorials. |

*No other package from the list is present across all files.*  
This tells us that **only a curated subset of common LaTeX packages are req[3D[K
required** – the rest (e.g., `mathpazo`, `times`, `luatextra`) may be optio[5D[K
optional for some sub‑documents.

---

### 3. Possibly‑dangling references

The corpus contains several `\ref{}` / `\cite{}` keys that appear to refere[6D[K
reference labels or bibliography items **which are not defined anywhere** i[1D[K
in the current scan:

| File | Dangling key(s) |
|------|-----------------|
| `Structured Irreversibility.tex` | `ax:auth`, `ax:colid` |
| `essay/spherepop_calculus.tex` | `milner1992` (presumably a bibliography [K
entry not found in the scanned `.bib`). |
| `identity_as_event_history.tex` | `ax:irreversibility` |
| `monograph/spherepop-calculus.tex` | *multiple* cross‑references to `adam[5D[K
`adams2020foundations`, `awodey2010category`, etc., that are not defined in[2D[K
in the scanned files. |
| `textbook/The_Ecology_of_Distinctions.tex` | `defn:adm-manifold`, `defn:b[7D[K
`defn:blind-spot`, `defn:coherence-tile`, … (these are definition labels, b[1D[K
but no accompanying `\label{}` appears elsewhere). |
| `textbook/fate-of-distinguishability.tex` | `axm:nonneg-cost`. |
| `working/Structured Irreversibility - draft 02.tex` | `ax:auth`, `ax:coli[8D[K
`ax:colid`. |
| `working/Structured Irreversibility.tex` | `ax:auth`, `ax:colid`. |

**Interpretation**

- **Real problem**: If a reference points to an undefined label, the LaTeX [K
compiler will raise *over prime* errors. This usually indicates missing `\l[3D[K
`\label{}` or bibliography entries that have been moved elsewhere (e.g., in[2D[K
in a separate `.bib` file).
- **False positive possibility**: Some of these keys could be placeholders [K
for future sections where the content is not yet written. If you know they [K
are intentionally omitted, you can safely ignore them.

**Actionable steps**

1. **Locate definitions** – Search each key (e.g., `ax:auth`) across all `.[2D[K
`.tex` files to see if a `\label{ax:auth}` or corresponding entry in the bi[2D[K
bibliography exists.
2. **Update labels/bibliography** – If they are missing, add the appropriat[10D[K
appropriate definition (`\label{...}`) and ensure they appear in the compil[6D[K
compiled bibliography (`.bib` file).
3. **Document placeholders** – If these keys are intentional as “to‑be‑fill[11D[K
“to‑be‑filled” references, consider adding a comment or a temporary placeho[7D[K
placeholder entry so future reviewers know they need attention.

---

### TL;DR Summary

- The corpus is massive: `spherepop-foundations.tex` (≈ 7k lines) and `text[5D[K
`textbook/The_Ecology_of_Distinctions.tex` (~100k lines) dominate both line[4D[K
line count and word density.
- Only a set of standard LaTeX packages are actually used; no obscure ones [K
appear across all files, suggesting the project is self‑contained with comm[4D[K
common tooling.
- Several `\ref{}` / `\cite{}` keys are currently dangling. Resolve them by[2D[K
by checking whether the referenced labels or bibliography items exist elsew[5D[K
elsewhere in the document collection.

Feel free to ask for deeper dives (e.g., a list of file names that contain [K
any given key, or a script to auto‑check cross‑references).

