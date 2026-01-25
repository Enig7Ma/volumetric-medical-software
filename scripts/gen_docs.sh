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
doxygen docs/Doxyfile

echo "Done. Open: build/docs/html/index.html"
