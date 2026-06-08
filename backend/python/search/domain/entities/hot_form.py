from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4
from pymongo import IndexModel, ASCENDING
from datetime import datetime, UTC

from domain.values import RankRange, LolRole


def time_now():
    return datetime.now(tz=UTC)


class HotForm(Document):
    id: UUID = Field(default_factory=uuid4)
    owner_id: UUID
    liked_by: list[UUID] = Field(default_factory=list)
    disliked_by: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=time_now)

    rank_range: list[RankRange]

    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: str

    class Settings:
        bson_encoders = {UUID: str}

        indexes = [IndexModel([("created_at", ASCENDING)], expireAfterSeconds=1200)]
