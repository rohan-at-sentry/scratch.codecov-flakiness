#!/bin/bash
set -euo pipefail
exec >&2  # we're not building a file from stdout

set -x
redo-ifchange requirements.txt

python3.12 -m venv --upgrade-deps venv
./venv/bin/pip install pip-tools
./venv/bin/pip-sync


./venv/bin/pre-commit install
touch venv/

# vim:ft=bash:
