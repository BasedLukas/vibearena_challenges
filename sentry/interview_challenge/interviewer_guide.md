# Interviewer Guide

## Format options

### 45-minute live

1. 0-8 min: Candidate runs environment and asks clarifying questions.
2. 8-33 min: Candidate implements vertical slice.
3. 33-45 min: Candidate explains design and tradeoffs.

### 90-minute live

1. 0-15 min: Exploration + requirement clarification.
2. 15-65 min: Implementation.
3. 65-90 min: Test pass, design note, walkthrough.

## Pre-interview checklist

1. Run `./start_challenge.sh` on a fresh machine once.
2. Verify login works (`admin@sentry.io` / `admin`).
3. Verify seed script output reports projects/groups/searches.
4. Confirm prompt and rubric match your role level expectations.

## Interview script

1. Ask candidate to restate requirements in their own words.
2. Act as PM and answer requirement questions, but avoid giving implementation.
3. Ask where they enforce permissions and why there.
4. Ask their idempotency strategy.
5. Ask what they would change for 10x data volume.

## Strong signals

- Candidate identifies and defends a clear permission boundary.
- Candidate chooses an explicit cursor/newness definition and explains caveats.
- Candidate makes scoped, coherent changes rather than broad rewrites.
- Candidate uses tests to lock in critical invariants.

## Weak signals

- Candidate ignores authorization implications.
- Candidate cannot explain duplicate prevention.
- Candidate overfocuses on UI polish and ignores data correctness.
- Candidate cannot map changes to existing Sentry architecture.

## Debrief prompts

1. What did they optimize for under time pressure?
2. Did they ask clarifying questions before coding?
3. Did they make tradeoffs explicit?
4. What risks remain if this shipped today?
