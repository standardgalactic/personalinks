**1. Definitions and primitive concepts introduced**

- **Historias (histories)** – Ordered sequences of irreversible events that[4D[K
that change the set of possible future states (“espacios de opciones”).  
  *Source: “Las historias son secuencias ordenadas de eventos (morfismos) q[1D[K
que modifican el espacio de opciones correspondiente al sistema.”*

- **Espacios de Opciones** – Formento conjunto de trayectorias futuras posi[4D[K
posibles del sistema.  
  *Source: “Un objeto en la categoría Sph corresponde a un espacio de opcio[5D[K
opciones, es decir, un conjunto de trayectorias futuras posibles del sistem[6D[K
sistema.”*

- **Morfismos (eventos)** – Irreversible transformations that reduce the nu[2D[K
number of compatible trajectories in an option space.  
  *Source: “Cada evento representa un cambio irreversible en el estado del [K
mundo.”*

**2. Mathematical claims and formal structures**

- The model uses a category \( \mathbf{Sph} \) where objects are option spa[3D[K
spaces and morphisms encode event‑induced reductions of those options.  
  *Source: “Las historias se interpretan como secuencias de eventos que tra[3D[K
transforman espacios de opciones (conjuntos posibles de resultados).”*

- Composition of histories is given by the categorical composition \( e_2 \[1D[K
\circ e_1 \), preserving temporal order and thus structural properties such[4D[K
such as associativity.  
  *Source: “La composición de historias (`e2 ∘ e1`) captura la secuencialid[12D[K
secuencialidad temporal de eventos, permitiendo describir procesos que evol[4D[K
evolucionan paso a paso.”*

- Identity morphisms \( \mathrm{id}_X \) represent the trivial history with[4D[K
with no change.  
  *Source: “La identidad categórica (`idX`) representa la historia trivial [K
donde no ocurre ningún cambio.”*

**3. Mechanisms and processes**

- **Irreversibility & Entropy:** Each event corresponds to a Landauer‑type [K
irreversible information erasure, implying an associated energy cost \( kT\[3D[K
kT\ln 2 \).  
  *Source: “Cada operación pop puede interpretarse como una reducción de op[2D[K
opción que disipa al menos \(kB T\ln 2\) de energía libre.”*

- **Event Structures:** The formalism aligns with Glynn Winskel’s event‑str[9D[K
event‑structure semantics, where concurrent events are modeled by intersect[9D[K
intersections of option spaces.  
  *Source: “Enseñan a la teoría de estructuras de eventos (Winskel, 1987) q[1D[K
que concurrencia se modela mediante intersecciones de espacios de opciones.[9D[K
opciones.”*

**4. Connections to broader themes**

- The framework bridges **category theory**, **type theory**, and **distrib[9D[K
**distributed systems** by providing a mathematically rigorous description [K
of concurrent computations via event structures.  
  *Source: “Marc Shapiro et al.’s CRDT work (2011) shows how these ideas ex[2D[K
extend to conflict‑free replicated data types.”*

- It also relates to **information theory** through Shannon’s notion that e[1D[K
each irreversible step corresponds to a minimum entropy change, justifying [K
the energy‑cost claim.  
  *Source: “Claude E. Shannon’s 1948 communication theory connects informat[8D[K
information loss with physical entropy constraints.”*

These points collectively establish how histories, option spaces, and morph[5D[K
morphisms form an underlying algebraic structure capable of modeling both a[1D[K
abstract computational processes and concrete physical realities such as co[2D[K
computation and thermodynamics.
