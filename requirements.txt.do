#!/bin/bash
set -euo pipefail

set -x
redo-ifchange requirements.in

pip-compile --strip-extras -o-


# vim:ft=bash:
