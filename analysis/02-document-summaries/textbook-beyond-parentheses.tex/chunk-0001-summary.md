**Replay and Refusal: A Historical View of Computation**

---

### 1. From Substitution to Replay  

Traditional symbolic computation replaces a formal parameter by an argument[8D[K
argument using **substitution**:

\[
(\lambda x.t)\;u \;\longrightarrow\; t[u/x].
\]

This operation is elegant because it turns function application into a pure[4D[K
purely syntactic transformation: the variable disappears, and evaluation pr[2D[K
proceeds as if the term had *always* denoted the supplied value.

**Spherepop’s observation:**  
Substitution hides the **history** that produced the argument. The transfor[8D[K
transformed expression no longer records how `v` came to be, only its curre[5D[K
current value.  

**Replay (the primitive operation):**  
Instead of inserting just `v`, replay inserts a pair \((v,H_v)\), where \(H[3D[K
\(H_v\) is the entire historical construction that generated `v`. Function [K
application then becomes:

\[
\operatorname{Replay}(H_f, H_v) = H',
\]

extending both histories into a larger computational narrative. The resulti[7D[K
resulting computation inherits provenance: identical values can be distingu[8D[K
distinguished by their distinct origins (e.g., from probabilistic sampling [K
vs. pure arithmetic).

---

### 2. What Happens When No Admissible Continuation Exists?  

While replay focuses on extending existing histories, **Refusal** governs t[1D[K
the *prevention* of inadmissible continuations.

#### Definition

Given a current history \(H\) and a proposed extension event \(e\), evaluat[7D[K
evaluate:

- If \(\operatorname{Adm}(H,e)\) holds → extend:  
  \[
  H \;\longrightarrow\; H \mathbin{\|} e.
  \]
- Otherwise (the continuation is inadmissible) → refuse:  
  \[
  H \;\longrightarrow\; \operatorname{Refuse}(r),
  \]
  where \(r\) records the reason for rejection.

#### Why This Matters  

1. **Failure as a Boundary, Not an Exception**  
   Traditional languages treat failure (exceptions, error codes) as *post‑h[7D[K
*post‑hoc* consequences of attempting an invalid computation. Spherepop tre[3D[K
treats refusal as a *preemptive* guard: the history itself never contains i[1D[K
inadmissible events.

2. **Types as Historical Boundaries**  
   A type judgment \(\Gamma \vdash t : A\) is read historically: it asserts[7D[K
asserts that extending the current context \(\Gamma\) with \(t\) remains wi[2D[K
within admissible continuations defined by \(A\). Thus types become operati[7D[K
operational boundaries rather than static value sets.

3. **Contexts as Histories**  
   The conventional context  

  \[
  \Gamma = x_1:A_1,\,x_2:A_2,\dots ,x_n:A_n
  \]

  is interpreted not merely as a list of assumptions but as an ordered reco[4D[K
record of admitted computational events. Future extensions inherit these co[2D[K
commitments and cannot invalidate them.

4. **Uniform Verification Foundation**  
   Resource constraints (e.g., “a resource may only be consumed once”) are [K
naturally expressed via refusal: the first successful consumption extends t[1D[K
the history, subsequent attempts meet a refusal because no admissible conti[5D[K
continuation exists. This unifies verification across domains—access contro[6D[K
control, protocol checking, dependent resources—all as boundary conditions [K
on historical extension.

---

### 3. Consequences for Computation  

- **Incremental Evaluation:** When parts of a computation change only sligh[5D[K
slightly, replay identifies and reconstructs the minimal portions whose dep[3D[K
dependencies have altered, leaving untouched regions valid.
  
- **Explanations at Historical Granularity:** Execution traces naturally be[2D[K
become explanations because they directly trace back to the original admiss[6D[K
admissible events that produced each value.

- **Persistence of Provenance:** Histories are preserved throughout executi[7D[K
execution. Identical numerical results from different origins remain distin[6D[K
distinguishable, enabling richer reasoning about data provenance and model [K
checking.

---

### 4. Summary  

Spherepop replaces substitution with replay, emphasizing that computation i[1D[K
is a *continuation* of historical construction rather than the mere manipul[7D[K
manipulation of isolated symbols. The complementary operation **Refusal** e[1D[K
ensures histories never contain inadmissible events, treating failure as a [K
safeguard against invalid extensions. Types and contexts acquire new meanin[6D[K
meanings as historical boundaries, unifying type‑checking, resource verific[7D[K
verification, and incremental compilation under a single conceptual framewo[7D[K
framework: *the preservation and extension of admissible histories*.
