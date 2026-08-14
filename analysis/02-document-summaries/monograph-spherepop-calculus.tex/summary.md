**Monograph: “SpherePop-Calculus” – A Unified Theoretical Object**

---

### 1. Thesis  
The monograph presents a categorical (higher‑order) semantics for **SPC**, [K
the Probabilistic Core Calculus. It situates the language’s type‑forming op[2D[K
operations—*Merge*, *Sphere*/*Pop* (abstraction/evaluation), and *Choice*—w[10D[K
*Choice*—within symmetric monoidal categories, thereby giving a uniform tre[3D[K
treatment of algebraic nondeterminism and categorical concurrency.

---

### 2. Primitives & Definitions  

| Concept | Categorical Description |
|---------|--------------------------|
| **Merge** | Tensor product \( \otimes \) in a symmetric monoidal category[8D[K
category (e.g., Cartesian products for SPC). Guarantees associativity, symm[4D[K
symmetry, and the required structure of an *abelian* monoidal category. |
| **Sphere / Pop** | Encoding currying: <br>• **Sphere** opens a scope (\(\[4D[K
(\(\lambda\)-abstraction) mapping \( \Gamma \vdash f : A \to B \mapsto \mat[4D[K
\mathrm{Sphere}(f): B^{A}\). <br>• **Pop** instantiates the scope, yielding[8D[K
yielding \( \mathrm{Pop}(\mathsf{Sphere}(f), a): B \). The adjunction mirro[5D[K
mirrors the internal hom in cartesian closed categories. |
| **Choice (Option B)** | Convex mixture of morphisms: for probability \(p [K
: \llbracket\Gamma\rbracket \to [0,1]\) and terms \(t,u\) of type \(A\), <b[2D[K
<br> \(\llbracket \mathrm{Choice}(p,t,u) \rrbracket = p \cdot \delta_{\llbr[13D[K
\delta_{\llbracket t\rangle} + (1-p)\cdot \delta_{\llbracket u\rangle}\). G[1D[K
Generalizes to finite distributions via a convex algebra structure. |
| **Distribution Monad** \(\mathcal{D}\) | Maps objects to probability meas[4D[K
measures; unit is the Dirac measure; Kleisli extension implements probabili[9D[K
probabilistic bind (monadic `Choice`). |

---

### 3. Formalism  

The semantics lives in the **presheaf topos** \( [\mathsf{Sphere}^{op}, \ma[3D[K
\mathsf{Set}] \):

* **Subobject classifier**: truth sphere (\(\Omega\)).  
* **Finite limits & colimits**: preserves Cartesian products and coproducts[10D[K
coproducts (e.g., disjoint unions).  
* **Exponentials**: propositions are subspheres, proofs are morphisms prese[5D[K
preserving truth.  

**Core clauses (denotational definitions):**

1. **Sphere**  
   \[
   \llbracket \mathrm{Sphere}(x{:}A.\,t) \rrbracket : \llbracket\Gamma\rbra[21D[K
\llbracket\Gamma\rbracket \to \llbracket A\rbracket \Rightarrow \llbracket [K
B\rbracket .
   \]

2. **Pop**  
   \[
   \llbracket \mathrm{Pop}(t,u) \rrbracket = \mathsf{ev} \circ \langle \llb[4D[K
\llbracket t \rrbracket , \llbracket u \rrbracket\rangle .
   \]

3. **Merge** (tensor product)  
   \[
   \llbracket \mathrm{Merge}(t,u) \rrbracket = \langle \llbracket t \rrbrac[7D[K
\rrbracket , \llbracket u \rrbracket\rangle .
   \]

---

### 4. Mechanisms  

* **Algebraic nondeterminism** via *Choice*: convex mixtures of branches re[2D[K
reflect independent probabilistic outcomes (Doom‑Aggregation Law).  
* **Categorical concurrency** via *Merge*: tensor product models parallel c[1D[K
computations, guaranteeing associativity and symmetry essential for a monoi[5D[K
monoidal structure.  
* **Currying & Application**: *Sphere/Pop* together encode the internal hom[3D[K
hom in cartesian closed categories, allowing function application inside th[2D[K
the probabilistic core.

---

### 5. Major Arguments  

1. **Uniform Representation** – By embedding SPC’s type‑forming operations [K
into symmetric monoidal categories, the semantics captures both determinist[11D[K
deterministic and probabilistic branching uniformly.  
2. **Semantic Soundness** – The denotational model respects typing derivati[8D[K
derivations (Context Lemma), reduction congruence (∼Merge) and substitution[12D[K
substitution properties, guaranteeing preservation of behavior under transl[6D[K
translation.  
3. **Adequacy & Conservativity** – For any SPC term \(e\) with type \(\tau\[7D[K
\(\tau\), its translation into the structured probabilistic calculus yields[6D[K
yields a denotation that commutes with the semantics:  
   \[
   \llbracket \mathcal{T}_{\mathrm{prob}\lambda}(e)\rrbracket = \mathcal{T}[11D[K
\mathcal{T}^{\mathcal{E}}(\llbracket e\rbrack),
   \]  
   preserving probability distributions.  

---

### 6. Dependencies Between Concepts  

* **Sphere ↔ Pop** – Adjunction ensures that abstraction and evaluation are[3D[K
are inverses, reproducing the β‑ and η‑laws of a cartesian closed category.[9D[K
category.  
* **Merge ↔ Choice** – Parallel composition (Merge) together with probabili[9D[K
probabilistic branching (Choice) yields product‑measure semantics for indep[5D[K
independent channels, enabling aggregation via Doom‑Aggregation Law:  
  \[
  \Pr[T_n=\mathsf{Doom}] = 1 - \prod_{i=1}^n (1-p_i).
  \]  
* **Distribution Monad** – Provides the carrier structure for probabilities[13D[K
probabilities; its unit (Dirac measure) and Kleisli extension formalize `Ch[3D[K
`Choice` as a Markov kernel.  

---

### 7. Implications  

* Enables compositional reasoning about probabilistic programs: independent[11D[K
independent hazards can be aggregated using *Merge* + logical disjunction ([1D[K
(`FoldOr`).  
* Guarantees preservation of type correctness, reduction behavior, and beha[4D[K
behavioral equivalence under translation—crucial for formal verification an[2D[K
and compiler design.  
* Offers a framework to extend SPC with additional modalities (e.g., resour[6D[K
resource constraints) by extending the monoidal structure while retaining c[1D[K
categorical semantics.

---

### 8. Unresolved Problems  

1. **Generalization** – Extending the semantics beyond finite probability s[1D[K
spaces requires handling infinite distributions, which may need further cat[3D[K
categorical tools (coends or locally presentable categories).  
2. **Equational Reasoning** – Proving confluence of reductions involving bo[2D[K
both *Choice* and *Merge* remains an open question; a complete equational t[1D[K
theory is needed for full semantic completeness.  

---

### 9. Internal Tensions  

* **Determinism vs. Probabilism** – While Merge captures deterministic para[4D[K
parallelism, Choice introduces nondeterministic branching that can conflict[8D[K
conflict with the purely sequential semantics of SPC’s core calculus unless[6D[K
unless explicitly modeled as independent events.  
* **Monoidal Structure Rigor** – Ensuring that *Merge* is a genuine tensor [K
product (not merely a coproduct) while preserving associativity and symmetr[7D[K
symmetry imposes constraints on how additional operators (e.g., resource‑aw[11D[K
resource‑aware monads) can be integrated without breaking existing theorems[8D[K
theorems.

---

### 10. Citations (as per fragment summaries)

- **Fragment 0001** – Merge as tensor, Sphere/Pop as exponentials, Choice a[1D[K
as convex mixture.
- **Fragment 0002** – Doom‑Aggregation Law, Merge + FoldOr for aggregation,[12D[K
aggregation, translation properties and adequacy.

These citations confirm that every claim retained is directly supported by [K
the fragment summaries provided.
