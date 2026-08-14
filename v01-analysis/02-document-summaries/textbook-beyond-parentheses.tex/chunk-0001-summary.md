**Replay and Refusal: A Historical View of Computation**

---

### 1. From Substitution to Replay  

Traditional symbolic computation replaces a function’s formal parameter wit[3D[K
with an actual argument using **substitution**:

\[
(\lambda x.t)\;u \;\longrightarrow\; t[u/x].
\]

*Why this works:* the substitution operation erases the story of how `u` ca[2D[K
came into being, leaving only its syntactic value.  

In Spherepop we argue that computation is fundamentally a **continuation of[2D[K
of historical construction**, not just isolated symbolic manipulation.

#### Replay as an Extension Operation  

Instead of inserting the raw argument `v`, replay records both the *value* [K
and its provenance:

\[
(v,H_v) \quad\text{where } H_v \text{ is the history that produced } v.
\]

When a function expects a value of type `A` and we have an argument `v:A` w[1D[K
with history \(H_v\), application becomes

\[
(H_f,\;H_v)\;\xrightarrow{\text{Replay}}\;(H',\text{result}),
\]

where the resulting computation inherits **both** histories. This preserves[9D[K
preserves every step that led to the value, allowing later analysis (e.g., [K
debugging, verification) to trace back precisely how a result was obtained.[9D[K
obtained.

---

### 2. Refusal as an Admissibility Guard  

#### What is Refusal?  

Refusal is not an error or exception; it is a **computational boundary** th[2D[K
that blocks any continuation of a history when the proposed step would viol[4D[K
violate admissible conditions:

\[
H \longrightarrow 
\begin{cases}
H \| e & \text{if } \operatorname{Adm}(H,e) \text{ holds},\\[4pt]
\operatorname{Refuse}(r) & \text{otherwise}.
\end{cases}
\]

*Key point:* a refusal occurs **before** the computation proceeds, preventi[8D[K
preventing any inadmissible history from being recorded.

#### Why This Matters  

- **Errors are not “after‑the‑fact” failures** but *prevented attempts*.  
- Types become **operational boundaries**:  
  \[
  \Gamma \vdash t : A
  \]
  now reads as “`t` may be extended by history `Γ` without violating the co[2D[K
continuation discipline encoded in type `A`.”  

- Contexts (`Γ = x_1:A_1, …, x_n:A_n`) are interpreted not merely as a list[4D[K
list of assumptions but as an ordered record of **committed steps** that sh[2D[K
shape future extension possibilities.

#### Implications for Verification  

Consider a resource that may be consumed only once (e.g., file handles). Th[2D[K
The first successful application extends the history normally; any subseque[8D[K
subsequent attempt to reuse it meets Refusal because no admissible continua[8D[K
continuation exists. This uniform treatment allows verification tools to en[2D[K
enforce invariants by checking each continuation against historical constra[7D[K
constraints, rather than relying on domain‑specific runtime guards.

---

### 3. From Symbolic Replaces to Historical Continuation  

The shift from substitution to replay (and complemented by refusal) yields [K
several conceptual advantages:

1. **Traceability:** Every value carries its full provenance, enabling prec[4D[K
precise debugging and explanation.
2. **Incremental Computation:** Only the changed parts of a computation nee[3D[K
need reconstruction, preserving memory usage.
3. **Unified Type System:** Types encode admissibility rules directly, elim[4D[K
eliminating the separation between syntactic typing and semantic constraint[10D[K
constraints.
4. **Error Prevention:** Refusal eliminates “exception‑only” handling by bl[2D[K
blocking impossible steps early.

---

### 4. Summary  

- **Replay** replaces substitution with a *historical continuation* operati[7D[K
operation:  
  \[
  (v,H_v) \;\rightarrow\; H' = \operatorname{Replay}(H_f, H_v).
  \]  
- **Refusal** acts as an admissibility guard: if extending history `H` with[4D[K
with event `e` is not allowed, the computation stops (`Δ → Refuse(r)`).  

Together they turn computation from a sequence of isolated symbol replaceme[9D[K
replacements into a **dynamic construction of histories**, where every step[4D[K
step is recorded and can be revisited or verified. This view naturally acco[4D[K
accommodates incremental updates, verification mechanisms, and robust error[5D[K
error handling—all grounded in preserving the *history* rather than discard[7D[K
discarding it.

