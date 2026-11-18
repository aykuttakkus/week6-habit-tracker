# Week 6 Write-up — AI Code Review & Testing: Habit Tracker

Repository: <https://github.com/aykuttakkus/week6-habit-tracker>

## Guardrails

The repository uses a deterministic quality gate:

```bash
./scripts/quality-gate.sh
```

It runs these commands in order:

```bash
python -m black --check .
python -m ruff check .
python -m pytest
```

Black catches Python formatting drift. Ruff catches lint problems such as unused imports
and import-order issues. Pytest checks whether the expected application behavior still
works. A controlled failing test demonstrated that the quality gate exits with status 1
when one test fails, even if the other tests pass. The temporary failing test was removed
after the demonstration; the evidence is in
[`artifacts/guardrail-failing-test.txt`](artifacts/guardrail-failing-test.txt).

## PR 1 — Streak

- PR: [#1 Add habit streak endpoint and tests](https://github.com/aykuttakkus/week6-habit-tracker/pull/1)
- Feature commit: [`3078234`](https://github.com/aykuttakkus/week6-habit-tracker/commit/3078234ceff58e5d99a24a90c4c2825629857479)
- Documentation commit: [`c2abe68`](https://github.com/aykuttakkus/week6-habit-tracker/commit/c2abe68eec4ec90c249a5945776a5a9d2c713505)
- AI reviewer: Graphite Agent, [successful review check](https://app.graphite.com/github/pr/aykuttakkus/week6-habit-tracker/1)

The endpoint returns a habit's consecutive check-in days ending today. It returns zero
when today has no check-in, counts duplicate same-day check-ins once, ignores future and
malformed dates, and returns 404 for an unknown habit.

### Human review

The manual review confirmed that the backward date loop matched the streak behavior. It
found that `days_ago` was misleading when used with negative values, so it became
`day_offset`. It also found a missing malformed-date regression test and added it. Finally,
the response was changed to include `habit_name` because a numeric ID alone was not clear
for a person.

### AI review comparison

Graphite completed successfully and left zero actionable comments. The human review was
performed before the PR was opened and found three concrete improvements; Graphite reviewed
the corrected diff and found no additional issue.
For this PR, the human review was better at spotting the misleading name, the missing
regression test, and the unclear response shape. Graphite's value was an independent final
check after those issues were fixed, rather than finding an issue the human review missed.

Reviewing it myself made the system more understandable. Perhaps if it had been a large
system, there could have been ambiguity and faulty code could have been written.

## PR 2 — Weekly summary

- PR: [#2 Add weekly habit summary endpoint and tests](https://github.com/aykuttakkus/week6-habit-tracker/pull/2)
- Feature commit: [`8457219`](https://github.com/aykuttakkus/week6-habit-tracker/commit/8457219faaa822528737499286e6e6226f0193ea)
- AI reviewer: Graphite Agent, [successful review check](https://app.graphite.com/github/pr/aykuttakkus/week6-habit-tracker/2)

The endpoint returns the count of check-in records from today through the previous six
calendar days. It includes the habit name and the exact period boundaries, ignores future
and malformed dates, and returns 404 for an unknown habit.

### Human review

The manual review confirmed that today plus the previous six days is the intended seven-day
window. It supported moving common date cleanup into one helper so the streak and summary
features follow the same date rules. It also added `period_start` and `period_end` because a
count without its date range was not clear enough. A final review against the assignment
wording corrected the summary from counting distinct active days to counting check-in
records, including multiple records on the same day.

### AI review comparison

Graphite completed successfully and left zero actionable comments. The human review caught
the period-context issue and the task-wording mismatch before the PR was opened. Graphite
then reviewed the corrected diff without finding an additional issue.
For this PR, the human review was better at comparing the behavior with the instructor's
exact wording and explaining the date range. Graphite again provided an independent final
check, but it did not identify an additional problem in the corrected diff.

This time, in my own review, I paid more attention to whether the feature worked in the way
the instructor wanted. The AI review checked the final code again and showed that there was
no new problem.

## What I learned

It enabled the early detection of code that could later grow, become hard to understand and
find, and break the system.

It helped me change `days_ago` to `day_offset` and add `habit_name` because tests check
whether it works but do not measure variable naming or understandability.

AI review should not be trusted completely because there can be systematic or semantic
errors. It may also evaluate changed code against an older version of the system or not be
updated for the changed code. For this reason, it is definitely useful as a second check and
makes people faster.
