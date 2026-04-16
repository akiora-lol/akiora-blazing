from draft_schemas import Command, PrepareDraft
from shared.redis import RedisService
from draft_model import Draft


class DraftService:
    def __init__(self, redis_service: RedisService):
        self.prefix = "draft:"
        self.redis_service = redis_service

    async def get_draft(self, game_id: str) -> Draft:
        return await self.redis_service.get(f"{self.prefix}{game_id}", obj_type=Draft)

    async def prepare_draft(self, prepare_draft: PrepareDraft) -> None:
        draft = Draft.prepare(prepare_draft)
        return await self.save_draft(draft)

    async def save_draft(self, draft: Draft) -> None:
        await self.redis_service.create(
            f"{self.prefix}{draft.game_id}", draft.model_dump()
        )

    async def delete_draft(self, draft: Draft) -> None:
        await self.redis_service.delete(f"{self.prefix}{draft.game_id}")

    async def perform_command(self, draft: Draft, command: Command) -> None:
        nc = draft.perform_command(command)
        if not nc:
            await self.redis_service.publish_pubsub(
                "notification", {"data": "Draft finished"}
            )
        else:
            await self.redis_service.publish_pubsub(
                "notification", {"data": nc.model_dump()}
            )
