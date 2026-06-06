import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject
from loguru import logger

from common import game_actors_pb2 as actors_pb2
from common import types_pb2
from common.types_pb2 import Empty
from domain.entities.lol.tournament import Tournament
from domain.services.lol.tournament_serivce import TournamentService
from domain.value_objects.actors import Actor
from domain.value_objects.settings import (
    BracketType,
    DraftType,
    LolGameSeriesSettings,
    LolGameSettings,
    LolTournamentSettings,
)
from domain.value_objects.statuses import TournamentStatus
from game.v1 import tournament_service_pb2 as pb2
from game.v1.tournament_service_pb2_grpc import TournamentServiceServicer


_ACTOR_TYPE_MAP = {1: "user", 2: "team", 3: "club"}
_ACTOR_TYPE_REVERSE = {"user": 1, "team": 2, "club": 3}
_BRACKET_MODE_MAP = {
    1: BracketType.DOUBLE_ELIMINATION,
    2: BracketType.SINGLE_ELIMINATION_WITH_THIRD,
    3: BracketType.SINGLE_ELIMINATION,
    4: BracketType.SWISS,
    5: BracketType.ROUND_ROBIN,
}
_BRACKET_MODE_REVERSE = {value: key for key, value in _BRACKET_MODE_MAP.items()}
_DRAFT_MODE_MAP = {
    1: DraftType.CLASSIC,
    2: DraftType.FEARLESS,
    3: DraftType.IRON_MAN,
    4: DraftType.ALL_RANDOM,
}
_DRAFT_MODE_REVERSE = {value: key for key, value in _DRAFT_MODE_MAP.items()}
_STATUS_REVERSE = {
    TournamentStatus.SCHEDULED: types_pb2.SCHEDULED,
    TournamentStatus.ACTIVE: types_pb2.ACTIVE,
    TournamentStatus.FINISHED: types_pb2.FINISHED,
    TournamentStatus.CANCELED: types_pb2.CANCELLED,
}
_STATUS_MAP = {
    types_pb2.SCHEDULED: TournamentStatus.SCHEDULED,
    types_pb2.ACTIVE: TournamentStatus.ACTIVE,
    types_pb2.FINISHED: TournamentStatus.FINISHED,
    types_pb2.CANCELLED: TournamentStatus.CANCELED,
}


def _paginate(items, pagination):
    page = pagination.page or 1
    page_size = pagination.page_size or 50
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], page, page_size, end < len(items)


def _proto_actor_to_domain(proto_actor) -> Actor:
    return Actor(
        id=UUID(proto_actor.id),
        type=_ACTOR_TYPE_MAP.get(proto_actor.actor_type, "user"),
    )


def _domain_actor_to_proto(actor: Actor):
    return actors_pb2.Actor(
        id=str(actor.id),
        actor_type=_ACTOR_TYPE_REVERSE.get(actor.type, 0),
    )


def _proto_lol_settings_to_domain(lol_settings) -> LolTournamentSettings:
    game_settings = LolGameSettings(
        team_size=lol_settings.team_size or 5,
        map=lol_settings.map or 11,
    )
    draft_type = _DRAFT_MODE_MAP.get(
        lol_settings.draft_mode[0] if lol_settings.draft_mode else 1,
        DraftType.CLASSIC,
    )
    game_series_settings = LolGameSeriesSettings(
        game_settings=game_settings,
        forbidden_champions=list(lol_settings.forbidden_champions),
        best_of=lol_settings.series_best_of[0] if lol_settings.series_best_of else 3,
        draft_type=draft_type,
    )
    bracket_type = _BRACKET_MODE_MAP.get(
        lol_settings.bracket_mode,
        BracketType.SINGLE_ELIMINATION,
    )
    return LolTournamentSettings(
        game_settings=game_settings,
        game_series_settings=game_series_settings,
        best_of=list(lol_settings.series_best_of),
        bracket_type=bracket_type,
    )


def _domain_settings_to_proto(settings: LolTournamentSettings):
    return pb2.TournamentSettings(
        game_type=1,
        lol=pb2.LolTournamentSettings(
            tournament_type=1,
            bracket_mode=_BRACKET_MODE_REVERSE.get(settings.bracket_type, 0),
            draft_mode=[
                _DRAFT_MODE_REVERSE.get(settings.game_series_settings.draft_type, 0)
            ],
            team_size=settings.game_settings.team_size,
            map=settings.game_settings.map,
            forbidden_champions=settings.game_series_settings.forbidden_champions,
            series_best_of=settings.best_of,
        ),
    )


