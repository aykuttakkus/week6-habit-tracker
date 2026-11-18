# Starter — Habit Tracker

A tiny FastAPI + SQLite service for habits and daily check-ins. You'll add two features
on branches, open PRs, and run an AI reviewer.

## Setup
```bash
pip install -r requirements.txt
pytest
uvicorn main:app --reload   # http://localhost:8000  (docs at /docs)
```

## Guardrails

Run the complete deterministic quality gate from the repository root:

```bash
./scripts/quality-gate.sh
```

The script runs these checks in order:

```bash
python -m black --check .   # catches Python formatting drift
python -m ruff check .      # catches lint errors and unsorted imports
python -m pytest            # catches behavior regressions and failing tests
```

Any failing command returns a non-zero exit status and stops the quality gate. A controlled
failure demonstration is recorded in `artifacts/guardrail-failing-test.txt`; the temporary
failing test used for the demonstration was removed afterward.

## Endpoints
- `POST /habits` `{ "name": ... }`
- `GET /habits`
- `POST /habits/{id}/checkin` `{ "day": "2026-09-22" }`
- `GET /habits/{id}/checkins`
- `GET /habits/{id}/streak` — returns the habit name and its consecutive check-in days
  ending today; the streak is `0` when today has no check-in

## Files
- `main.py` — the app
- `test_main.py` — pytest suite
- `docs/TASKS.md` — the two features to implement
- `scripts/quality-gate.sh` — Black, Ruff, and pytest quality gate
- `artifacts/guardrail-failing-test.txt` — proof that a failing test blocks the gate
