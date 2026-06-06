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


class GameSeriesResponse(BaseModel):
    id: UUID
    tournament_id: Optional[UUID] = None
    settings: GameSettings
    participants: list[Actor]

    class Config:
        from_attributes = True
