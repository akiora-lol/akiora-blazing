import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject

from game.v1.tournament_service_pb2 import (
    CreateTournamentRequest,
    GetTournamentRequest,
    AddParticipantRequest,
    AddTeamParticipantRequest,
    RemoveParticipantRequest,
    ChangeBracketRequest,
)
from common.types_pb2 import Empty
from game.v1.tournament_service_pb2_grpc import (
    TournamentServiceServicer,
)

from domain.services.lol.tournament_serivce import TournamentService
from domain.value_objects.actors import Actor, TeamParticipant
from domain.value_objects.settings import (
    LolTournamentSettings,
    LolGameSeriesSettings,
    LolGameSettings,
    BracketType,
    DraftType,
)


_ACTOR_TYPE_MAP = {1: "user", 2: "team", 3: "club"}
_BRACKET_MODE_MAP = {
    1: BracketType.DOUBLE_ELIMINATION,
    2: BracketType.SINGLE_ELIMINATION_WITH_THIRD,
    3: BracketType.SINGLE_ELIMINATION,
    4: BracketType.SWISS,
    5: BracketType.ROUND_ROBIN,
}
_DRAFT_MODE_MAP = {
    1: DraftType.CLASSIC,
    2: DraftType.FEARLESS,
    3: DraftType.IRON_MAN,
    4: DraftType.ALL_RANDOM,
}


def _proto_actor_to_domain(proto_actor) -> Actor:
    return Actor(
        id=UUID(proto_actor.id),
        type=_ACTOR_TYPE_MAP.get(proto_actor.actor_type, "user"),
    )


def _proto_lol_settings_to_domain(lol_settings) -> LolTournamentSettings:
    game_settings = LolGameSettings(
        team_size=lol_settings.team_size,
        map=lol_settings.map,
    )
    draft_type = _DRAFT_MODE_MAP.get(
        lol_settings.draft_mode[0] if lol_settings.draft_mode else 0,
        DraftType.CLASSIC,
    )
    game_series_settings = LolGameSeriesSettings(
        game_settings=game_settings,
        forbidden_champions=list(lol_settings.forbidden_champions),
        best_of=lol_settings.series_best_of[0] if lol_settings.series_best_of else 3,
        draft_type=draft_type,
    )
    bracket_type = _BRACKET_MODE_MAP.get(
        lol_settings.bracket_mode, BracketType.SINGLE_ELIMINATION
    )
    return LolTournamentSettings(
        game_settings=game_settings,
        game_series_settings=game_series_settings,
        best_of=list(lol_settings.series_best_of),
        bracket_type=bracket_type,
    )


class TournamentGrpc(TournamentServiceServicer):
    @inject
    async def CreateTournament(
        self,
        request: CreateTournamentRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        print(request)
        host = _proto_actor_to_domain(request.host)
        settings_proto = request.settings
        lol_settings = _proto_lol_settings_to_domain(settings_proto.lol)
        await tournament_service.create(
            host=host,
            is_open=request.is_open,
            prize_pool=request.prizepool,
            start=request.start,
            settings=lol_settings,
        )
        return Empty()

    @inject
    async def GetTournament(
        self,
        request: GetTournamentRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        ids = [UUID(id_str) for id_str in request.ids]
        await tournament_service.get(ids if len(ids) > 1 else ids[0])
        return Empty()

    @inject
    async def GetTournaments(
        self,
        request: GetTournamentRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        ids = [UUID(id_str) for id_str in request.ids]
        await tournament_service.get(ids)
        return Empty()

    @inject
    async def StartTournament(
        self,
        request: GetTournamentRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        await tournament_service.start_tournament(UUID(request.ids[0]))
        return Empty()

    @inject
    async def PreBuildBracket(
        self,
        request: GetTournamentRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        await tournament_service.prebuild_bracket(UUID(request.ids[0]))
        return Empty()

    @inject
    async def FinishTournament(
        self,
        request: GetTournamentRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        # TODO: implement finish in TournamentService
        return Empty()

    @inject
    async def AddParticipant(
        self,
        request: AddParticipantRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        actor = _proto_actor_to_domain(request.participant)
        await tournament_service.add_participant(UUID(request.tournament_id), actor, [])
        return Empty()

    @inject
    async def AddTeam(
        self,
        request: AddTeamParticipantRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        tp = request.team_participant
        actor = _proto_actor_to_domain(tp.participant)
        player_ids = [UUID(uid) for uid in tp.user_ids]
        await tournament_service.add_participant(
            UUID(request.tournament_id), actor, player_ids
        )
        return Empty()

    @inject
    async def ChangeBracket(
        self,
        request: ChangeBracketRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        t1 = _proto_actor_to_domain(request.swap_initiator)
        t2 = _proto_actor_to_domain(request.swap_victim)
        await tournament_service.swap_teams(UUID(request.tournament_id), t1, t2)
        return Empty()

    @inject
    async def AddParticipantToWaitList(
        self,
        request: AddParticipantRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        actor = _proto_actor_to_domain(request.participant)
        await tournament_service.add_to_waitlist(UUID(request.tournament_id), actor, [])
        return Empty()

    @inject
    async def RemoveParticipant(
        self,
        request: RemoveParticipantRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        # TODO: implement remove_participant in TournamentService
        return Empty()
