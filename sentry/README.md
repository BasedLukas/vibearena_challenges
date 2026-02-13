# Sentry Interview Challenge Pack

This repository contains a runnable interview harness for a mid-level full-stack challenge based on `getsentry/sentry`.

## One-command start

```bash
./start_challenge.sh
```

That command will:

1. Clone `getsentry/sentry` into `.challenge-workdir/sentry` if needed.
2. Pin to Sentry `26.1.0` (`faf322d6052a8fedb8813c1471949a701bfd49c7`).
3. Create/switch to branch `interview/saved-search-alerts`.
4. Run `devenv sync`.
5. Start dependency services (`devservices`).
6. Reset database and seed challenge data.
7. Start the development stack via `devservices serve`.

## Prerequisites

- Docker
- Git
- `devenv` (from [getsentry/devenv](https://github.com/getsentry/devenv))
- `devservices`

## Candidate credentials after bootstrap

- `admin@sentry.io` / `admin` (created by `make reset-db`)
- `candidate_user` / `candidate`
- `other_user` / `other_user`

## Challenge materials

- Prompt: `interview_challenge/prompt.md`
- Rubric: `interview_challenge/rubric.md`
- Interviewer runbook: `interview_challenge/interviewer_guide.md`
- Design note template: `interview_challenge/design_note_template.md`
