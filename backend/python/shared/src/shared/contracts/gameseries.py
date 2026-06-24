from typing import Optional
from pydantic import BaseModel
from uuid import UUID

from .tournament import Actor, GameSettings


class ToggleReadyRequest(BaseModel):
    series_id: UUID
    actor: Actor


class DraftAction(BaseModel):
    pick: int | None = None
    ban: int | None = None


class DraftCommand(BaseModel):
    actor: Actor
    action: DraftAction


class DraftActionRequest(BaseModel):
    series_id: UUID
    command: DraftCommand


class SetGameWinnerRequest(BaseModel):
    series_id: UUID
    game_id: UUID
    actor_id: UUID  # the host calling this
    winner: Actor   # which team participant won the game


class GameSeriesResponse(BaseModel):
    id: UUID
    tournament_id: Optional[UUID] = None
    settings: GameSettings
    participants: list[Actor]

    class Config:
        from_attributes = True


class SeriesGameView(BaseModel):
    """A single game in a series as needed by the host results UI."""

    id: UUID
    status: str                       # "scheduled" | "active" | "finished" | ...
    winner: Optional[Actor] = None    # populated for finished games


class GetSeriesResponse(BaseModel):
    """Lightweight read-side payload for the host's per-game results screen."""

    id: UUID
    status: str
    best_of: int
    games: list[SeriesGameView]
