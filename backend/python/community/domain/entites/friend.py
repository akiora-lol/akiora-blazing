from datetime import UTC, datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


def time_now():
    return datetime.now(tz=UTC)


class Friend(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id_1: UUID
    user_id_2: UUID
    status: str = "pending"
    created_at: datetime = Field(default_factory=time_now)
    updated_at: datetime = Field(default_factory=time_now)

    class Settings:
        bson_encoders = {UUID: str}
