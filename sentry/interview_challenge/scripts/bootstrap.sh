#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/env.sh"

require_cmd git
require_cmd docker
require_cmd devenv
require_cmd rsync

mkdir -p "$WORKDIR"

if [ ! -d "$SENTRY_DIR/.git" ]; then
  log_step "1/7" "Cloning getsentry/sentry into $SENTRY_DIR"
  git clone "$SENTRY_REPO_URL" "$SENTRY_DIR"
fi

cd "$SENTRY_DIR"

log_step "2/7" "Fetching tags and pinned revision"
git fetch --tags origin
if ! git cat-file -e "$SENTRY_COMMIT^{commit}" 2>/dev/null; then
  git fetch origin "$SENTRY_REF"
fi

if git rev-parse "$SENTRY_REF^{commit}" >/dev/null 2>&1; then
  ref_commit="$(git rev-parse "$SENTRY_REF^{commit}")"
  if [ "$ref_commit" != "$SENTRY_COMMIT" ]; then
    echo "Warning: $SENTRY_REF resolves to $ref_commit, expected $SENTRY_COMMIT." >&2
  fi
fi

if git show-ref --verify --quiet "refs/heads/$CHALLENGE_BRANCH"; then
  git switch "$CHALLENGE_BRANCH"
else
  git switch --create "$CHALLENGE_BRANCH" "$SENTRY_COMMIT"
fi

current_commit="$(git rev-parse HEAD)"
if [ "$current_commit" != "$SENTRY_COMMIT" ]; then
  echo "Warning: branch is not at pinned commit $SENTRY_COMMIT (current: $current_commit)." >&2
  echo "Continuing with current branch state." >&2
fi

log_step "3/7" "Syncing challenge materials into cloned Sentry repo"
mkdir -p "$SENTRY_DIR/interview_challenge"
rsync -a --delete "$CHALLENGE_ROOT/interview_challenge/" "$SENTRY_DIR/interview_challenge/"

log_step "4/7" "Running devenv sync (frontend-only mode to avoid migration deadlock)"
SENTRY_DEVENV_FRONTEND_ONLY=1 devenv sync

if [ ! -f "$SENTRY_DIR/.venv/bin/activate" ]; then
  echo "Expected virtualenv at $SENTRY_DIR/.venv was not created by devenv sync." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "$SENTRY_DIR/.venv/bin/activate"

if command -v devservices >/dev/null 2>&1; then
  DEVICESVC_BIN="$(command -v devservices)"
elif [ -x "$SENTRY_DIR/.venv/bin/devservices" ]; then
  DEVICESVC_BIN="$SENTRY_DIR/.venv/bin/devservices"
else
  echo "devservices command not found. Run devenv sync and ensure sentry .venv is healthy." >&2
  exit 1
fi

log_step "5/7" "Starting dependency services"
if ! "$DEVICESVC_BIN" up --mode migrations; then
  echo "devservices up --mode migrations failed; retrying with default devservices up." >&2
  "$DEVICESVC_BIN" up
fi

log_step "6/7" "Resetting database and seeding challenge data"
CHALLENGE_WORKDIR="$WORKDIR" SENTRY_DIR="$SENTRY_DIR" \
  "$SENTRY_DIR/interview_challenge/scripts/reset_db.sh"

log_step "7/7" "Bootstrap complete"
cat <<EOF

Challenge environment is ready in:
  $SENTRY_DIR

Next step (normally called by start_challenge.sh):
  interview_challenge/scripts/run_all.sh

Login credentials:
  admin@sentry.io / admin
  candidate_user / candidate
  other_user / other_user
EOF
