from datetime import UTC, datetime
import json
from uuid import UUID

from shared.redis import RedisService

from notification_model import (
    FriendRequestNotification,
    Notification,
    NotificationRead,
)
from settings import Settings


class NotificationService:
    def __init__(self, redis_service: RedisService, settings: Settings):
        self.redis_service = redis_service
        self.channel = settings.channel_name

    async def handle_event(self, event: dict) -> Notification | None:
        event_type = event.get("type")
        data = self._normalize_data(event.get("data") or {})

        if event_type == "friend_request":
            return await self.create_friend_request_notification(
                FriendRequestNotification(**data)
            )

        if event_type == "notification_read":
            return await self.mark_as_read(NotificationRead(**data))

        return None

    async def create_friend_request_notification(
        self, data: FriendRequestNotification
    ) -> Notification:
        notification = Notification(
            type="friend_request",
            status="sent",
            recipient_id=data.recipient_id,
            actor_id=data.sender_id,
            title="New friend request",
            body=self._friend_request_body(data),
            payload={
                "request_id": str(data.request_id) if data.request_id else None,
                "sender_id": str(data.sender_id),
                "sender_nickname": data.sender_nickname,
            },
        )
        await notification.insert()
        await self.publish(notification)
        return notification

    async def mark_as_read(self, data: NotificationRead) -> Notification | None:
        notification = await Notification.get(data.notification_id)
        if not notification:
            return None
        if notification.recipient_id != data.user_id:
            return None

        now = datetime.now(tz=UTC)
        notification.status = "read"
        notification.read_at = now
        notification.updated_at = now
        await notification.save()
        await self.publish(notification)
        return notification

    async def publish(self, notification: Notification) -> None:
        await self.redis_service.publish_pubsub(
            self.channel,
            {
                "id": str(notification.id),
                "type": notification.type,
                "status": notification.status,
                "recipient_id": str(notification.recipient_id),
                "actor_id": str(notification.actor_id) if notification.actor_id else None,
                "title": notification.title,
                "body": notification.body,
                "payload": notification.payload,
                "created_at": notification.created_at.isoformat(),
                "updated_at": notification.updated_at.isoformat(),
                "read_at": notification.read_at.isoformat() if notification.read_at else None,
            },
        )

    @staticmethod
    def _friend_request_body(data: FriendRequestNotification) -> str:
        sender = data.sender_nickname or str(data.sender_id)
        return f"{sender} sent you a friend request"

    @staticmethod
    def _normalize_data(data) -> dict:
        if isinstance(data, str):
            return json.loads(data)
        return data
