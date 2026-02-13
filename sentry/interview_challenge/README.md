# Interview Challenge: Saved Search Alerts

This challenge pack is designed for a 45-minute to 90-minute full-stack interview focused on:

- navigating a large production codebase,
- clarifying product requirements,
- making tradeoffs explicit,
- delivering a small vertical slice (DB + API + UI + background job).

## Setup command

From this repository root:

```bash
./start_challenge.sh
```

## Scope

Candidates implement **per-user in-app alerts** for an Issue saved search.  
Alerts should be generated periodically when new matching issues appear since the last check.

## Build checklist

- [x] Sentry pinned to an explicit revision (`26.1.0` / `faf322d6052a8fedb8813c1471949a701bfd49c7`)
- [x] One-command bootstrap (`./start_challenge.sh`)
- [x] DB reset + deterministic seed script (`interview_challenge/scripts/reset_db.sh`)
- [x] Seed fixture file with permission boundary data (`interview_challenge/seed/challenge_seed.json`)
- [x] Starter failing invariant test (`interview_challenge/tests/test_saved_search_alerts_permissions.py`)
- [x] Candidate prompt (`interview_challenge/prompt.md`)
- [x] Rubric (`interview_challenge/rubric.md`)
- [x] Interviewer runbook (`interview_challenge/interviewer_guide.md`)

## Notes for interviewers

- Keep the exercise focused on tradeoffs, not infra troubleshooting.
- Encourage requirement clarification with the interviewer acting as PM/manager.
- Grade reasoning quality and safety boundaries at least as much as "feature complete."

## Licensing note

This pack expects use in an internal/private interview process against a private fork.  
Confirm your legal/ops policy before redistributing a modified Sentry repository publicly.
