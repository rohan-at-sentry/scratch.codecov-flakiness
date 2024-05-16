#!/bin/bash
set -euo pipefail

set -x
redo-ifchange requirements.in

# there's one library we have vendored as a submodule -- it needed lots of
# patches
redo-ifchange .gitmodules vendor/*/pyproject.toml

pip-compile --strip-extras -o-


# vim:ft=bash:
