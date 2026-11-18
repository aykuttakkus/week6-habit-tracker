from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "habits.db")
    main.init_db()


def create_habit(name="Read 20 minutes"):
    return client.post("/habits", json={"name": name}).json()["id"]


def check_in(habit_id, days_from_today=0):
    day = date.today() + timedelta(days=days_from_today)
    return client.post(f"/habits/{habit_id}/checkin", json={"day": day.isoformat()})


def test_create_and_list_habit():
    r = client.post("/habits", json={"name": "Read 20 minutes"})
    assert r.status_code == 200
    hid = r.json()["id"]
    r2 = client.get("/habits")
    assert r2.status_code == 200
    assert any(h["id"] == hid for h in r2.json())


def test_checkin_flow():
    hid = client.post("/habits", json={"name": "Stretch"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 200
    r2 = client.get(f"/habits/{hid}/checkins")
    assert r2.json() == ["2026-09-22"]


def test_checkin_unknown_habit_404():
    r = client.post("/habits/99999/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 404


def test_streak_unknown_habit_404():
    response = client.get("/habits/99999/streak")

    assert response.status_code == 404
    assert response.json() == {"detail": "unknown habit"}


def test_streak_is_zero_without_checkins():
    habit_id = create_habit()

    response = client.get(f"/habits/{habit_id}/streak")

    assert response.status_code == 200
    assert response.json() == {
        "habit_id": habit_id,
        "habit_name": "Read 20 minutes",
        "streak": 0,
    }


def test_streak_counts_consecutive_days_through_today():
    habit_id = create_habit()
    for day_offset in (0, -1, -2):
        check_in(habit_id, day_offset)

    response = client.get(f"/habits/{habit_id}/streak")

    assert response.status_code == 200
    assert response.json() == {
        "habit_id": habit_id,
        "habit_name": "Read 20 minutes",
        "streak": 3,
    }


def test_streak_stops_at_a_gap():
    habit_id = create_habit()
    check_in(habit_id, 0)
    check_in(habit_id, -2)

    response = client.get(f"/habits/{habit_id}/streak")

    assert response.status_code == 200
    assert response.json() == {
        "habit_id": habit_id,
        "habit_name": "Read 20 minutes",
        "streak": 1,
    }


def test_streak_counts_duplicates_once_and_ignores_future_dates():
    habit_id = create_habit()
    check_in(habit_id, 0)
    check_in(habit_id, 0)
    check_in(habit_id, -1)
    check_in(habit_id, 1)

    response = client.get(f"/habits/{habit_id}/streak")

    assert response.status_code == 200
    assert response.json() == {
        "habit_id": habit_id,
        "habit_name": "Read 20 minutes",
        "streak": 2,
    }


def test_streak_ignores_an_invalid_stored_date():
    habit_id = create_habit()
    check_in(habit_id, 0)
    client.post(f"/habits/{habit_id}/checkin", json={"day": "not-a-date"})

    response = client.get(f"/habits/{habit_id}/streak")

    assert response.status_code == 200
    assert response.json() == {
        "habit_id": habit_id,
        "habit_name": "Read 20 minutes",
        "streak": 1,
    }
