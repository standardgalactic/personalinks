**9. El axioma de irreversibilidad y espacios de opción**

La teoría contemporánea de la computación a menudo describe los sistemas co[2D[K
como configuraciones que cambian con el tiempo, pero muchos fenómenos cotid[5D[K
cotidianos muestran que esta descripción es incompleta: acciones humanas, i[1D[K
instituciones sociales e incluso sistemas técnicos dependen profundamente d[1D[K
del pasado que ha producido. La formalización de este pensamiento en Sphere[6D[K
Spherepop se logra mediante el **Axioma 9.1 (Irreversibilidad)**.

### Axioma 9.1 (Irreversibilidad)

Sea X el conjunto de espacios de opción del sistema. Para cualquier evento [K
irreversible e : X → X′ con X, X′ ∈ X, se cumple:

- **|X′| ≤ |X|**: El espacio de opciones después del evento no puede ser má[2D[K
más grande que antes.
- No existe ningún evento e⁻¹ tal que e⁻¹ ◦ e = id_X: Una vez que un evento[6D[K
evento ha ocurrido, su efecto es irreversíble; no se puede “deshacer” el ca[2D[K
cambio completo.

La composición de eventos H = en ○ ··· ○ e₁ : X₀ → Xₙ es irreversible como [K
historia completa. Esto significa que la secuencia de cambios acumulados (H[2D[K
(H) no puede revertirse a través de una secuencia inversa; cada evento perm[4D[K
permanentemente reduce o elimina opciones anteriores.

### Definición 9.2 (Espacio de opciones)

Un **espacio de opciones X** es un conjunto (puede ser finito o infinito) d[1D[K
de trayectorias futuras que son compatibles con todos los eventos que han o[1D[K
ocurrido en la historia hasta el momento presente. El espacio inicial X₀ re[2D[K
representa todas las posibilidades antes de cualquier cambio histórico.

### Ilustración gráfica

La figura 6 muestra cómo un conjunto inicial de espacios de opción X₀ se tr[2D[K
transforma a través de una secuencia de eventos irreversibles:

1. **X₀**: Todos los trayectorias futuras posibles antes del primer evento.[7D[K
evento.
2. **Eventos f₁ y f₂**: Eliminan algunas trayectorías debido a cambi[5D[K
cambios irrevocables (por ejemplo, construcción de carreteras que bloquean [K
rutas).
3. **Resultados activos**: Las trayectorias activadas después de los evento[6D[K
eventos irreversibles son X_H = {f₁, f₃, f₁₁, f₁₃, f₃₁, f₃₂}, representando[13D[K
representando las opciones viables en el futuro.

Esto ilustra cómo cada evento no sólo produce un resultado, sino que perman[6D[K
permanentemente transforma y reduce el conjunto de posibilidades futuras. E[1D[K
Este principio refleja la realidad práctica donde el pasado determina y lim[3D[K
limita las posibilidades actuales e inmediatas.

