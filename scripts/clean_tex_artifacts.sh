#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_ROOT="${ROOT_DIR}/build/pdfs"
BUILD_ONLY=0

if [[ "${1:-}" == "--build-only" ]]; then
  BUILD_ONLY=1
fi

if [[ -d "${OUT_ROOT}" ]]; then
  find "${OUT_ROOT}" -type f ! -name '*.pdf' -delete
  find "${OUT_ROOT}" -type d -empty -delete
fi

if [[ "${BUILD_ONLY}" -eq 0 ]]; then
  find "${ROOT_DIR}" -type f \
    \( -name '*.aux' -o -name '*.bcf' -o -name '*.blg' -o -name '*.fdb_latexmk' -o -name '*.fls' -o -name '*.idx' -o -name '*.ilg' -o -name '*.ind' -o -name '*.lof' -o -name '*.log' -o -name '*.lot' -o -name '*.nav' -o -name '*.out' -o -name '*.run.xml' -o -name '*.snm' -o -name '*.synctex.gz' -o -name '*.toc' -o -name '*.vrb' -o -name '*.xdv' \) \
    ! -path "${ROOT_DIR}/.git/*" \
    ! -path "${OUT_ROOT}/*" \
    -delete
fi

echo "LaTeX artifact cleanup complete."
