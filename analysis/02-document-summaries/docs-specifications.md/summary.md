**confluent(c: Config, ops: List[Operation]) → bool**

**Specification**

```
confluent(c, [op₁, op₂, …, opₙ]) = true ⇔
   ∃ result such that ∀ permutations π of ops:
      eval_program(c, π(ops)) = result
```

*In words*: The operation order is irrelevant – no matter how the list `ops[9D[K
list `ops` is permuted, evaluating them in any order from the initial confi[5D[K
configuration `c` always leads to the same final state (or error).  

**Complexity**

The check requires considering every possible ordering of the operations. F[1D[K
For a list of length *n* there are *n!* possible permutations, and each eva[3D[K
evaluation may take time *T*(eval) depending on how deep the resulting hist[4D[K
history is processed.

Thus the worst‑case runtime is **O(n! × T(eval))**, which grows factorially[11D[K
factorially with the number of operations – an exponential algorithm in ter[3D[K
terms of problem size.

**Behavior**

- Returns **true** only when all permutations produce identical results (or[3D[K
(or failures), otherwise returns **false**.
- Does **not** modify any configuration, authorize any particular ordering,[9D[K
ordering, or claim semantic validity if confluence fails.  
  *Non‑confluence ≠ error*; it merely signals that the system is order‑sens[10D[K
order‑sensitive.

---

