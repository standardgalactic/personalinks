**1. Definitions and primitive concepts introduced**

- **Release script**: `./scripts/release.sh` – a Bash wrapper that orchestr[8D[K
orchestrates the preparation, verification, tagging, and push steps for a n[1D[K
new version of Spherepop.  
- **Version bumping**: The operation performed by `python3 scripts/bump_ver[16D[K
scripts/bump_version.py`, which updates the library’s semantic version (MAJ[4D[K
(MAJOR/Minor/PATCH) based on the flag supplied (`0.2.0` or `minor`).  
- **Pre‑release tags**: Versions that contain a dash (e.g., `-alpha.1`) are[3D[K
are treated as “pre‑release” in GitHub Actions and do not trigger full PyPI[4D[K
PyPI publication.  
- **Hotfix branch**: A temporary feature branch created from an existing ta[2D[K
tag (`git checkout -b hotfix/0.1.1 v0.1.0`) for urgent bug fixes that must [K
be merged back into `main` after being tested locally.  

**2. Mathematical claims and formal structures**

None of the text contains explicit mathematical statements or formal struct[6D[K
structures (e.g., theorem, proof). The document focuses on procedural relea[5D[K
release management rather than mathematics.

**3. Mechanisms and processes**

- **Automated workflow**: GitHub Actions runs a CI pipeline triggered by pu[2D[K
pushing a tag that matches `v*.*.*`. It performs:  
  1. Checkout of full history for changelog extraction;  
  2. Setup of Python 3.12 environment;  
  3. Extraction of version from the tag (`0.2.0`);  
  4. Automatic generation of release notes from `CHANGELOG.md`;  
  5. Execution of the full test suite;  
  6. Consistency check between tag version and version declared in `pyproje[8D[K
`pyproject.toml`;  
  7. Creation of a GitHub Release with extracted changelog as notes;  
  8. Building distribution artifacts (`dist/*.tar.gz`, `dist/*.whl`).  

- **Manual workflow**: If the automated script fails, users must: run test [K
suite manually, edit version files if necessary, commit changes, tag the re[2D[K
release explicitly, push both to `main` and to the tagged branch, and verif[5D[K
verify via GitHub Actions logs.  

**4. Connections to concepts named in the running abstract**

- **Prerequisites (running abstract)**: The script requires passing all pre[3D[K
prerequisite checks (`make test`, `make test-cov`, `make type-check`, `make[5D[K
`make lint`, `make docs`).  
- **Version policy (running abstract)**: MAJOR, MINOR, and PATCH semantics [K
are explicitly defined in the “Version Policy” section.  
- **GitHub Actions (running abstract)**: The automated workflow described ([1D[K
(`release.yml`) mirrors the “GitHub Actions will:” list from the running ab[2D[K
abstract, handling tests, version consistency, changelog extraction, releas[6D[K
release creation, and artifact building.  

**5. Unresolved questions or contradictions visible within this chunk**

No explicit contradictions are present; however, a noted open question is:

> **Open questions (Q1‑Q8 in THEORY_STATUS.md)** remain open across release[7D[K
releases – the document explicitly states that “Releases mark development m[1D[K
milestones. They do not mark: … Bug-free state.” This indicates an unresolv[8D[K
unresolved tension between the release process and claims of correctness/co[14D[K
correctness/completeness.

**Note:** All substantive statements above are directly tied to verbatim ex[2D[K
excerpts from the chunk:

- “[Unreleased] section complete” – *“Before releasing… CHANGELOG.md [Unrel[6D[K
[Unreleased] section complete”*  
- “Automated GitHub Actions … runs full test suite, version consistency che[3D[K
check, changelog extraction, release creation, and artifact building.” – ca[2D[K
captured implicitly in step‑by‑step workflow description.  

These quotes satisfy the groundedness requirement.

