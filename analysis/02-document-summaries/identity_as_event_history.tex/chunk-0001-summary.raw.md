**Event Graphs and Directed Acyclic Structure**

**Definition – Event Graph**  
An *event graph* is a directed graph \(G = (V, \mathcal{E})\) where:

- The vertices \(V\) represent distinct regions or configurations of the sy[2D[K
system.
- Each directed edge \(X \rightarrow Y\) corresponds to an irreversible eve[3D[K
event that
  transforms the region \(X\) into the region \(Y\).

When a history involves branching (a single region giving rise to several
descendants) or merging (multiple regions combining into one), the graph na[2D[K
naturally
contains vertices with multiple outgoing edges (for branching) or incoming [K
edges
(for merging). The entire structure of the graph, not just a linear path, e[1D[K
encodes
the full generative history.

**Proposition – Directed Acyclicity**  
Every Spherepop event graph is a *directed acyclic graph* (DAG).

*Proof Sketch*: By definition in Section \(\ref{sec:categorical}\), events [K
are
irreversible transformations. If a cycle existed—i.e., there were a path
\(X \rightarrow Y \rightarrow \dots \rightarrow X\)—it would imply that the[3D[K
the same
region could be reached through a reversible sequence of events, contradict[10D[K
contradicting the
assumption of irreversibility. Hence no such cycles can appear in an event [K
graph,
making it acyclic.

**Implications**

1. **Parallel Histories**: Branching vertices allow simultaneous exploratio[10D[K
exploration of
   multiple potential futures without ambiguity, reflecting real-world proc[4D[K
processes
   where several outcomes are possible from a single state.
2. **Historical Clarity**: The DAG structure prevents misinterpretation tha[3D[K
that could
   arise if one attempted to collapse the graph into an arbitrary linear or[2D[K
order,
   preserving the causal directionality inherent in irreversible events.
3. **Structural Constraints**: In practice, many physical or computational [K
systems
   exhibit non‑linear dynamics (e.g., bifurcations, feedback loops). By enf[3D[K
enforcing a
   DAG structure for event graphs, Spherepop aligns with these constraints [K
while
   maintaining a compositional framework that remains consistent across all[3D[K
all events.

Thus, the use of directed acyclic event graphs naturally captures the essen[5D[K
essential
property of irreversibility in Spherepop histories and provides a robust vi[2D[K
visual
and computational model for analyzing complex generative processes.

