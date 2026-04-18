from datetime import datetime, UTC
from typing import Literal
from beanie import Document
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


def utc_now():
    return datetime.now(tz=UTC)


class MessageShort(BaseModel):
    body: str
    timestamp: datetime = Field(default_factory=utc_now)


class Reaction(BaseModel):
    emote_id: str
    user_id: str


class Message(Document):
    id: UUID = Field(default_factory=uuid4)
    chat_id: UUID
    creator_id: UUID
    body: str = Field(min_length=1, max_length=500)
    status: Literal["sent", "read"] = "sent"
    read_by: list[UUID] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=utc_now)
    history: list[MessageShort] = Field(default_factory=list)
    reply_to: UUID | None = None
    reactions: list[Reaction] = Field(default_factory=list)
    spoiler: bool = Field(False)

    def short(self):
        return MessageShort(body=self.body)

    class Settings:
        bson_encoders = {UUID: str}
