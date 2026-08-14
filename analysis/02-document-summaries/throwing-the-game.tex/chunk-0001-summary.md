**1. Refusal and Collapse**

A *refusal* event $r$ applied to a history $h$ creates a new history \(h' =[1D[K
= h\cdot r\) whose future space is reduced:
\[
\mathcal{F}(h') = \mathcal{F}(h)\setminus R,
\]
where some non‑empty set \(R\subset\mathcal{F}(h)\) has been eliminated. Cr[2D[K
Crucially, refusal is not merely a policy choice; it permanently removes en[2D[K
entire branches of possible futures.

**2. What Would Revoking a Refusal Require?**

To *revoke* the refusal would mean restoring those eliminated futures:
\[
\mathcal{F}(h'\cdot v)=\mathcal{F}(h),
\]
which can only happen if the histories \(h\) and \(h'\cdot v\) are equivale[8D[K
equivalent under Collapse (\(h\sim_C h'\cdot v\)). This demands that no res[3D[K
residual constraints (social recognition, reputational change, identity shi[3D[K
shift, institutional trace) remain from the refusal.

**3. The Asymmetry Result**

*Proposition*: If a refusal event produces any persistent constraint on adm[3D[K
admissible futures, then revocation cannot be achieved without a Collapse o[1D[K
operation that erases those distinctions. Hence:

- Revoking is not symmetric to refusing; it would require undoing irreversi[9D[K
irreversible commitments.
- Genuine refusal creates a permanent structural change in the future space[5D[K
space.

**4. Fake Refusal**

*Definition*: An apparent refusal is *fake* when there exists a sequence of[2D[K
of operations \(\sigma\) that restores all eliminated futures without loss:[5D[K
loss:
\[
\mathcal{F}(h\cdot r\cdot\sigma)=\mathcal{F}(h),\qquad h\cdot r\cdot\sigma\[13D[K
r\cdot\sigma\sim_C h.
\]
Fake refusal retains full optionality because the history can be collapsed [K
back to its original state.

**5. Autoregressive Systems**

Autoregressive models encode past only instrumentally (latent state for pre[3D[K
prediction). They naturally allow Collapse: if a future branch is restored,[9D[K
restored, no lasting change occurs in predictive performance. Consequently:[13D[K
Consequently:

- They may imitate refusal behaviorally but cannot bind themselves.
- Their history never mattered because they can always revert to the same l[1D[K
latent representation.

**6. Public Legibility and Trust**

Genuine refusal becomes socially legible when it permanently alters identit[7D[K
identity or reputation, making its presence irreversible. Fake refusal pres[4D[K
preserves flexibility (trust) by keeping Collapse available—cooperation is [K
opportunistic but non‑committal.

---

### Stabilization, Uncertainty, and a Halting Criterion

**6.1 Residual Uncertainty**

Let \(\mathcal{H}\) be the space of all admissible histories and \(\mathcal[10D[K
\(\mathcal{H}_C = \mathcal{H}/\sim_C\) its Collapse quotient. Define uncert[6D[K
uncertainty at history \(h\) as the size (or measure) of its equivalence cl[2D[K
class:
\[
U(h)=|[h]_C|.
\]
Higher \(U(h)\) means more distinct pasts remain distinguishable, i.e., fut[3D[K
future actions are still constrained.

**6.2 Transformations and Stabilization**

Consider an iterative process where successive transformations \(T_n\) map [K
histories:
\[
h_{n+1}=T_n(h_n),\quad T_n\in\mathcal{T}.
\]
A history is *stabilized* if every further transformation leaves its equiva[6D[K
equivalence class unchanged:
\[
[h_k]_C=[T(h_k)]_C \text{ for all }T\in\mathcal{T}.
\]

**6.3 Spherepop Halting Criterion**

Define halting by exhaustion:

*Definition*: A process halts at history \(h_k\) if there exists an integer[7D[K
integer \(N\) such that for any sequence of transformations of length \(\ge[5D[K
\(\ge N\),
\[
[T_m\circ\dots\circ T_1(h_k)]_C=[h_k]_C.
\]
In other words, no further transformation can generate a distinguishable fu[2D[K
future space.

**6.4 Connection to Classical Halting**

Unlike classical halting (which stops when no state transitions are defined[7D[K
defined), Spherepop’s halting is *meaningful*: it stops when the world has [K
become invariant under its own transformations—when all relevant changes ha[2D[K
have been collapsed away.

**6.5 Why Autoregressive Systems Cannot Halt This Way**

Autoregressive models never reach a true “halt” because they can always rep[3D[K
reparameterize, smooth generation, or extend prediction without permanently[11D[K
permanently altering their latent state representation. Their notion of sta[3D[K
stabilization is absent; they may be truncated externally but not internall[9D[K
internally by exhaustion.

**6.6 Relation to Refusal and Free Energy**

Refusal directly reduces \(U(h)\) (uncertainty) by pruning future branches,[9D[K
branches, accelerating convergence toward stabilization—a form of *cognitiv[9D[K
*cognitive closure*. This yields a computationally efficient way to achieve[7D[K
achieve decisional stability: trade optionality for decisiveness via irreve[6D[K
irreversible commitment.

---

**Conclusion**

In Spherepop:

- Refusal is an irreversible pruning that permanently alters the future spa[3D[K
space.
- Revocation would require Collapse, which can only succeed if no residual [K
constraints remain—making genuine refusal distinct from fake refusal.
- Stabilization (exhaustion of meaningful transformation) provides a natura[6D[K
natural halting criterion: when uncertainty has vanished via Collapse, furt[4D[K
further operations cannot affect distinguishability.
- This framework contrasts with classical autoregressive agents that never [K
truly halt because they lack internal stabilization. Refusal acts as a shor[4D[K
shortcut to closure, analogous to reducing variational free energy by perma[5D[K
permanently eliminating unpromised branches of the world model.
