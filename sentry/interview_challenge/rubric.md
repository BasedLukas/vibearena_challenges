# Rubric

Score each category from 1 to 5.

## 1) Problem framing and requirement clarification

- 1: Implements quickly without clarifying behavior or edge cases.
- 3: Clarifies some assumptions (for example definition of "new").
- 5: Proactively clarifies user intent, constraints, and tradeoffs before coding.

## 2) Codebase navigation and leverage

- 1: Creates ad-hoc patterns, ignores existing conventions.
- 3: Reuses some existing patterns but with inconsistencies.
- 5: Follows existing Sentry patterns for models, endpoints, authz, and tests.

## 3) Permission safety

- 1: Permission leaks possible.
- 3: Permission checks exist but are brittle or poorly placed.
- 5: Explicitly enforces project/org access boundaries and validates with tests.

## 4) Idempotency and correctness

- 1: Duplicate alerts likely and semantics unclear.
- 3: Partial duplicate protection but edge cases unaddressed.
- 5: Strong duplicate protection (constraints/transactional logic) and clear semantics.

## 5) Performance and scaling awareness

- 1: Naive per-search loops with no discussion.
- 3: Some batching or indexing awareness.
- 5: Makes deliberate query-shape decisions and explains scaling path to 1,000+ searches.

## 6) Vertical slice completeness

- 1: Incomplete implementation with unclear boundaries.
- 3: Mostly complete but fragile integration points.
- 5: Usable DB + API + UI + worker flow in timebox, with reasonable scope control.

## 7) Communication quality

- 1: Can not explain design choices.
- 3: Explains what was built, but little rationale.
- 5: Clear rationale, risks, alternatives, and next steps.

## Overall interpretation

- 30+: Strong mid-level/full-stack signal.
- 22-29: Hire discussion, depends on role needs and growth trajectory.
- <22: Gaps in ownership, safety, or navigation for this role level.
