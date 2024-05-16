#!/bin/bash
set -euo pipefail
set -x
: ARGV: "$@"

git submodule update --init
if [[ "$1" =~ \* ]]; then
  eval "redo-ifchange $1"
fi


# vim:ft=bash:
