#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v doxygen >/dev/null 2>&1; then
  echo "Error: doxygen is not installed or not on PATH." >&2
  echo "On macOS: brew install doxygen graphviz" >&2
  exit 1
fi

echo "Generating Doxygen docs..."
mkdir -p build/docs
project_version=""
if command -v uv >/dev/null 2>&1; then
  project_version="$(uv version --short 2>/dev/null || true)"
fi

tmp_doxyfile="build/Doxyfile.generated"

if [[ -n "${project_version}" ]]; then
  echo "Using project version: ${project_version}"
  # Doxygen doesn't reliably expand environment variables in config across versions,
  # so we generate a temporary config with PROJECT_NUMBER inlined.
  sed -E "s|^PROJECT_NUMBER[[:space:]]*=.*$|PROJECT_NUMBER         = \"${project_version}\"|" \
    docs/Doxyfile >"${tmp_doxyfile}"
else
  echo "Warning: could not determine project version via 'uv version --short'." >&2
  cp docs/Doxyfile "${tmp_doxyfile}"
fi

doxygen "${tmp_doxyfile}"

echo "Done. Open: build/docs/html/index.html"
