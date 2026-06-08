# services/cold_form_service.py
from typing import Optional, List, Literal
from uuid import UUID
from datetime import datetime, UTC

from domain.entities.cold_form import ColdForm, ShortForm
from domain.values import RankRange, LolRole


class ColdFormService:
    """Сервис для работы с холодными анкетами (ColdForm)"""

    @staticmethod
    async def create(
        owner_id: UUID,
        rank_range: List[RankRange],
        my_roles: List[LolRole],
        looking_for_roles: List[LolRole],
        description: str,
        status: Literal["active", "frozen"] = "active",
    ) -> ColdForm:
        """Создание новой холодной анкеты"""
        cold_form = ColdForm(
            owner_id=owner_id,
            rank_range=rank_range,
            my_roles=my_roles,
            looking_for_roles=looking_for_roles,
            description=description,
            status=status,
        )
        await cold_form.insert()
        return cold_form

    @staticmethod
    async def update(
        form_id: UUID,
        rank_range: Optional[List[RankRange]] = None,
        my_roles: Optional[List[LolRole]] = None,
        looking_for_roles: Optional[List[LolRole]] = None,
        description: Optional[str] = None,
        status: Optional[Literal["active", "frozen"]] = None,
    ) -> Optional[ColdForm]:
        """
        Обновление анкеты с сохранением истории изменений
        """
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        if not cold_form:
            return None

        # Сохраняем текущую версию в историю
        current_short = cold_form.short()
        cold_form.history.append(current_short)

        # Обновляем поля
        if rank_range is not None:
            cold_form.rank_range = rank_range
        if my_roles is not None:
            cold_form.my_roles = my_roles
        if looking_for_roles is not None:
            cold_form.looking_for_roles = looking_for_roles
        if description is not None:
            cold_form.description = description
        if status is not None:
            cold_form.status = status

        cold_form.updated_at = datetime.now(UTC)
        await cold_form.save()
        return cold_form

    @staticmethod
    async def like(form_id: UUID, user_id: UUID) -> Optional[ColdForm]:

        cold_form = await ColdForm.find_one(ColdForm.id == form_id)
        if not cold_form:
            return None

        if user_id in cold_form.disliked_by:
            cold_form.disliked_by.remove(user_id)

        if user_id not in cold_form.liked_by:
            cold_form.liked_by.append(user_id)

        await cold_form.save()
        return cold_form

    @staticmethod
    async def dislike(form_id: UUID, user_id: UUID) -> Optional[ColdForm]:
        """Поставить дизлайк анкете"""
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        if not cold_form:
            return None

        if user_id in cold_form.liked_by:
            cold_form.liked_by.remove(user_id)

        if user_id not in cold_form.disliked_by:
            cold_form.disliked_by.append(user_id)

        await cold_form.save()
        return cold_form

    @staticmethod
    async def block(form_id: UUID, user_id: UUID) -> Optional[ColdForm]:
        """Заблокировать анкету (пользователь не будет её видеть)"""
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        if not cold_form:
            return None

        if user_id not in cold_form.blocked_by:
            cold_form.blocked_by.append(user_id)

        await cold_form.save()
        return cold_form

    @staticmethod
    async def unblock(form_id: UUID, user_id: UUID) -> Optional[ColdForm]:
        """Разблокировать анкету"""
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        if cold_form and user_id in cold_form.blocked_by:
            cold_form.blocked_by.remove(user_id)
            await cold_form.save()
        return cold_form

    @staticmethod
    async def freeze(form_id: UUID) -> Optional[ColdForm]:
        """Заморозить анкету"""
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        if cold_form:
            cold_form.status = "frozen"
            cold_form.updated_at = datetime.now(UTC)
            await cold_form.save()
        return cold_form

    @staticmethod
    async def unfreeze(form_id: UUID) -> Optional[ColdForm]:
        """Разморозить анкету"""
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        if cold_form:
            cold_form.status = "active"
            cold_form.updated_at = datetime.now(UTC)
            await cold_form.save()
        return cold_form

    @staticmethod
    async def get_by_id(form_id: UUID) -> Optional[ColdForm]:
        """Получить анкету по ID"""
        return await ColdForm.find(ColdForm.id == form_id).first_or_none()

    @staticmethod
    async def get_by_owner(owner_id: UUID) -> List[ColdForm]:
        """Получить все анкеты владельца"""
        return await ColdForm.find(ColdForm.owner_id == owner_id).to_list()

    @staticmethod
    async def delete(form_id: UUID) -> bool:
        """Удалить анкету"""
        result = await ColdForm.find(ColdForm.id == form_id).delete()
        return result.deleted_count > 0

    @staticmethod
    async def get_history(form_id: UUID) -> List[ShortForm]:
        """Получить историю изменений анкеты"""
        cold_form = await ColdForm.find(ColdForm.id == form_id).first_or_none()
        return cold_form.history if cold_form else []

    @staticmethod
    async def search(
        rank_range: Optional[List[RankRange]] = None,
        my_roles: Optional[List[LolRole]] = None,
        looking_for_roles: Optional[List[LolRole]] = None,
        owner_id: Optional[UUID] = None,
        exclude_owner_id: Optional[UUID] = None,
        status: Optional[Literal["active", "frozen"]] = "active",
        exclude_blocked_by: Optional[UUID] = None,
        min_likes: Optional[int] = None,
        limit: int = 50,
        skip: int = 0,
    ) -> List[ColdForm]:
        """
        Поиск холодных анкет по фильтрам
        """
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

        if status:
            query["status"] = status

        if exclude_blocked_by:
            query["blocked_by"] = {"$ne": exclude_blocked_by}

        cursor = ColdForm.find(query)

        if min_likes is not None:
            all_forms = await cursor.to_list()
            filtered = [f for f in all_forms if len(f.liked_by) >= min_likes]
            return filtered[skip : skip + limit]

        cursor = cursor.sort(-ColdForm.created_at).skip(skip).limit(limit)
        return await cursor.to_list()

    @staticmethod
    async def get_popular(limit: int = 10) -> List[ColdForm]:
        """Получить самые популярные (по лайкам) анкеты"""
        all_forms = await ColdForm.find(ColdForm.status == "active").to_list()
        sorted_forms = sorted(all_forms, key=lambda f: len(f.liked_by), reverse=True)
        return sorted_forms[:limit]
