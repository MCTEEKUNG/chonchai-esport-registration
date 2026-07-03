import json
import os
import sqlite3
from pathlib import Path
from typing import Any


DEFAULT_DATABASE_PATH = Path("data") / "registration.db"


def get_database_path() -> Path:
    return Path(os.getenv("DATABASE_PATH", DEFAULT_DATABASE_PATH))


def get_connection() -> sqlite3.Connection:
    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                team_name TEXT PRIMARY KEY,
                game TEXT NOT NULL,
                members_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def clear_teams() -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM teams")


def team_exists(team_name: str) -> bool:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM teams WHERE team_name = ?",
            (team_name,),
        ).fetchone()
    return row is not None


def save_team(team_name: str, game: str, members: list[str]) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO teams (team_name, game, members_json)
            VALUES (?, ?, ?)
            """,
            (team_name, game, json.dumps(members, ensure_ascii=False)),
        )


def get_team(team_name: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT team_name, game, members_json
            FROM teams
            WHERE team_name = ?
            """,
            (team_name,),
        ).fetchone()

    if row is None:
        return None

    return {
        "team_name": row["team_name"],
        "game": row["game"],
        "members": json.loads(row["members_json"]),
    }


def list_teams() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT team_name, game, members_json
            FROM teams
            ORDER BY created_at ASC, team_name ASC
            """
        ).fetchall()

    return [
        {
            "team_name": row["team_name"],
            "game": row["game"],
            "members": json.loads(row["members_json"]),
        }
        for row in rows
    ]


def get_stats(allowed_games: tuple[str, ...]) -> dict[str, Any]:
    teams = list_teams()
    by_game = {game: 0 for game in allowed_games}
    total_members = 0

    for team in teams:
        by_game[team["game"]] = by_game.get(team["game"], 0) + 1
        total_members += len(team["members"])

    return {
        "total_teams": len(teams),
        "total_members": total_members,
        "total_games": len(allowed_games),
        "by_game": [
            {"game": game, "teams": by_game.get(game, 0)}
            for game in allowed_games
        ],
        "latest_teams": teams[-5:][::-1],
    }
