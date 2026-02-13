# Candidate Prompt: Saved Search Alerts

## Context

Sentry already supports saved searches for Issues.  
Your task is to add a **small alerting layer** on top of saved searches.

## Goal

Implement per-user, in-app alerts for an Issue saved search:

1. A user can subscribe/unsubscribe to alerts for one of their saved searches.
2. A periodic worker (or a manually triggerable command used as a periodic worker) checks for "new" matching issues.
3. New matches produce in-app alert records for that user.
4. Alerts are visible in a small UI panel or challenge page.

## Required boundaries

1. In-app alerts only (database-backed).  
   Do not implement email/Slack/pager integrations.
2. Permission safety is mandatory.  
   A user must never receive an alert for a project they cannot access.
3. Idempotency is mandatory.  
   Running the worker twice for the same window must not create duplicates.
4. Performance awareness is mandatory.  
   Assume users can have up to 1,000 saved searches. Avoid obvious N-per-search query loops without justification.

## Timebox expectations

This is intentionally scoped for a partial but working vertical slice:

- a minimal data model,
- minimal API endpoints,
- minimal UI rendering,
- a worker path (or management command equivalent),
- at least one automated test around permission boundaries,
- a short design note.

## Definition of done

1. Candidate can subscribe and unsubscribe to a saved search alert.
2. Worker/command creates alert rows for new matches.
3. Candidate can view generated alerts in UI.
4. At least one test captures permission-safe behavior.
5. A short design note documents:
   - how "new" is defined,
   - how idempotency is enforced,
   - where permission filtering occurs,
   - known scalability limits and what would be improved next.

## Starter artifacts provided

- Seed data with:
  - two users (`candidate_user`, `other_user`),
  - two projects in a shared org (`project-a`, `project-b`),
  - one private project in a different org (`shadow-private`),
  - challenge saved searches owned by `candidate_user`.
- A starter failing test:
  `interview_challenge/tests/test_saved_search_alerts_permissions.py`

## Non-goals

- Do not redesign Sentry saved searches.
- Do not implement full event ingestion or analytics pipeline behavior.
- Do not optimize everything; prioritize correct boundaries and clear tradeoffs.
