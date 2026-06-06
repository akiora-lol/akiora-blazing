from datetime import datetime
from typing import Literal
from uuid import UUID


from pydantic import ValidationError

from domain.entities.message import Message, MessageShort, Reaction

from domain.entities.chat import Chat


class MessageService:
    """Доменный сервис для работы с сообщениями."""

    @staticmethod
    async def create_message(
        chat_id: UUID,
        creator_id: UUID,
        body: str,
        reply_to: UUID | None = None,
        spoiler: bool = False,
    ) -> Message:
        """Создаёт новое сообщение в чате.

        Проверки:
        - чат существует и активен
        - пользователь имеет право писать (в allowed_users или владелец)
        """
        chat = await Chat.get(chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        if chat.status != "active":
            raise ValueError("Cannot send message to frozen chat")

        # Простая проверка прав (можно расширить)
        if (
            creator_id != chat.owner_id
            and creator_id not in chat.allowed_users
            and chat.owner_type != "system"
        ):
            raise PermissionError("User is not allowed to write in this chat")

        if not 1 <= len(body) <= 500:
            raise ValueError("Message body must be between 1 and 500 characters")

        message = Message(
            chat_id=chat_id,
            creator_id=creator_id,
            body=body,
            reply_to=reply_to,
            spoiler=spoiler,
        )
        await message.insert()
        return message

    @staticmethod
    async def update_message(
        message_id: UUID,
        new_body: str,
        editor_id: UUID,
    ) -> Message:
        """Обновляет тело сообщения.

        Важная логика по ТЗ:
        1. Загружаем текущее сообщение
        2. Создаём short-версию старого тела
        3. Добавляем её в history
        4. Обновляем body и сбрасываем статус/реакции при необходимости
        """
        if not 1 <= len(new_body) <= 500:
            raise ValueError("Message body must be between 1 and 500 characters")

        message = await Message.get(message_id)
        if not message:
            raise ValueError(f"Message with id {message_id} not found")

        if message.creator_id != editor_id:
            raise PermissionError("Only the creator can edit their message")

        old_short = message.short()

        update_query = {
            "$set": {
                "body": new_body,
                "status": "sent",
            },
            "$push": {"history": old_short.model_dump()},
        }

        await message.update(update_query)

        # Перезагружаем обновлённый документ
        updated_message = await Message.get(message_id)
        return updated_message

    @staticmethod
    async def add_reaction(
        message_id: UUID,
        user_id: UUID,
        emote_id: str,
    ) -> Message:
        """Добавляет реакцию (idempotent — один emote от одного пользователя)."""
        message = await Message.get(message_id)
        if not message:
            raise ValueError(f"Message with id {message_id} not found")

        existing = next(
            (
                r
                for r in message.reactions
                if r.user_id == str(user_id) and r.emote_id == emote_id
            ),
            None,
        )
        if existing:
            return message  # уже есть — ничего не делаем

        reaction = Reaction(emote_id=emote_id, user_id=str(user_id))
        update_query = {
            "$push": {"reactions": reaction.model_dump()},
        }
        await message.update(update_query)

        return await Message.get(message_id)

    @staticmethod
    async def remove_reaction(
        message_id: UUID,
        user_id: UUID,
        emote_id: str,
    ) -> Message:
        """Удаляет конкретную реакцию пользователя."""
        message = await Message.get(message_id)
        if not message:
            raise ValueError(f"Message with id {message_id} not found")

        await message.update(
            {"$pull": {"reactions": {"emote_id": emote_id, "user_id": str(user_id)}}}
        )
        return await Message.get(message_id)

    @staticmethod
    async def mark_as_read(
        message_id: UUID,
        user_id: UUID,
    ) -> Message:
        """Отмечает сообщение как прочитанное (idempotent)."""
        message = await Message.get(message_id)
        if not message:
            raise ValueError(f"Message with id {message_id} not found")

        if user_id not in message.read_by:
            update_query = {
                "$push": {"read_by": user_id},
            }
            await message.update(update_query)
            # можно также изменить status на "read", если все прочитали и т.д.

        return await Message.get(message_id)

    @staticmethod
    async def get_messages(
        chat_id: UUID,
        limit: int = 50,
        before_timestamp: int | None = None,
    ) -> list[Message]:
        from datetime import datetime, UTC

        query = Message.find(Message.chat_id == chat_id)
        if before_timestamp is not None:
            dt = datetime.fromtimestamp(before_timestamp, tz=UTC)
            query = query.find(Message.timestamp < dt)
        return await query.sort(-Message.timestamp).limit(limit).to_list()

    @staticmethod
    async def delete_message(message_id: UUID, deleter_id: UUID) -> bool:
        """Мягкое удаление или hard delete (по вашей политике)."""
        message = await Message.get(message_id)
        if not message:
            return False

        if message.creator_id != deleter_id:
            raise PermissionError("Only the creator can delete the message")

        await message.delete()
        return True
