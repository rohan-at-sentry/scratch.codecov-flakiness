#!/bin/bash
set -euo pipefail

with-tty() { script -q /dev/stderr "$@"; }

set -x
with-tty pytest



# vim:ft=bash:
