#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  command -v python3.11 >/dev/null || { echo "Python 3.11 é necessário" >&2; exit 2; }
  python3.11 -m venv .venv
fi
.venv/bin/python -c 'import sys; assert sys.version_info[:2] == (3, 11), "Python 3.11 é necessário"'
.venv/bin/python -m pip install -r portal/requirements.txt
echo "Portal técnico: http://127.0.0.1:8080"
exec .venv/bin/python -m portal.run
