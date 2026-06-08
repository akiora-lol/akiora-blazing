from uuid import UUID
from loguru import logger

from domain.entites.club import Club, ClubPermission


class ClubService:
    @staticmethod
    async def create(owner_id: UUID, name: str, fields: list[list[str]] | None = None) -> Club:
        club = Club(
            owner_id=owner_id,
            name=name,
            fields=fields or [],
        )
        club.members.append(owner_id)
        await club.insert()
        logger.info("Club created id={} owner={}", club.id, owner_id)
        return club

    @staticmethod
    async def get(club_id: UUID) -> Club | None:
        return await Club.get(club_id)

    @staticmethod
    async def add_member(club_id: UUID, user_id: UUID, tokens: list[str] | None = None) -> Club:
        club = await Club.get(club_id)
        if not club:
            raise ValueError(f"Club {club_id} not found")

        if user_id not in club.members:
            club.members.append(user_id)

        if tokens:
            perm = ClubPermission(tokens=tokens)
            club.permissions[str(user_id)] = perm

        await club.save()
        logger.info("Member added club={} user={}", club_id, user_id)
        return club

    @staticmethod
    async def remove_member(club_id: UUID, user_id: UUID) -> Club:
        club = await Club.get(club_id)
        if not club:
            raise ValueError(f"Club {club_id} not found")
        if user_id == club.owner_id:
            raise PermissionError("Cannot remove the owner")

        if user_id in club.members:
            club.members.remove(user_id)
        club.permissions.pop(str(user_id), None)

        await club.save()
        return club

    @staticmethod
    async def set_permission(
        club_id: UUID, actor_id: UUID, target_user_id: UUID, tokens: list[str]
    ) -> Club:
        club = await Club.get(club_id)
        if not club:
            raise ValueError(f"Club {club_id} not found")
        if actor_id != club.owner_id:
            raise PermissionError("Only owner can change permissions")

        club.permissions[str(target_user_id)] = ClubPermission(tokens=tokens)
        await club.save()
        return club

    @staticmethod
    async def update(
        club_id: UUID,
        actor_id: UUID,
        *,
        name: str | None = None,
        avatar: str | None = None,
        description: str | None = None,
        fields: list[list[str]] | None = None,
    ) -> Club:
        club = await Club.get(club_id)
        if not club:
            raise ValueError(f"Club {club_id} not found")

        patch: dict = {}
        if name is not None:
            if not club.user_can_write(actor_id):
                raise PermissionError("No write permission")
            patch["name"] = name
        if avatar is not None:
            if not club.user_can_write(actor_id):
                raise PermissionError("No write permission")
            patch["avatar"] = avatar
        if description is not None:
            if not club.user_can_write(actor_id):
                raise PermissionError("No write permission")
            patch["description"] = description
        if fields is not None:
            if actor_id != club.owner_id:
                raise PermissionError("Only owner can redefine field groups")
            patch["fields"] = fields

        if patch:
            await club.update({"$set": patch})
        return await Club.get(club_id)
