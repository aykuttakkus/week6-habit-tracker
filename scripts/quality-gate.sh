#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_root"

if [ -x ".venv/bin/python" ]; then
    python_cmd=".venv/bin/python"
else
    python_cmd="python"
fi

echo "[quality-gate] Black format check"
"$python_cmd" -m black --check .

echo "[quality-gate] Ruff lint check"
"$python_cmd" -m ruff check .

echo "[quality-gate] Pytest"
"$python_cmd" -m pytest

echo "[quality-gate] All checks passed."
