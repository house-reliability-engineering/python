#!/bin/bash

# This script should be run from a Python package
# root directory.

set -o errexit
set -o nounset

PYTHON=python3.11

$PYTHON -m pip \
  install \
  --quiet \
  poetry

$PYTHON -m poetry \
  install \
  --quiet \
  --with test

$PYTHON -m poetry \
  run \
  python -m unittest \
    --verbose
