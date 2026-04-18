from datetime import datetime, UTC
from typing import Literal
from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4


def utc_now():
    return datetime.now(tz=UTC)


class Chat(Document):
    id: UUID = Field(default_factory=uuid4)
    owner_id: UUID
    owner_type: Literal["system", "club", "tournament", "gameseries"] = "system"
    type: Literal["private", "public"] = "private"
    status: Literal["active", "frozen"] = "active"
    timestamp: datetime = Field(default_factory=utc_now)
    allowed_users: list[UUID] = Field(default_factory=list)

    class Settings:
        bson_encoders = {UUID: str}
