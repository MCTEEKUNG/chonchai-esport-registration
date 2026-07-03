import os

os.environ["DATABASE_PATH"] = "data/test-registration.db"

from fastapi.testclient import TestClient

from app.database import clear_teams, get_database_path
from app.main import app


client = TestClient(app)


def setup_function():
    clear_teams()


def test_get_games():
    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == {"games": ["RoV", "Valorant", "FC Online"]}


def test_register_team_success():
    response = client.post(
        "/register",
        json={
            "team_name": "Chonchai Alpha",
            "game": "RoV",
            "members": ["A", "B", "C"],
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "ลงทะเบียนสำเร็จ!"
    assert response.json()["team"] == {
        "team_name": "Chonchai Alpha",
        "game": "RoV",
        "members": ["A", "B", "C"],
    }


def test_reject_unknown_game():
    response = client.post(
        "/register",
        json={
            "team_name": "Chonchai Beta",
            "game": "Unknown Game",
            "members": ["A", "B", "C"],
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "ไม่มีเกมนี้ในการแข่งขัน"


def test_reject_duplicate_team_name():
    payload = {
        "team_name": "Chonchai Gamma",
        "game": "Valorant",
        "members": ["A", "B", "C"],
    }

    first_response = client.post("/register", json=payload)
    second_response = client.post("/register", json=payload)

    assert first_response.json()["success"] is True
    assert second_response.status_code == 200
    assert second_response.json()["success"] is False
    assert second_response.json()["message"] == "ชื่อทีมนี้ถูกใช้ไปแล้ว"


def test_reject_too_few_members():
    response = client.post(
        "/register",
        json={
            "team_name": "Chonchai Delta",
            "game": "FC Online",
            "members": ["A", "B"],
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "สมาชิกไม่ครบ 3 คน"


def test_reject_duplicate_members_in_same_team():
    response = client.post(
        "/register",
        json={
            "team_name": "Chonchai Same Members",
            "game": "RoV",
            "members": ["A", "B", "A"],
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "ชื่อสมาชิกซ้ำกัน"


def test_reject_member_used_by_another_team():
    first_response = client.post(
        "/register",
        json={
            "team_name": "Chonchai First",
            "game": "RoV",
            "members": ["A", "B", "C"],
        },
    )
    second_response = client.post(
        "/register",
        json={
            "team_name": "Chonchai Second",
            "game": "Valorant",
            "members": ["D", "E", "A"],
        },
    )

    assert first_response.json()["success"] is True
    assert second_response.status_code == 200
    assert second_response.json()["success"] is False
    assert second_response.json()["message"] == "ชื่อสมาชิกนี้ถูกใช้ไปแล้ว"


def test_get_teams_after_register():
    client.post(
        "/register",
        json={
            "team_name": "Chonchai Echo",
            "game": "RoV",
            "members": ["A", "B", "C"],
        },
    )

    response = client.get("/teams")

    assert response.status_code == 200
    assert response.json() == {
        "teams": [
            {
                "team_name": "Chonchai Echo",
                "game": "RoV",
                "members": ["A", "B", "C"],
            }
        ]
    }


def test_registration_is_saved_to_local_database():
    client.post(
        "/register",
        json={
            "team_name": "Chonchai Persist",
            "game": "Valorant",
            "members": ["A", "B", "C"],
        },
    )

    assert get_database_path().exists()


def test_get_stats():
    client.post(
        "/register",
        json={
            "team_name": "Stats RoV",
            "game": "RoV",
            "members": ["A", "B", "C"],
        },
    )
    client.post(
        "/register",
        json={
            "team_name": "Stats Valorant",
            "game": "Valorant",
            "members": ["D", "E", "F", "G"],
        },
    )

    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json()["total_teams"] == 2
    assert response.json()["total_members"] == 7
    assert response.json()["by_game"] == [
        {"game": "RoV", "teams": 1},
        {"game": "Valorant", "teams": 1},
        {"game": "FC Online", "teams": 0},
    ]
