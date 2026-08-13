**Rewriting Rules and Normalization**

The normalization procedure described in Section \ref{sec:normalization} ca[2D[K
can be precisely captured by a rewriting system acting on Spherepop express[7D[K
expressions. Rewriting systems provide a standard framework for defining ca[2D[K
canonical forms through the iterative application of local rules, and their[5D[K
their confluence and termination properties ensure that the normalization p[1D[K
process is well‑defined and terminates \citep{Abramsky1994}.

**Core Rewriting Rule**

The central rule leverages the independence relation $\parallel$ defined in[2D[K
in Section \ref{sec:normalization}. When two adjacent events in an event wo[2D[K
word are independent, their order can be exchanged:

\[
(E_i, E_j) \;\longrightarrow\; (E_j, E_i)
\quad\text{whenever } E_i \parallel E_j.
\]

**Normalization Process**

1. **Parse the Expression:** Convert the Spherepop expression into its unde[4D[K
underlying event word representation.

2. **Construct the Event Graph:** Identify all events and their independenc[11D[K
independence relations to build the causal graph of dependencies among even[4D[K
events.

3. **Apply Rewriting Rules Iteratively:**
   - Scan the event word linearly.
   - For each pair of adjacent events $(E_i, E_j)$ where $E_i \parallel E_j[3D[K
E_j$, apply the rewriting rule to reorder them as $(E_j, E_i)$.
   - Continue scanning and applying rewrites until no further independent s[1D[K
swaps are possible.

4. **Resulting Normal Form:** The event word obtained after all applicable [K
rewrites is in its normal form (canonical order). Two Spherepop expressions[11D[K
expressions represent identical objects precisely when they normalize to th[2D[K
the same normal form according to these rules.

**Properties**

- **Confluence:** Any two sequences of rewrite steps starting from a given [K
expression lead to the same normal form, ensuring that the result does not [K
depend on the order in which rewrites are applied.
  
- **Termination:** The process terminates because each rewrite reduces the [K
number of adjacent non‑independent pairs, and there is no infinite descendi[8D[K
descending chain of rewrites.

These rewriting rules thus provide a decision procedure for Spherepop ident[5D[K
identity: by parsing an expression, constructing its event graph, computing[9D[K
computing a topological ordering respecting independence relations, and com[3D[K
comparing resulting normal forms.

