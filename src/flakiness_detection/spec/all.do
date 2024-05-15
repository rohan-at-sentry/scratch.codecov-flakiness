#!/bin/bash
set -euo pipefail

with-tty() { script -q /dev/null "$@"; }

exec  >&2  # we only have log output
set -x
with-tty pytest



# vim:ft=bash:
