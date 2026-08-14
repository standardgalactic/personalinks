**Key Points**

1. **Reachable Opportunity Volume (Ω(P))**  
   - Defined as the size of the cumulative reachable set \(R_n = \bigcup_{k[10D[K
\bigcup_{k=0}^{n} N(v_k)\).  
   - Unlike raw path length, Ω measures *future accessibility* rather than [K
distance traveled.

2. **Opportunity Expansion Theorem**  
   - If two traversals have equal length (\(|P_1| = |P_2|\)) but different [K
reachable volumes (Ω), the traversal with larger Ω admits a strictly larger[6D[K
larger space of future navigational continuations.

3. **Marginal Opportunity Contribution (ΔΩ(v))**  
   - Measures how much new territory is uncovered by visiting \(v\): \(\Del[6D[K
\(\Delta\Omega(v) = |N(v) \setminus R_n|\).  
   - A vertex’s informational value is thus proportional to its marginal op[2D[K
opportunity contribution, not just its degree.

4. **Two Geometries of the Graph**  
   - **Structural Geometry**: Fixed by the graph \(G=(V,E)\).  
   - **Navigational (Opportunity) Geometry** \(G_{\text{nav}}=(V,E,\mathcal[30D[K
\(G_{\text{nav}}=(V,E,\mathcal{T},\mathcal{W})\) depends on traversal histo[5D[K
history \(\mathcal{T}\). The weight update rule  

     \[
     w_{ij}(t)=\int_0^t e^{-(t-s)/\tau} f_{ij}(s)\,ds
     \]

     makes each edge’s value evolve with traversal frequency \(f_{ij}(s)\).[14D[K
\(f_{ij}(s)\).

5. **Frontier Dominance**  
   - For large \(n\), opportunity expansion rate is governed by the frontie[7D[K
frontier size:  

     \[
     \frac{d\Omega}{dn} \approx |\partial R_n| \cdot \bar p_{\text{novel}},[17D[K
p_{\text{novel}},
     \]

     where \(\bar p_{\text{novel}}\) is the probability a frontier vertex c[1D[K
connects to unexplored territory. Internal vertices contribute little after[5D[K
after their neighborhoods are fully explored.

6. **Exploration Under Partial Observability**  
   - The observer only knows an observed subgraph \(\mathcal{F}_n\). Transi[6D[K
Transition decisions must be based on local information and history.  

7. **Epistemic Value**  
   - Defined as the reduction in entropy due to a new vertex:  

     \[
     \mathcal{E}(v|\mathcal{F}_n)=H(\mathcal{F}_n)-H(\mathcal{F}_n\cup\{v\}[70D[K
\mathcal{E}(v|\mathcal{F}_n)=H(\mathcal{F}_n)-H(\mathcal{F}_n\cup\{v\}),
     \]

     where \(H\) is the Shannon entropy of the observed topology. This valu[4D[K
value changes with each traversal.

8. **Optimal Exploration Policy**  
   - An admissible policy maximizes expected information gain:  

     \[
     \pi^*=\arg\max_v \mathbb{E}[\Delta\Omega(v)|\mathcal{F}_n].
     \]

9. **Context Dependence (Proposition)**  
   - No globally optimal ordering of vertices exists because the epistemic [K
value depends on \(R_n\). History determines which vertex yields maximal ma[2D[K
marginal opportunity.

10. **Community Saturation (Corollary)**  
    - For any finite community \(C\), after a sufficiently large traversal [K
length \(n^*\), exploring further within \(C\) yields diminishing returns, [K
while expanding into neighboring unexplored regions provides higher expecte[7D[K
expected value.

**Conclusion**

The exploration problem is fundamentally *history‑dependent*. Optimal strat[5D[K
strategies must continually evaluate the current reachable frontier and mar[3D[K
marginal opportunity contributions, rather than following fixed rankings or[2D[K
or global distance metrics. This perspective reveals why sparse bridges (hi[3D[K
(high ΔΩ) often dominate exploratory value despite low local degree, emphas[6D[K
emphasizing that navigational information—rather than structural centrality[10D[K
centrality—is what drives cognitive expansion in complex networks.
