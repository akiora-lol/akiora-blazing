from datetime import datetime, UTC
from typing import Literal
from uuid import UUID
from loguru import logger

from beanie.operators import Set, Push, Pull

from domain.entites.user import User, UserType, Platform, Social, Birthday, LeagueAccount


class UserService:
    @staticmethod
    async def create(email: str, nickname: str | None = None) -> User:
        user = User(email=email, nickname=nickname or f"user{int(datetime.now(tz=UTC).timestamp())}")
        await user.insert()
        logger.info("User created id={} email={}", user.id, email)
        return user

    @staticmethod
    async def get(user_id: UUID) -> User | None:
        return await User.get(user_id)

    @staticmethod
    async def get_by_email(email: str) -> User | None:
        return await User.find_one(User.email == email)

    @staticmethod
    async def update(
        user_id: UUID,
        *,
        nickname: str | None = None,
        bio: str | None = None,
        gender: Literal["male", "female"] | None = None,
        avatar: str | None = None,
        user_type: UserType | None = None,
        birth_date: Birthday | None = None,
        socials: dict[Platform, Social] | None = None,
        league_accounts: list[LeagueAccount] | None = None,
    ) -> User:
        user = await User.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        patch: dict = {"last_updated": datetime.now(tz=UTC)}
        if nickname is not None:
            patch["nickname"] = nickname
        if bio is not None:
            patch["bio"] = bio
        if gender is not None:
            patch["gender"] = gender
        if avatar is not None:
            patch["avatar"] = avatar
        if user_type is not None:
            patch["user_type"] = user_type
        if birth_date is not None:
            patch["birth_date"] = birth_date.model_dump()
        if socials is not None:
            patch["socials"] = {k: v.model_dump() for k, v in socials.items()}
        if league_accounts is not None:
            patch["league_accounts"] = [account.model_dump() for account in league_accounts]

        await user.update({"$set": patch})
        logger.info("User updated id={}", user_id)
        return await User.get(user_id)
