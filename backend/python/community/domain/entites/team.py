"""
Team entity — lightweight version of Club.
Max 10 members. No field-level permission system (owner has full control).
"""
from beanie import Document
from pydantic import Field, field_validator
from uuid import UUID, uuid4
from datetime import datetime, UTC


def time_now():
    return datetime.now(tz=UTC)

MAX_TEAM_SIZE = 10


class Team(Document):
    id: UUID = Field(default_factory=uuid4)
    owner_id: UUID
    name: str = Field(min_length=1, max_length=64)
    avatar: str | None = None
    tag: str | None = Field(default=None, max_length=8)
    members: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=time_now)

    @field_validator("members", mode="before")
    @classmethod
    def validate_size(cls, v: list) -> list:
        if len(v) > MAX_TEAM_SIZE:
            raise ValueError(f"Team cannot have more than {MAX_TEAM_SIZE} members")
        return v

    class Settings:
        bson_encoders = {UUID: str}

    def is_full(self) -> bool:
        return len(self.members) >= MAX_TEAM_SIZE
