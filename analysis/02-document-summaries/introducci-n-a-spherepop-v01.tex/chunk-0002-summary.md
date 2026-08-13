**Resumen**

Spherepop es un marco teórico que busca capturar la naturaleza histórica de[2D[K
de muchos sistemas reales, incluyendo los cognitivos, computacionales y soc[3D[K
sociales. En lugar de definir estos sistemas únicamente por configuraciones[15D[K
configuraciones estáticas, Spherepop se centra en las trayectorias irrevers[8D[K
irreversibles (historias) que determinan su identidad y estructura.

**Puntos clave:**

1. **Historias de Eventos:**  
   - Definida como una secuencia ordenada de eventos irreversibles \(H = (e[2D[K
(e_1, e_2, \ldots, e_n)\).  
   - Alternativamente representable mediante una relación de orden parcial [K
\(H = (E_H, \prec)\) donde cada evento ocurre exactamente una vez y el orde[4D[K
orden refleja precedencia causal.  

2. **Espacios de Opción:**  
   - Representan los futuros compatibles con una historia dada.  
   - Inicial \(X_0\) y transformado por eventos irreversibles: \(e : X \rig[4D[K
\rightarrow X'\).  
   - Después de una secuencia de eventos \(H\), el espacio de opciones es \[1D[K
\(X_H = e_n(\cdots e_2(e_1(X_0))\cdots)\).

3. **Operadores Fundamentales:**  
   - Exclusión: elimina una posibilidad específica (\(popp (X) = X \setminu[8D[K
\setminus \{p\}\)).  
   - Negativa: restringe el espacio mediante una condición estructural (\(r[4D[K
(\(refuseR (X) = \{x \in X | x \notin R\}\)).  
   - Ligadura: introduce dependencia entre regiones del espacio (\(bind(X, [K
Y) = \{(x,y) | x \in X, y \in Y, C(x,y)\}\)).  
   - Colapso: identifica trayectorias equivalentes mediante una relación de[2D[K
de equivalencia (\(collapse(X) = X/\sim\)).

4. **Semántica de Pila:**  
   - La máquina computacional mínima asociada a Spherepop se describe media[5D[K
mediante una pila \(S = (X_1, X_2, \ldots, X_n)\).  
   - Un operador o actúa como transformación \(o : S \rightarrow S'\).  
   - Ejecución de un programa \(P = (o_1, o_2, \ldots, o_k)\) produce una s[1D[K
secuencia de estados de pila \(S_i+1 = o_i(S_i)\).

5. **Lógica como Restricción de Posibilidades:**  
   - Operaciones lógicas interpretadas como transformaciones geométricas so[2D[K
sobre espacios de opción:  
     - ¬A = X \ A (negación).  
     - A ∧ B = A ∩ B (conjunción).  
     - A ∨ B = A ∪ B (disyunción).

6. **Interpretación Categórica:**  
   - Los espacios de opción como objetos y eventos irreversibles como morfi[5D[K
morfismos en una categoría \(C\).  
   - Historia \(H = e_n \circ \cdots \circ e_1\) corresponde a composición [K
de morfismos.  

7. **Conexión con Event Sourcing:**  
   - Estado del sistema derivado a partir del historial de eventos registra[8D[K
registrados (\(s = f(L)\)).  
   - En arquitecturas distribuidas, múltiples registros pueden evolucionar [K
independientemente y fusionarse mediante operaciones de unión compatible co[2D[K
con orden causal.

**Conclusión**

Spherepop proporciona una formalización que enfatiza la naturaleza históric[8D[K
histórica e irreversible de los sistemas, permitiendo modelar procesos comp[4D[K
computacionales y sociales a través de historias de eventos y espacios de o[1D[K
opción dinámicos. Esta aproximación es particularmente útil para abordar si[2D[K
sistemas distribuidos donde la consistencia eventual se mantiene mediante l[1D[K
la acumulación y reconciliación de registros de eventos.