def _team_participant_to_actor(team_participant):
    return team_participant.actor


def _tournament_to_proto(tournament: Tournament):
    return pb2.TournamentResponse(
        id=str(tournament.id),
        host=_domain_actor_to_proto(tournament.host),
        participants=[
            _domain_actor_to_proto(participant.actor)
            for participant in tournament.participant_pool
            if participant.actor
        ],
        settings=_domain_settings_to_proto(tournament.settings),
        game_series_ids=[],
        start=int(tournament.start.timestamp()),
        end=int(tournament.end.timestamp()) if tournament.end else 0,
        status=_STATUS_REVERSE.get(tournament.status, types_pb2.STATUS_UNSPECIFIED),
        prizepool=tournament.prizepool or "",
    )


class TournamentGrpc(TournamentServiceServicer):
    @inject
    async def CreateTournament(
        self,
        request,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ):
        host = _proto_actor_to_domain(request.host)
        settings = _proto_lol_settings_to_domain(request.settings.lol)
        tournament = await tournament_service.create(
            host=host,
            is_open=request.is_open,
            prize_pool=request.prizepool,
            start=request.start,
            settings=settings,
        )
        return _tournament_to_proto(tournament)

    @inject
    async def GetTournament(
        self,
        request,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ):
        ids = [UUID(id_str) for id_str in request.ids]
        tournaments = await tournament_service.get(ids)
        if not isinstance(tournaments, list):
            tournaments = [tournaments] if tournaments else []
        return pb2.ManyTournamentsResponse(
            tournaments=[_tournament_to_proto(tournament) for tournament in tournaments]
        )

    @inject
    async def UpdateTournament(self, request, context: grpc.aio.ServicerContext):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        if request.HasField("start"):
            tournament.reschedule(request.start)
        if request.HasField("prizepool"):
            tournament.prizepool = request.prizepool
        if request.HasField("is_open"):
            tournament.is_open = request.is_open
        if request.HasField("status"):
            tournament.status = _STATUS_MAP.get(request.status, tournament.status)
        await tournament.save()
        return _tournament_to_proto(tournament)

    @inject
    async def DeleteTournament(self, request, context: grpc.aio.ServicerContext):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        await tournament.delete()
        return Empty()

    @inject
    async def ListTournaments(self, request, context: grpc.aio.ServicerContext):
        tournaments = await Tournament.find_all().to_list()
        if request.HasField("filter"):
            filter_ = request.filter
            if filter_.game_type and filter_.game_type != 1:
                tournaments = []
            if filter_.status:
                status = _STATUS_MAP.get(filter_.status)
                tournaments = [t for t in tournaments if t.status == status]
            if filter_.host_id:
                host_id = UUID(filter_.host_id)
                tournaments = [t for t in tournaments if t.host.id == host_id]
            if filter_.is_participant and filter_.host_id:
                participant_id = UUID(filter_.host_id)
                tournaments = [
                    t for t in tournaments
                    if any(p.actor and p.actor.id == participant_id for p in t.participant_pool)
                ]
            if filter_.min_start_time:
                tournaments = [
                    t for t in tournaments
                    if int(t.start.timestamp()) >= filter_.min_start_time
                ]
            if filter_.max_start_time:
                tournaments = [
                    t for t in tournaments
                    if int(t.start.timestamp()) <= filter_.max_start_time
                ]
            if filter_.is_open:
                tournaments = [t for t in tournaments if t.is_open]
        page_items, page, page_size, has_next = _paginate(tournaments, request.pagination)
        return pb2.ListTournamentsResponse(
            tournaments=[_tournament_to_proto(tournament) for tournament in page_items],
            total_count=len(tournaments),
            page=page,
            page_size=page_size,
            has_next=has_next,
        )

    @inject
    async def StartTournament(self, request, context, tournament_service: FromDishka[TournamentService]):
        tournament = await tournament_service.start_tournament(UUID(request.tournament_id))
        return _tournament_to_proto(tournament)

    @inject
    async def FinishTournament(self, request, context, tournament_service: FromDishka[TournamentService]):
        tournament = await tournament_service.finish_tournament(UUID(request.tournament_id))
        return _tournament_to_proto(tournament)

    @inject
    async def PreBuildBracket(self, request, context, tournament_service: FromDishka[TournamentService]):
        tournament = await tournament_service.prebuild_bracket(UUID(request.tournament_id))
        return _tournament_to_proto(tournament)

    @inject
    async def AddParticipant(self, request, context, tournament_service: FromDishka[TournamentService]):
        actor = _proto_actor_to_domain(request.participant)
        tournament = await tournament_service.add_participant(
            UUID(request.tournament_id),
            actor,
            [],
        )
        return _tournament_to_proto(tournament)

    @inject
    async def AddTeam(self, request, context, tournament_service: FromDishka[TournamentService]):
        actor = _proto_actor_to_domain(request.team_participant.participant)
        player_ids = [UUID(user_id) for user_id in request.team_participant.user_ids]
        tournament = await tournament_service.add_participant(
            UUID(request.tournament_id),
            actor,
            player_ids,
        )
        return _tournament_to_proto(tournament)

    @inject
    async def RemoveParticipant(self, request, context, tournament_service: FromDishka[TournamentService]):
        tournament = await tournament_service.remove_participant(
            UUID(request.tournament_id),
            UUID(request.participant_id),
        )
        return _tournament_to_proto(tournament)

    @inject
    async def UpdateParticipant(self, request, context):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        return _tournament_to_proto(tournament)

    @inject
    async def AddParticipantToWaitList(self, request, context, tournament_service: FromDishka[TournamentService]):
        actor = _proto_actor_to_domain(request.participant)
        tournament = await tournament_service.add_to_waitlist(
            UUID(request.tournament_id),
            actor,
            [],
        )
        return _tournament_to_proto(tournament)

    @inject
    async def RemoveFromWaitList(self, request, context, tournament_service: FromDishka[TournamentService]):
        tournament = await tournament_service.remove_from_waitlist(
            UUID(request.tournament_id),
            UUID(request.participant_id),
        )
        return _tournament_to_proto(tournament)

    @inject
    async def ChangeBracket(self, request, context, tournament_service: FromDishka[TournamentService]):
        first = _proto_actor_to_domain(request.swap_initiator)
        second = _proto_actor_to_domain(request.swap_victim)
        tournament = await tournament_service.swap_teams(
            UUID(request.tournament_id),
            first,
            second,
        )
        return _tournament_to_proto(tournament)

    @inject
    async def GetBracket(self, request, context):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        if not tournament.bracket:
            return pb2.GetBracketResponse()
        participant_ids = []
        for round_matches in tournament.bracket.rounds:
            for match in round_matches:
                if match.team1:
                    participant_ids.append(str(match.team1.id))
                if match.team2:
                    participant_ids.append(str(match.team2.id))
        return pb2.GetBracketResponse(
            bracket=pb2.BracketInfo(
                bracket_id=str(tournament.id),
                participant_ids=participant_ids,
                round=len(tournament.bracket.rounds),
            )
        )

    @inject
    async def GetParticipants(self, request, context):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        participants, _, _, _ = _paginate(tournament.participant_pool, request.pagination)
        return pb2.GetParticipantsResponse(
            participants=[
                pb2.ParticipantInfo(
                    participant=_domain_actor_to_proto(participant.actor),
                    user_ids=[str(user_id) for user_id in participant.players],
                    joined_at=0,
                )
                for participant in participants
                if participant.actor
            ],
            total_count=len(tournament.participant_pool),
        )

    @inject
    async def GetWaitlist(self, request, context):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        participants, _, _, _ = _paginate(tournament.wait_list, request.pagination)
        return pb2.GetWaitlistResponse(
            participants=[
                _domain_actor_to_proto(participant.actor)
                for participant in participants
                if participant.actor
            ],
            total_count=len(tournament.wait_list),
        )

    @inject
    async def IsParticipant(self, request, context):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        participant_id = UUID(request.participant_id)
        is_participant = any(
            participant.actor and participant.actor.id == participant_id
            for participant in tournament.participant_pool
        )
        return pb2.IsParticipantResponse(
            is_participant=is_participant,
            role="participant" if is_participant else "",
        )

    @inject
    async def GetTournamentStats(self, request, context):
        tournament = await Tournament.get(UUID(request.tournament_id))
        if not tournament:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Tournament not found")
        return pb2.TournamentStatsResponse(
            total_participants=len(tournament.participant_pool),
            total_teams=len([p for p in tournament.participant_pool if p.actor and p.actor.type == "team"]),
            waitlist_count=len(tournament.wait_list),
            status=tournament.status.value,
            time_until_start=max(int(tournament.start.timestamp()), 0),
        )
