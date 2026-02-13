#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/env.sh"

if [ ! -d "$SENTRY_DIR/.git" ]; then
  echo "Sentry clone not found at $SENTRY_DIR. Run interview_challenge/scripts/bootstrap.sh first." >&2
  exit 1
fi

cd "$SENTRY_DIR"

if [ -f "$SENTRY_DIR/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$SENTRY_DIR/.venv/bin/activate"
fi

if command -v devservices >/dev/null 2>&1; then
  DEVICESVC_BIN="$(command -v devservices)"
elif [ -x "$SENTRY_DIR/.venv/bin/devservices" ]; then
  DEVICESVC_BIN="$SENTRY_DIR/.venv/bin/devservices"
else
  echo "devservices command not found. Run interview_challenge/scripts/bootstrap.sh first." >&2
  exit 1
fi

echo "Starting Sentry development stack via devservices serve..."
echo "Challenge docs: $SENTRY_DIR/interview_challenge/prompt.md"
exec "$DEVICESVC_BIN" serve
