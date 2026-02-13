#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/env.sh"

if [ ! -d "$SENTRY_DIR/.git" ]; then
  echo "Sentry clone not found at $SENTRY_DIR." >&2
  exit 1
fi

cd "$SENTRY_DIR"
# shellcheck disable=SC1091
source "$SENTRY_DIR/.venv/bin/activate"

exec sentry run web
