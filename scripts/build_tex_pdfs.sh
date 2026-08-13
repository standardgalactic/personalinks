#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_ROOT="${ROOT_DIR}/build/pdfs"
SCRIPT_DIR="${ROOT_DIR}/scripts"
CLEAN_SCRIPT="${SCRIPT_DIR}/clean_tex_artifacts.sh"

if ! command -v lualatex >/dev/null 2>&1; then
  echo "error: lualatex is not installed or not in PATH" >&2
  exit 1
fi

mkdir -p "${OUT_ROOT}"

mapfile -d '' TEX_FILES < <(
  find "${ROOT_DIR}" -type f -name '*.tex' ! -path "${OUT_ROOT}/*" -print0 | sort -z
)

if [[ ${#TEX_FILES[@]} -eq 0 ]]; then
  echo "No .tex files found."
  exit 0
fi

echo "Compiling ${#TEX_FILES[@]} .tex files with lualatex..."

for tex_file in "${TEX_FILES[@]}"; do
  rel_path="${tex_file#${ROOT_DIR}/}"
  rel_dir="$(dirname "${rel_path}")"
  base_name="$(basename "${tex_file}")"
  stem="${base_name%.tex}"
  out_dir="${OUT_ROOT}/${rel_dir}"

  mkdir -p "${out_dir}"

  (
    cd "${ROOT_DIR}/${rel_dir}"
    echo "  -> ${rel_path}"
    lualatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory "${out_dir}" "${base_name}" >/dev/null
  )

  if [[ ! -f "${out_dir}/${stem}.pdf" ]]; then
    echo "error: expected output missing for ${rel_path}" >&2
    exit 1
  fi
done

"${CLEAN_SCRIPT}" --build-only

pdf_count="$(find "${OUT_ROOT}" -type f -name '*.pdf' | wc -l | tr -d ' ')"
echo "Done. Generated ${pdf_count} PDFs in ${OUT_ROOT}"
