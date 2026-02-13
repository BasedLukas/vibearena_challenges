#!/usr/bin/env bash

if [ -n "${CHALLENGE_HOST_ROOT:-}" ]; then
  CHALLENGE_ROOT="$(
    cd "$CHALLENGE_HOST_ROOT"
    pwd -P
  )"
  WORKDIR="${CHALLENGE_WORKDIR:-$CHALLENGE_ROOT/.challenge-workdir}"
  SENTRY_DIR="${SENTRY_DIR:-$WORKDIR/sentry}"
else
  SCRIPT_ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/../.."
    pwd -P
  )"
  CHALLENGE_ROOT="$SCRIPT_ROOT"
  if [ -d "$SCRIPT_ROOT/src/sentry" ] && [ -f "$SCRIPT_ROOT/Makefile" ]; then
    # Running inside the cloned Sentry repo.
    WORKDIR="${CHALLENGE_WORKDIR:-$SCRIPT_ROOT}"
    SENTRY_DIR="${SENTRY_DIR:-$SCRIPT_ROOT}"
  else
    WORKDIR="${CHALLENGE_WORKDIR:-$CHALLENGE_ROOT/.challenge-workdir}"
    SENTRY_DIR="${SENTRY_DIR:-$WORKDIR/sentry}"
  fi
fi

SENTRY_REPO_URL="${SENTRY_REPO_URL:-https://github.com/getsentry/sentry.git}"
SENTRY_REF="${SENTRY_REF:-26.1.0}"
SENTRY_COMMIT="${SENTRY_COMMIT:-faf322d6052a8fedb8813c1471949a701bfd49c7}"
CHALLENGE_BRANCH="${CHALLENGE_BRANCH:-interview/saved-search-alerts}"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

log_step() {
  printf "\n[%s] %s\n" "$1" "$2"
}
