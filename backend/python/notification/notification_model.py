from datetime import UTC, datetime
from typing import Literal
from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, Field


def utc_now():
    return datetime.now(tz=UTC)


NotificationStatus = Literal["sent", "read"]
NotificationType = Literal["friend_request"]


class Notification(Document):
    id: UUID = Field(default_factory=uuid4)
    type: NotificationType
    status: NotificationStatus = "sent"
    recipient_id: UUID
    actor_id: UUID | None = None
    title: str
    body: str
    payload: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    read_at: datetime | None = None

    class Settings:
        bson_encoders = {UUID: str}


class FriendRequestNotification(BaseModel):
    recipient_id: UUID
    sender_id: UUID
    request_id: UUID | None = None
    sender_nickname: str | None = None


class NotificationRead(BaseModel):
    notification_id: UUID
    user_id: UUID
