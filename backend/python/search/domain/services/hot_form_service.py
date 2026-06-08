from datetime import UTC, datetime, timedelta
from typing import Optional
from uuid import UUID

from domain.entities.hot_form import HotForm
from domain.values import LolRole, RankRange


class HotFormService:
    @staticmethod
    async def create(
        owner_id: UUID,
        rank_range: list[RankRange],
        my_roles: list[LolRole],
        looking_for_roles: list[LolRole],
        description: str,
    ) -> HotForm:
        hot_form = HotForm(
            owner_id=owner_id,
            rank_range=rank_range,
            my_roles=my_roles,
            looking_for_roles=looking_for_roles,
            description=description,
        )
        await hot_form.insert()
        return hot_form

    @staticmethod
    async def get_by_id(form_id: UUID) -> Optional[HotForm]:
        return await HotForm.find(HotForm.id == form_id).first_or_none()

    @staticmethod
    async def like(form_id: UUID, user_id: UUID) -> Optional[HotForm]:
        hot_form = await HotForm.find(HotForm.id == form_id).first_or_none()
        if not hot_form:
            return None
        if user_id in hot_form.disliked_by:
            hot_form.disliked_by.remove(user_id)
        if user_id not in hot_form.liked_by:
            hot_form.liked_by.append(user_id)
        await hot_form.save()
        return hot_form

    @staticmethod
    async def dislike(form_id: UUID, user_id: UUID) -> Optional[HotForm]:
        hot_form = await HotForm.find(HotForm.id == form_id).first_or_none()
        if not hot_form:
            return None
        if user_id in hot_form.liked_by:
            hot_form.liked_by.remove(user_id)
        if user_id not in hot_form.disliked_by:
            hot_form.disliked_by.append(user_id)
        await hot_form.save()
        return hot_form

    @staticmethod
    async def search(
        rank_range: Optional[list[RankRange]] = None,
        my_roles: Optional[list[LolRole]] = None,
        looking_for_roles: Optional[list[LolRole]] = None,
        owner_id: Optional[UUID] = None,
        exclude_owner_id: Optional[UUID] = None,
        limit: int = 50,
        skip: int = 0,
    ) -> list[HotForm]:
        query = {}
        if rank_range:
            query["rank_range"] = {"$in": rank_range}
        if my_roles:
            query["my_roles"] = {"$in": my_roles}
        if looking_for_roles:
            query["looking_for_roles"] = {"$in": looking_for_roles}
        if owner_id:
            query["owner_id"] = owner_id
        if exclude_owner_id:
            query["owner_id"] = {"$ne": exclude_owner_id}

        cursor = HotForm.find(query).sort(-HotForm.created_at).skip(skip).limit(limit)
        return await cursor.to_list()

    @staticmethod
    def expires_at(hot_form: HotForm) -> datetime:
        return hot_form.created_at + timedelta(seconds=1200)
