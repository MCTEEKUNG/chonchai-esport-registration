from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.database import get_stats, get_team, init_db, list_teams, save_team, team_exists


allowed_games = ("RoV", "Valorant", "FC Online")


class RegisterRequest(BaseModel):
    team_name: str = Field(..., min_length=1)
    game: str = Field(..., min_length=1)
    members: List[str] = Field(..., min_length=1)


class RegisterResponse(BaseModel):
    success: bool
    message: str
    team: dict | None = None


app = FastAPI(title="Chonchai E-Sport Tournament Registration")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def show_games() -> tuple[str, ...]:
    return allowed_games


def register_team(team_name: str, game: str, members_list: list[str]) -> tuple[bool, str]:
    cleaned_team_name = team_name.strip()
    cleaned_game = game.strip()
    cleaned_members = [member.strip() for member in members_list if member.strip()]

    if cleaned_game not in allowed_games:
        return False, "ไม่มีเกมนี้ในการแข่งขัน"

    if team_exists(cleaned_team_name):
        return False, "ชื่อทีมนี้ถูกใช้ไปแล้ว"

    if len(cleaned_members) < 3:
        return False, "สมาชิกไม่ครบ 3 คน"

    save_team(cleaned_team_name, cleaned_game, cleaned_members)
    return True, "ลงทะเบียนสำเร็จ!"


@app.get("/games")
def get_games() -> dict:
    return {"games": list(show_games())}


@app.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest) -> RegisterResponse:
    success, message = register_team(request.team_name, request.game, request.members)
    team_name = request.team_name.strip()
    team = None

    if success:
        team = get_team(team_name)

    return RegisterResponse(success=success, message=message, team=team)


@app.get("/teams")
def get_teams() -> dict:
    return {"teams": list_teams()}


@app.get("/stats")
def stats() -> dict:
    return get_stats(allowed_games)


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
