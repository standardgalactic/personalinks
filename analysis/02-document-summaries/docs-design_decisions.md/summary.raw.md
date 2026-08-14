**Theoretical Synthesis: docs-design_decisions.md**

---

### 1. Thesis  
The document codifies design‑decision rules that shape the technical archit[6D[K
architecture of the project around three guiding principles:

| Principle | Manifestation |
|-----------|----------------|
| **Hardware Independence (OVERSOUL §9)** | Performance benchmarks are expr[4D[K
expressed as *structural scaling* functions rather than raw wall‑clock time[4D[K
time. This isolates algorithmic complexity from machine‑specific clock spee[4D[K
speeds, enabling reproducible performance analysis across diverse hardware [K
generations. |
| **Speed of Local Development** | MyPy static type checking is limited to [K
the CI pipeline; local pre‑commit hooks run only on formatting and syntax c[1D[K
checks. This preserves rapid iteration cycles while preserving safety guara[5D[K
guarantees for global merges. |
| **Future‑Ready Compatibility** | Both Python 3.12 and 3.13 are required a[1D[K
as supported interpreter versions, ensuring access to modern language featu[5D[K
features (e.g., native union types) without sacrificing broader community s[1D[K
support. |

---

### 2. Primitives / Definitions  

1. **Structural Scaling Function**  
   \[
   T(|h|,\;|O|,\;k,\;b)=\text{complexity derived from history length }|h|,\[6D[K
}|h|,\\
   \text{option‑space cardinality }|O|,\\
   \text{observational horizon }k,\\
   \text{branching factor }b.
   \]  
   - **\( |h| \)**: Length of the problem’s historical context.  
   - **\( |O| \)**: Cardinality of all possible decisions/options.  
   - **\( k \)**: Horizon over which observability is required (e.g., numbe[5D[K
number of steps to look ahead).  
   - **\( b \)**: Maximum branching per decision node.

2. **Pre‑commit Hook Policy**  
   - *Local phase*: Enforces basic linting, formatting (`ruff`, `black`).  [K

   - *CI phase*: Executes full type checking with MyPy (ensuring no regress[7D[K
regressions survive the whole pipeline).

3. **Python Version Policy**  
   - Supported interpreters: Python ≥ 3.12 (including 3.13).  
   - Rationale: Aligns with August‑2026 release window, leverages new langu[5D[K
language features introduced in Python 3.10+, and future‑proofs against dep[3D[K
deprecation warnings.

---

### 3. Formalism  

The formal description of the benchmarking metric is:

\[
T(|h|,\;|O|,\;k,\;b) = f_{\text{alg}}(h,O,k,b)
\]

where \(f_{\text{alg}}\) captures algorithmic complexity (e.g., Big‑O notat[5D[K
notation adjusted by empirical scaling factors observed in CI runs).  

The decision to use **structural scaling** over raw wall‑clock time is form[4D[K
formalized as:

- **Benchmark Metric**:  
  \[
  B = T(|h|,\;|O|,\;k,\;b) \quad\text{instead of}\quad C_{\text{wall}}.
  \]  

Thresholds (sanity checks) are defined per target problem size, e.g., for 1[1D[K
10 000 options:

- **Acceptable latency**: \(3–5\) ms.  
- For 100 history operations: \(2–3\) ms.

---

### 4. Mechanisms  

1. **Structural Scaling Measurement**  
   - Implemented in `tests/test_performance.py`.  
   - Stores both raw wall‑clock time and the derived scaling value, allowin[7D[K
allowing regression detection independent of hardware speed.

2. **Pre‑commit Hook Enforcement**  
   - Defined via `.pre-commit-config.yaml` with a comment explaining MyPy’s[6D[K
MyPy’s exclusion from local runs.  
   - CI workflow (`lint.yml`) triggers type checking after all formatting c[1D[K
checks pass:

   ```yaml
   name: Type check with mypy
   group: ‘Pre-commit verification’
   run: make type-check
   ```

3. **Python Version Matrix**  
   - `pyproject.toml` enforces required interpreter versions:

   ```toml
   [project]
   requires-python = ">=3.12"
   ```

   - CI strategy uses matrix deployment for both Python 3.12 and 3.13, ensu[4D[K
ensuring all tests run on each supported version.

---

### 5. Major Arguments  

| Argument | Supporting Evidence |
|----------|---------------------|
| **Hardware Independence** (DDR‑009) | Over SOUL §9 mandates structural sc[2D[K
scaling to avoid correlation with clock speed variations across hardware ge[2D[K
generations. |
| **Speed of Development vs Safety** (DDR‑010) | MyPy’s latency (~3–5 s per[3D[K
per run) makes it impractical locally; early detection is reserved for CI w[1D[K
where all checks are enforced, preserving rapid iteration cycles and develo[6D[K
developer productivity. |
| **Future Compatibility** (DDR‑011) | Python 3.13 introduces new safety fe[2D[K
features and language enhancements that must be supported to prevent deprec[6D[K
deprecation warnings later in the project lifecycle. |

---

### 6. Dependencies Between Concepts  

- **Structural Scaling ↔ Benchmarking**: The choice of a scaling metric dir[3D[K
directly impacts how performance regressions are identified; without it, be[2D[K
benchmark results would be hardware‑biased.
- **Pre‑commit Hooks ↔ MyPy Integration**: Enforcing type checks only in CI[2D[K
CI ensures that local commits remain fast (no MyPy overhead) while guarante[8D[K
guaranteeing global safety. This dependency is reflected in the hook config[6D[K
configuration and CI workflow ordering.
- **Python Version Policy ↔ Structural Scaling & Pre‑commit**: Supporting b[1D[K
both Python 3.12/13 enables developers to run full test suites on their own[3D[K
own machines, aligning with the hardware‑independent benchmarking approach.[9D[K
approach.

---

### 7. Implications  

1. **Technical Reproducibility** – All performance analyses become reproduc[8D[K
reproducible across different compute environments because they are express[7D[K
expressed in terms of structural variables.
2. **Developer Experience** – Local workflow remains snappy; only catastrop[9D[K
catastrophic type errors surface during CI, reducing friction for rapid pro[3D[K
prototyping.
3. **Maintenance & Future‑Readiness** – Supporting both 3.12 and 3.13 precl[5D[K
precludes deprecation issues down the line, allowing the project to leverag[7D[K
leverage language features introduced after August 2026.

---

### 8. Unresolved Problems  

- **Threshold Calibration**: Determining optimal latency bounds for differe[7D[K
different problem spaces (e.g., high‑dimensional option spaces) remains emp[3D[K
empirical and may require additional benchmark data.
- **CI Resource Consumption**: Running tests on both Python versions double[6D[K
doubles CI build time; investigating parallelizable test suites could mitig[5D[K
mitigate this cost without compromising coverage.

---

### 9. Internal Tensions  

| Tension | Description |
|---------|-------------|
| **Speed vs Safety** (DDR‑010) | Balancing rapid local commits against the[3D[K
the safety guarantees provided by MyPy creates a trade‑off between develope[8D[K
developer ergonomics and code quality assurance. |
| **Hardware Independence vs Resource Cost** (DDR‑009) | While hardware ind[3D[K
independence is desirable, it incurs higher CI resource usage; future cost/[5D[K
cost/benefit analysis may be needed if scaling metric introduces additional[10D[K
additional overhead not justified by reproducibility gains. |

---

### 10. References  

- Over SOUL §9 – Guiding principle for algorithmic complexity measurement.
- DDR‑009 (Structural Scaling) – Detailed description of the benchmarking f[1D[K
function and threshold definitions.
- DDR‑010 (Pre‑commit Hooks) – Configuration and rationale for limiting MyP[3D[K
MyPy to CI environment.
- DDR‑011 (Python Version Policy) – Rationale for supporting Python 3.12+ b[1D[K
based on language feature timeline.

--- 

**End of Synthesis**

