**1.  What a “computational geodesic’’ is**

In differential geometry a *geodesic* is a curve on a manifold that locally[7D[K
locally minimizes distance (or, more generally, makes the action stationary[10D[K
stationary).  
When we speak of **computational geodesics** in Spherepop we replace “dista[6D[K
“distance” by the **action functional \(S[\gamma]\)** defined for a computa[7D[K
computational trajectory \(\gamma\):

* \(S[\gamma]=\sum_{t=0}^{n}\mathcal{L}_{t}(e_t,\Delta C_t,\Delta\Omega_t)\[20D[K
C_t,\Delta\Omega_t)\)  
  – each increment \(\mathcal{L}_t\) contains the *commitment cost* \(\Delt[7D[K
\(\Delta C_t\) (how much future accessibility is lost by popping a bubble) [K
and the *accessibility gain* \(\Delta\Omega_t\) (how much new evaluation ro[2D[K
routes become available).

A **computational geodesic** is therefore an admissible trajectory \(\gamma[8D[K
\(\gamma^*\in\mathcal{A}(X_0,X_n)\) that makes \(S[\gamma]\) stationary und[3D[K
under all *admissible variations*: any infinitesimal perturbation of the pa[2D[K
path (while keeping the start state \(X_0\) and final state \(X_n\) fixed, [K
and staying inside \(\mathcal{A}\)) cannot lower the total action. Mathemat[8D[K
Mathematically,

\[
\delta S[\gamma^*]=0\qquad\text{for all admissible }\delta\gamma .
\]

Because the variation is global (the whole trajectory must be unchanged), t[1D[K
the principle of stationary action captures not merely a local “greedy’’ ch[2D[K
choice but a *global optimality*: it balances early‑time commitment against[7D[K
against later‑time deferred evaluation.

---

**2.  Formulating the variational problem**

Let  

* \(X_0\) – the initial unreduced expression (full bubble topology \(\mathc[8D[K
\(\mathcal{B}_0\)).  
* \(X_n\) – the final fully reduced expression (empty bubbles).  

Define the **admissibility manifold** for an object \(X\),

\[
\mathcal{A}(X)=\{\gamma:\{0,\dots ,n\}\to\text{Admissible trajectories from[4D[K
from }X\}.
\]

The action functional is

\[
S[\gamma]=\sum_{t=0}^{n}
   \underbrace{\bigl(\Delta C_t + \lambda\Delta\Omega_t\bigr)}_{\text{local[41D[K
\lambda\Delta\Omega_t\bigr)}_{\text{local cost}}
   =\sum_{t}\mathcal{L}_t .
\]

The variational problem is:

\[
\boxed{
\gamma^*=\operatorname*{arg\,stationary}_{\gamma\in\mathcal{A}(X_0,X_n)} S[[2D[K
S[\gamma]
}
\tag{1}
\]

Solving (1) yields the **computational geodesic** \(\gamma^*\).  

---

**3.  Euler‑Lagrange equations in discrete form**

Because we work with a *discrete* action, the “Euler‑Lagrange’’ condition b[1D[K
becomes:

> For every admissible step \(e_t\) on \(\gamma^*\) there exists a local ba[2D[K
balance
> \[
> \Delta C_t^{(opt)} = f\bigl(\text{future accessibility gained at }t\bigr)[8D[K
}t\bigr),
> \]
> where the function \(f\) is determined by the *global* minimization of \([2D[K
\(S[\gamma]\).

In practice this translates into:

* **Early‑time bubbles**: pop only when it creates a structural shortcut (e[2D[K
(e.g., turning “\((a+b)c\)’’ into “\(ac+bc\)”) that reduces \(\Delta C_{t'}[6D[K
C_{t'}\) for later steps.  
* **Deferred‑evaluation bubbles**: postpone popping until the remaining exp[3D[K
expression is uniquely constrained, because popping earlier would incur unn[3D[K
unnecessary commitment.

These constraints are captured by a *variational constraint* on each step:

\[
\frac{\partial S[\gamma]}{\partial e_t}
   = \underbrace{\text{increase in }\Delta C_t}_{\text{commitment}} 
     - \underbrace{\text{decrease in future }\Delta\Omega_{t'}}_{\text{acce[31D[K
}\Delta\Omega_{t'}}_{\text{accessibility}}
     = 0 .
\]

---

**4.  Why the principle is not a “greedy’’ rule**

A greedy evaluator would always pop the *most convenient* expression at eve[3D[K
every step, ignoring later costs. The variational condition shows that:

* A trajectory may be locally cheaper (smaller \(\Delta C_t\)) but become g[1D[K
globally more expensive because it forces premature commitments.
* Conversely, a conservative trajectory can avoid immediate commitment yet [K
accumulate deferred‑evaluation cost later.

Thus the optimal strategy is *global*, not local: we must examine the whole[5D[K
whole path before deciding whether an admissible step improves the total ac[2D[K
action. This mirrors classical mechanics where stable equilibria are found [K
by stationary actions rather than by “minimum at every point’’ rules.

---

**5.  From geometry to semantics**

The analogy with **geodesics in physics** helps us interpret what a computa[7D[K
computational geodesic means semantically:

* **Initial and final states** correspond to the *semantic configuration sp[2D[K
space* of the expression: start = unreduced, end = fully reduced.
* The admissibility manifold \(\mathcal{A}(X)\) encodes all possible ways b[1D[K
bubbles could be popped while respecting the current bubble topology (the “[1D[K
“constraint structure’’).
* The action \(S[\gamma]\) measures total *structural commitment* plus *fut[4D[K
*future accessibility gain*.  
  Minimizing it is equivalent to minimizing future computational overhead: [K
we want the path that keeps evaluation routes open for as long as possible.[9D[K
possible.

Hence, a computational geodesic is a **semantically optimal reduction route[5D[K
route**—the “least structural commitment’’ trajectory through the configura[9D[K
configuration space of bubbles and constraints.

---

**6.  Concrete illustration – \(1+3\times2^2\)**

| Step | Expression before step | Bubble popped (local reason) | \(\Delta C[1D[K
C_t\) increase | Future accessibility gain \(\Delta\Omega_{t'}\) |
|------|------------------------|------------------------------|-----------|------|------------------------|------------------------------|--------------------------|-----------------------------------------------|
| 0    | \(1+3\times(2^2)\)    | **Exponentiation** → pop `\(2^2\)’’ to get[3D[K
get scalar value. | Low commitment (only a single multiplication). | Opens [K
path for linear combinations, reducing later multiplies. |
| 1    | \((1+12)\)            | **Addition** → pop the whole parenthetical[13D[K
parenthetical sum. | Still low (adds two numbers). | Creates a single large[5D[K
large number that can be used in future multiplications without extra paren[5D[K
parentheses. |
| 2    | \(13\)                | **Result** – no further bubble to pop. | N[1D[K
No new commitment needed. | Final state reached; cost minimized globally. |[1D[K
|

If we had popped the addition first, we would have created a single large t[1D[K
term \((1+3)=4\), forcing later multiplication by `\(2^2=4\)’’ (costly beca[4D[K
because it creates ambiguity). Conversely, popping exponentiation last forc[4D[K
forces us to multiply 3 and then repeatedly add 13, incurring higher commit[6D[K
commitment. The geodesic is exactly the order **Exponent → Addition** becau[5D[K
because this sequence makes \(S[\gamma]\) stationary.

---

### Summary

* A **computational geodesic** is an admissible trajectory that minimizes ([1D[K
(or makes stationary) the total action functional over all possible variati[7D[K
variations, analogous to a spacetime geodesic in physics.
* The variational problem (1) and its discrete Euler‑Lagrange conditions gi[2D[K
give us a *global* optimality criterion: balance early commitment against d[1D[K
deferred evaluation across the whole trajectory.
* This principle is called **least structural commitment**: it tells us why[3D[K
why greedy or overly conservative strategies can be suboptimal, and why und[3D[K
understanding computation requires knowledge of the full path—not just its [K
endpoints.
* Semantically, this corresponds to finding a *geodesic* through the config[6D[K
configuration space of bubbles and constraints, minimizing future accessibi[9D[K
accessibility loss while keeping evaluation routes open as long as possible[8D[K
possible.
