from datetime import datetime
from typing import Literal
from uuid import UUID


from beanie.odm.operators.update.general import Set
from pydantic import ValidationError

from domain.entities.chat import Chat


class ChatService:
    @staticmethod
    async def create_chat(
        owner_id: UUID,
        owner_type: Literal["system", "club", "tournament", "gameseries"] = "system",
        chat_type: Literal["private", "public"] = "private",
        allowed_users: list[UUID] | None = None,
    ) -> Chat:
        """Создаёт новый чат."""
        if allowed_users is None:
            allowed_users = []

        chat = Chat(
            owner_id=owner_id,
            owner_type=owner_type,
            type=chat_type,
            allowed_users=allowed_users,
        )
        await chat.insert()
        return chat

    @staticmethod
    async def add_allowed_user(chat_id: UUID, user_id: UUID) -> Chat:
        """Добавляет пользователя в список разрешённых (idempotent)."""
        chat = await Chat.get(chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        if user_id not in chat.allowed_users:
            chat.allowed_users.append(user_id)
            await chat.save()  # или использовать атомарный update

        return chat

    @staticmethod
    async def remove_allowed_user(chat_id: UUID, user_id: UUID) -> Chat:
        """Удаляет пользователя из allowed_users."""
        chat = await Chat.get(chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        if user_id in chat.allowed_users:
            chat.allowed_users.remove(user_id)
            await chat.save()

        return chat

    @staticmethod
    async def get_chat(chat_id: UUID) -> Chat | None:
        return await Chat.get(chat_id)

    @staticmethod
    async def freeze_chat(chat_id: UUID) -> Chat:
        """Замораживает чат (меняет статус на frozen)."""
        chat = await Chat.get(chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")
        if chat.status == "frozen":
            return chat

        chat.status = "frozen"
        await chat.save()
        return chat
