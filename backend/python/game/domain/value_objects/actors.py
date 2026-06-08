from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID


class Actor(BaseModel):
    id: UUID
    type: Literal["user", "team", "club"]

    def __hash__(self) -> int:
        return hash(f"{self.type}{self.id}")


class TeamParticipant(BaseModel):
    actor: Actor | None
    players: list[UUID]
    draft_roles: list[str] = Field(default_factory=list)
