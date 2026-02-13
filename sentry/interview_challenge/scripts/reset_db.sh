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

make drop-db
make create-db
sentry django migrate --noinput

python - <<'PY'
from sentry.runner import configure

configure()

from django.db import router, transaction

from sentry.models.organization import Organization
from sentry.services.organization import organization_provisioning_service

if not Organization.objects.filter(slug="default").exists():
    with transaction.atomic(router.db_for_write(Organization)):
        org = Organization.objects.create(name="Default", slug="default")
    organization_provisioning_service.change_organization_slug(
        organization_id=org.id, slug=org.slug
    )
    org.handle_async_replication(org.id)
PY

seed_exit=0
python interview_challenge/scripts/seed_challenge.py \
  --seed-file interview_challenge/seed/challenge_seed.json || seed_exit=$?

python - <<'PY'
from sentry.runner import configure

configure()

from sentry.models import Organization, SavedSearch
from sentry.users.models.user import User

required_users = {"admin@sentry.io", "candidate_user", "other_user"}
present_users = set(User.objects.filter(username__in=required_users).values_list("username", flat=True))
missing_users = sorted(required_users - present_users)
if missing_users:
    raise SystemExit(f"Missing required users after seed: {missing_users}")

if not Organization.objects.filter(slug="challenge-org").exists():
    raise SystemExit("Missing challenge-org organization after seed.")

challenge_search_count = SavedSearch.objects.filter(name__startswith="[Challenge]").count()
if challenge_search_count < 20:
    raise SystemExit(
        f"Expected at least 20 challenge saved searches, found {challenge_search_count}."
    )
PY

if [ "$seed_exit" -ne 0 ]; then
  echo "Seed script exited with code $seed_exit, but seed validation passed." >&2
fi

echo "Database reset + challenge seed complete."
