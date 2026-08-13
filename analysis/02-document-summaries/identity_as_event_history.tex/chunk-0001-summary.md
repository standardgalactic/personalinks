**Event Graphs and Directed Acyclic Structure**

Linear event words work well for histories where each event has at most one[3D[K
one predecessor and at most one successor. However, many real-world process[7D[K
processes involve branching (a single region giving rise to multiple descen[6D[K
descendants) or merging (multiple regions combining into a new one). In suc[3D[K
such cases the linear notation becomes inadequate because it hides the para[4D[K
parallel structure of the history.

**Definition – Event Graph**

An *event graph* is a directed graph \(G = (V, \mathcal{E})\) where:

- **Vertices (\(V\))**: Represent regions or configurations of a system.
- **Edges (\(\mathcal{E}\))**: Represent irreversible events. An edge from [K
vertex \(X\) to vertex \(Y\) denotes that event producing the region \(Y\) [K
from the region \(X\).

When an event produces multiple descendants, its corresponding vertex will [K
have several outgoing edges; similarly, if a new region is formed by mergin[6D[K
merging two others, there will be incoming edges representing those contrib[7D[K
contributions.

**Proposition – Directed Acyclicity**

Every Spherepop event graph is a *directed acyclic graph* (DAG).

**Why Directed Acyclic?**

1. **Irreversibility**: By definition, each edge in a Spherepop event graph[5D[K
graph corresponds to an irreversible transformation. If cycles were allowed[7D[K
allowed—paths that eventually return to the original region—an inverse proc[4D[K
process would be implied, contradicting irreversibility.

2. **No Reversible Loops**: In causal or computational systems modeled by S[1D[K
Spherepop, no sequence of events can reverse itself. A loop (e.g., \(X \rig[4D[K
\rightarrow Y \rightarrow \dots \rightarrow X\)) would imply a reversible s[1D[K
step, which is prohibited under the underlying physical or computational as[2D[K
assumptions.

3. **Structural Consequence**: The requirement that each event be irreversi[9D[K
irreversible inherently prevents cycles because a cycle would require an in[2D[K
inverse transformation at some point in the sequence, violating the irrever[7D[K
irreversibility constraint.

This property (directed acyclicity) is not merely a convenient representati[12D[K
representation but a structural necessity derived from the core assumptions[11D[K
assumptions of Spherepop. It aligns with broader principles observed in cat[3D[K
category theory and graph theory for systems where morphisms represent irre[4D[K
irreversible processes.

