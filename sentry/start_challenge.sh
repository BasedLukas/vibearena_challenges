#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)"

export CHALLENGE_HOST_ROOT="$ROOT_DIR"

"$ROOT_DIR/interview_challenge/scripts/bootstrap.sh"
"$ROOT_DIR/interview_challenge/scripts/run_all.sh"
