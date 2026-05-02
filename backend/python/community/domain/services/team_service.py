from uuid import UUID
from loguru import logger

from domain.entites.team import Team, MAX_TEAM_SIZE


class TeamService:
    @staticmethod
    async def create(owner_id: UUID, name: str, tag: str | None = None) -> Team:
        team = Team(owner_id=owner_id, name=name, tag=tag)
        team.members.append(owner_id)
        await team.insert()
        logger.info("Team created id={} owner={}", team.id, owner_id)
        return team

    @staticmethod
    async def get(team_id: UUID) -> Team | None:
        return await Team.get(team_id)

    @staticmethod
    async def add_member(team_id: UUID, actor_id: UUID, user_id: UUID) -> Team:
        team = await Team.get(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")
        if actor_id != team.owner_id:
            raise PermissionError("Only owner can add members")
        if team.is_full():
            raise ValueError(f"Team is full (max {MAX_TEAM_SIZE})")
        if user_id not in team.members:
            team.members.append(user_id)
            await team.save()
        logger.info("Member added team={} user={}", team_id, user_id)
        return team

    @staticmethod
    async def remove_member(team_id: UUID, actor_id: UUID, user_id: UUID) -> Team:
        team = await Team.get(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")
        if actor_id != team.owner_id and actor_id != user_id:
            raise PermissionError("Only owner or the member themselves can leave/kick")
        if user_id == team.owner_id:
            raise PermissionError("Owner cannot leave the team")
        if user_id in team.members:
            team.members.remove(user_id)
            await team.save()
        return team

    @staticmethod
    async def update(
        team_id: UUID,
        actor_id: UUID,
        *,
        name: str | None = None,
        avatar: str | None = None,
        tag: str | None = None,
    ) -> Team:
        team = await Team.get(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")
        if actor_id != team.owner_id:
            raise PermissionError("Only owner can update team")

        patch: dict = {}
        if name is not None:
            patch["name"] = name
        if avatar is not None:
            patch["avatar"] = avatar
        if tag is not None:
            patch["tag"] = tag

        if patch:
            await team.update({"$set": patch})
        return await Team.get(team_id)
