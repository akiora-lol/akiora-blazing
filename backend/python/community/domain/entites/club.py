"""
Club entity.

Permission model:
  Club.fields — list[list[str]]
    index 0 → field group 0, index 1 → field group 1, …

  Club.permissions — dict[user_id → list[str]]
    each entry is a list of permission tokens, e.g. ["r0", "w1"]

  Token semantics:
    r0  → read all field groups
    w0  → write all field groups
    rN  → read field group at index N
    wN  → write field group at index N

  Example: ["r0", "w1"] means the user can read everything
  but can only write to fields[1].
"""

from beanie import Document, Indexed
from typing import Annotated
from pydantic import Field, BaseModel, field_validator
from uuid import UUID, uuid4
from datetime import datetime, UTC


def time_now():
    return datetime.now(tz=UTC)


# Resolved permission for a single user on a single operation
class ClubPermission(BaseModel):
    """Raw permission tokens stored per user, e.g. ['r0', 'w1', 'r2']."""

    tokens: list[str] = Field(default_factory=list)

    @field_validator("tokens", mode="before")
    @classmethod
    def validate_tokens(cls, v: list[str]) -> list[str]:
        import re

        for t in v:
            if not re.fullmatch(r"[rw]\d+", t):
                raise ValueError(f"Invalid permission token: {t!r}")
        return v

    def can_read(self, field_group: int | None = None) -> bool:
        """True if this entry grants read on the given field group (or any if None)."""
        for t in self.tokens:
            if not t.startswith("r"):
                continue
            n = int(t[1:])
            if n == 0 or field_group is None or n - 1 == field_group:
                return True
        return False

    def can_write(self, field_group: int | None = None) -> bool:
        """True if this entry grants write on the given field group (or any if None)."""
        for t in self.tokens:
            if not t.startswith("w"):
                continue
            n = int(t[1:])
            if n == 0 or field_group is None or n - 1 == field_group:
                return True
        return False


class Club(Document):
    id: UUID = Field(default_factory=uuid4)
    owner_id: Annotated[UUID, Indexed(unique=True)]
    name: str = Field(min_length=1, max_length=64)
    avatar: str | None = None
    description: str | None = Field(default=None, max_length=500)

    # list[list[str]] — each inner list is a group of field names
    # Example: [["name", "avatar"], ["description"]]
    # r1 / w1 refers to fields[0], r2 / w2 to fields[1], etc.
    # r0 / w0 means all groups.
    fields: list[list[str]] = Field(default_factory=list)

    # user_id → permission tokens
    permissions: dict[str, ClubPermission] = Field(default_factory=dict)

    members: list[UUID] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=time_now)

    class Settings:
        bson_encoders = {UUID: str}

    def get_permission(self, user_id: UUID) -> ClubPermission | None:
        return self.permissions.get(str(user_id))

    def user_can_read(self, user_id: UUID, field_group: int | None = None) -> bool:
        if user_id == self.owner_id:
            return True
        perm = self.get_permission(user_id)
        return perm.can_read(field_group) if perm else False

    def user_can_write(self, user_id: UUID, field_group: int | None = None) -> bool:
        if user_id == self.owner_id:
            return True
        perm = self.get_permission(user_id)
        return perm.can_write(field_group) if perm else False
