#!/usr/bin/env bash
set -euo pipefail
export ARNMAP_RUN_INTEGRATION="${ARNMAP_RUN_INTEGRATION:-1}"
pytest -m integration "$@"
