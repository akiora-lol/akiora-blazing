import grpc
from uuid import UUID

from shared.contracts.tournament import (
    AddParticipantRequest,
    AddParticipantToWaitListRequest,
    AddTeamParticipantRequest,
    BracketInfo,
    BracketMatchInfo,
    BracketRoundSettings,
    ChangeBracketRequest,
    CreateTournamentRequest,
    DeleteTournamentRequest,
    DraftCaptainInfo,
    DraftConfig,
    DraftPickDirection,
    DraftPickPlayerRequest,
    DraftState,
    FinishTournamentRequest,
    GetBracketRequest,
    GetBracketResponse,
    GetParticipantsRequest,
    GetParticipantsResponse,
    GetTournamentRequest,
    GetTournamentStatsRequest,
    GetWaitlistRequest,
    GetWaitlistResponse,
    IsParticipantRequest,
    IsParticipantResponse,
    ListTournamentsRequest,
    ListTournamentsResponse,
    ManyTournamentsResponse,
    ParticipantInfo,
    PreBuildBracketRequest,
    RescheduleTournamentRequest,
    RemoveFromWaitListRequest,
    RemoveParticipantRequest,
    StartTournamentRequest,
    TournamentResponse,
    TournamentStatsResponse,
    TournamentLifecycle,
    UpdateBracketMatchRequest,
    UpdateDraftPickOrderRequest,
    UpdateParticipantRequest,
    UpdateTournamentRequest,
    ChangeBracketRequest,
    TournamentSettings,
    LolTournamentSettings,
    TftTournamentSettings,
    ValorantTournamentSettings,
    Actor,
    TeamParticipant,
    ActorType,
    GameType,
    LolGameMode,
    LolBracketMode,
    Status,
    TournamentType,
)

import game.v1.tournament_service_pb2 as pb2_module
import game.v1.tournament_service_pb2_grpc as pb2_grpc_module
import common.game_actors_pb2 as actors_pb2_module


class TournamentMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for Tournament service"""

    ACTOR_TYPE_MAP = {
        0: ActorType.ACTOR_UNSPECIFIED,
        1: ActorType.USER,
        2: ActorType.TEAM,
        3: ActorType.CLUB,
    }

    ACTOR_TYPE_TO_PROTO = {v: k for k, v in ACTOR_TYPE_MAP.items()}

    GAME_TYPE_MAP = {
        0: GameType.GAME_TYPE_UNSPECIFIED,
        1: GameType.LOL,
        2: GameType.TFT,
        3: GameType.VALORANT,
    }

    GAME_TYPE_TO_PROTO = {v: k for k, v in GAME_TYPE_MAP.items()}

    STATUS_MAP = {
        0: Status.STATUS_UNSPECIFIED,
        1: Status.SCHEDULED,
        2: Status.ACTIVE,
        3: Status.FINISHED,
        4: Status.CANCELLED,
    }

    STATUS_TO_PROTO = {v: k for k, v in STATUS_MAP.items()}

    TOURNAMENT_TYPE_MAP = {
        0: TournamentType.UNSPECIFIED,
        1: TournamentType.PRESIGNED,
        2: TournamentType.DRAFT,
    }

    TOURNAMENT_TYPE_TO_PROTO = {v: k for k, v in TOURNAMENT_TYPE_MAP.items()}
    TOURNAMENT_TYPE_TO_PROTO[TournamentType.PRESIGN] = 1
    TOURNAMENT_TYPE_TO_PROTO[TournamentType.PICKEM] = 2

    LIFECYCLE_MAP = {
        0: TournamentLifecycle.TOURNAMENT_LIFECYCLE_UNSPECIFIED,
        1: TournamentLifecycle.REGISTRATION_OPEN,
        2: TournamentLifecycle.REGISTRATION_LOCKED,
        3: TournamentLifecycle.CAPTAIN_SETUP,
        4: TournamentLifecycle.DRAFT_READY,
        5: TournamentLifecycle.DRAFT_IN_PROGRESS,
        6: TournamentLifecycle.DRAFT_FINISHED,
        7: TournamentLifecycle.BRACKET_READY,
        8: TournamentLifecycle.TOURNAMENT_ACTIVE,
        9: TournamentLifecycle.TOURNAMENT_FINISHED,
        10: TournamentLifecycle.TOURNAMENT_CANCELLED,
    }
    LIFECYCLE_TO_PROTO = {v: k for k, v in LIFECYCLE_MAP.items()}

    DRAFT_PICK_DIRECTION_MAP = {
        0: DraftPickDirection.DRAFT_PICK_DIRECTION_UNSPECIFIED,
        1: DraftPickDirection.LINEAR,
        2: DraftPickDirection.SNAKE,
        3: DraftPickDirection.MANUAL,
    }
    DRAFT_PICK_DIRECTION_TO_PROTO = {v: k for k, v in DRAFT_PICK_DIRECTION_MAP.items()}

    LOL_BRACKET_MODE_MAP = {
        0: LolBracketMode.LOL_BRACKET_MODE_UNSPECIFIED,
        1: LolBracketMode.DOUBLE_ELIM,
        2: LolBracketMode.SINGLE_ELIM_THIRD_PLACE,
        3: LolBracketMode.SINGLE_ELIM_NO_THIRD_PLACE,
        4: LolBracketMode.SWISS,
        5: LolBracketMode.ROUND_ROBIN,
        6: LolBracketMode.SCRIM,
    }

    LOL_BRACKET_MODE_TO_PROTO = {v: k for k, v in LOL_BRACKET_MODE_MAP.items()}

    LOL_GAME_MODE_MAP = {
        0: LolGameMode.GAME_MODE_UNSPECIFIED,
        1: LolGameMode.CLASSIC,
        2: LolGameMode.FEARLESS,
        3: LolGameMode.IRON_MAN,
        4: LolGameMode.ALL_RANDOM,
    }

    LOL_GAME_MODE_TO_PROTO = {v: k for k, v in LOL_GAME_MODE_MAP.items()}

    @classmethod
    def _to_pydantic_actor(cls, grpc_actor) -> Actor:
        return Actor(
            id=UUID(grpc_actor.id),
            actor_type=cls.ACTOR_TYPE_MAP.get(
                grpc_actor.actor_type, ActorType.ACTOR_UNSPECIFIED
            ),
        )

    @classmethod
    def _to_grpc_actor(cls, actor: Actor):
        return actors_pb2_module.Actor(
            id=str(actor.id),
            actor_type=cls.ACTOR_TYPE_TO_PROTO.get(actor.actor_type, 0),
        )

    @classmethod
    def _to_pydantic_team_participant(cls, grpc_participant) -> TeamParticipant:
        return TeamParticipant(
            participant=cls._to_pydantic_actor(grpc_participant.participant),
            user_ids=list(grpc_participant.user_ids),
        )

    @classmethod
    def _to_grpc_team_participant(cls, participant: TeamParticipant):
        return actors_pb2_module.TeamParticipant(
            participant=cls._to_grpc_actor(participant.participant),
            user_ids=participant.user_ids,
        )

    @classmethod
    def _to_pydantic_settings(cls, grpc_settings) -> TournamentSettings:
        lol = None
        if grpc_settings.HasField("lol"):
            lol = LolTournamentSettings(
                tournament_type=cls.TOURNAMENT_TYPE_MAP.get(
                    grpc_settings.lol.tournament_type, TournamentType.UNSPECIFIED
                ),
                bracket_mode=cls.LOL_BRACKET_MODE_MAP.get(
                    grpc_settings.lol.bracket_mode,
                    LolBracketMode.LOL_BRACKET_MODE_UNSPECIFIED,
                ),
                draft_mode=[
                    cls.LOL_GAME_MODE_MAP.get(m, LolGameMode.GAME_MODE_UNSPECIFIED)
                    for m in grpc_settings.lol.draft_mode
                ],
                team_size=grpc_settings.lol.team_size,
                map=grpc_settings.lol.map,
                forbidden_champions=list(grpc_settings.lol.forbidden_champions),
                series_best_of=list(grpc_settings.lol.series_best_of),
                draft_start=(
                    grpc_settings.lol.draft_start
                    if grpc_settings.lol.HasField("draft_start")
                    else None
                ),
            )

        tft = None
        if grpc_settings.HasField("tft"):
            tft = TftTournamentSettings(todo=grpc_settings.tft.todo or None)

        valorant = None
        if grpc_settings.HasField("valorant"):
            valorant = ValorantTournamentSettings(
                todo=grpc_settings.valorant.todo or None
            )

        return TournamentSettings(
            game_type=cls.GAME_TYPE_MAP.get(
                grpc_settings.game_type, GameType.GAME_TYPE_UNSPECIFIED
            ),
            lol=lol,
            tft=tft,
            valorant=valorant,
        )

    @classmethod
    def _to_grpc_settings(cls, settings: TournamentSettings):
        grpc_settings = pb2_module.TournamentSettings(
            game_type=cls.GAME_TYPE_TO_PROTO.get(settings.game_type, 0)
        )
        if settings.lol:
            lol_settings = pb2_module.LolTournamentSettings(
                tournament_type=cls.TOURNAMENT_TYPE_TO_PROTO.get(
                    settings.lol.tournament_type, 0
                ),
                bracket_mode=cls.LOL_BRACKET_MODE_TO_PROTO.get(
                    settings.lol.bracket_mode, 0
                ),
                draft_mode=[
                    cls.LOL_GAME_MODE_TO_PROTO.get(mode, 0)
                    for mode in settings.lol.draft_mode
                ],
                team_size=settings.lol.team_size,
                map=settings.lol.map,
                forbidden_champions=settings.lol.forbidden_champions,
                series_best_of=settings.lol.series_best_of,
            )
            if settings.lol.draft_start:
                lol_settings.draft_start = settings.lol.draft_start
            grpc_settings.lol.CopyFrom(lol_settings)
        if settings.tft:
            grpc_settings.tft.CopyFrom(
                pb2_module.TftTournamentSettings(todo=settings.tft.todo or "")
            )
        if settings.valorant:
            grpc_settings.valorant.CopyFrom(
                pb2_module.ValorantTournamentSettings(todo=settings.valorant.todo or "")
            )
        return grpc_settings

    @classmethod
    def _to_pydantic_round_setting(cls, grpc_setting) -> BracketRoundSettings:
        return BracketRoundSettings(
            round=grpc_setting.round,
            label=grpc_setting.label,
            best_of=grpc_setting.best_of,
        )

    @classmethod
    def _to_grpc_round_setting(cls, setting: BracketRoundSettings):
        return pb2_module.BracketRoundSettings(
            round=setting.round,
            label=setting.label,
            best_of=setting.best_of,
        )

    @classmethod
    def _to_pydantic_bracket_match(cls, grpc_match) -> BracketMatchInfo:
        return BracketMatchInfo(
            game_series_id=grpc_match.game_series_id,
            team1=cls._to_pydantic_actor(grpc_match.team1)
            if grpc_match.HasField("team1")
            else None,
            team2=cls._to_pydantic_actor(grpc_match.team2)
            if grpc_match.HasField("team2")
            else None,
            winner=cls._to_pydantic_actor(grpc_match.winner)
            if grpc_match.HasField("winner")
            else None,
            round=grpc_match.round,
            match_number=grpc_match.match_number,
            next_match_id=grpc_match.next_match_id
            if grpc_match.HasField("next_match_id")
            else None,
            best_of=grpc_match.best_of,
        )

    @classmethod
    def _to_pydantic_bracket_info(cls, grpc_bracket) -> BracketInfo:
        return BracketInfo(
            bracket_id=grpc_bracket.bracket_id,
            participant_ids=list(grpc_bracket.participant_ids),
            round=grpc_bracket.round,
            round_settings=[
                cls._to_pydantic_round_setting(x) for x in grpc_bracket.round_settings
            ],
            matches=[cls._to_pydantic_bracket_match(x) for x in grpc_bracket.matches],
        )

    @classmethod
    def _to_pydantic_draft_state(cls, grpc_state) -> DraftState:
        return DraftState(
            config=DraftConfig(
                captain_count=grpc_state.config.captain_count,
                captains=[
                    DraftCaptainInfo(
                        captain=cls._to_pydantic_actor(c.captain),
                        order=c.order,
                        picked_players=[
                            cls._to_pydantic_actor(p) for p in c.picked_players
                        ],
                    )
                    for c in grpc_state.config.captains
                ],
                pick_order_captain_ids=list(grpc_state.config.pick_order_captain_ids),
                pick_direction=cls.DRAFT_PICK_DIRECTION_MAP.get(
                    grpc_state.config.pick_direction,
                    DraftPickDirection.DRAFT_PICK_DIRECTION_UNSPECIFIED,
                ),
                max_extra_players_per_team=grpc_state.config.max_extra_players_per_team,
            ),
            current_pick_index=grpc_state.current_pick_index,
            current_captain_id=grpc_state.current_captain_id
            if grpc_state.HasField("current_captain_id")
            else None,
            available_player_ids=list(grpc_state.available_player_ids),
            finished=grpc_state.finished,
        )

    @classmethod
    def to_pydantic_response(cls, grpc_response) -> TournamentResponse:
        participants = [cls._to_pydantic_actor(p) for p in grpc_response.participants]

        return TournamentResponse(
            id=UUID(grpc_response.id),
            host=cls._to_pydantic_actor(grpc_response.host),
            participants=participants,
            settings=cls._to_pydantic_settings(grpc_response.settings),
            game_series_ids=list(grpc_response.game_series_ids),
            start=grpc_response.start,
            end=grpc_response.end if grpc_response.end else None,
            status=cls.STATUS_MAP.get(grpc_response.status, Status.STATUS_UNSPECIFIED),
            prizepool=grpc_response.prizepool if grpc_response.prizepool else None,
            is_open=grpc_response.is_open,
            lifecycle=cls.LIFECYCLE_MAP.get(
                grpc_response.lifecycle,
                TournamentLifecycle.TOURNAMENT_LIFECYCLE_UNSPECIFIED,
            ),
            draft_start=grpc_response.draft_start
            if grpc_response.HasField("draft_start")
            else None,
            registration_locked_at=(
                grpc_response.registration_locked_at
                if grpc_response.HasField("registration_locked_at")
                else None
            ),
            draft_state=(
                cls._to_pydantic_draft_state(grpc_response.draft_state)
                if grpc_response.HasField("draft_state")
                else None
            ),
            bracket=(
                cls._to_pydantic_bracket_info(grpc_response.bracket)
                if grpc_response.HasField("bracket")
                else None
            ),
        )

    @classmethod
    def to_pydantic_list_response(cls, grpc_response) -> ListTournamentsResponse:
        return ListTournamentsResponse(
            tournaments=[
                cls.to_pydantic_response(tournament)
                for tournament in grpc_response.tournaments
            ],
            total_count=grpc_response.total_count,
            page=grpc_response.page,
            page_size=grpc_response.page_size,
            has_next=grpc_response.has_next,
        )

    @classmethod
    def to_pydantic_participants_response(
        cls, grpc_response
    ) -> GetParticipantsResponse:
        return GetParticipantsResponse(
            participants=[
                ParticipantInfo(
                    participant=cls._to_pydantic_actor(participant.participant),
                    user_ids=list(participant.user_ids),
                    joined_at=participant.joined_at,
                    draft_roles=list(getattr(participant, "draft_roles", [])),
                    is_captain=(
                        participant.is_captain
                        if participant.HasField("is_captain")
                        else None
                    ),
                    captain_order=(
                        participant.captain_order
                        if participant.HasField("captain_order")
                        else None
                    ),
                )
                for participant in grpc_response.participants
            ],
            total_count=grpc_response.total_count,
        )

    @classmethod
    def to_pydantic_waitlist_response(cls, grpc_response) -> GetWaitlistResponse:
        return GetWaitlistResponse(
            participants=[
                cls._to_pydantic_actor(participant)
                for participant in grpc_response.participants
            ],
            total_count=grpc_response.total_count,
        )

    @classmethod
    def to_pydantic_bracket_response(cls, grpc_response) -> GetBracketResponse:
        if not grpc_response.HasField("bracket"):
            return GetBracketResponse()
        return GetBracketResponse(
            bracket=cls._to_pydantic_bracket_info(grpc_response.bracket)
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateTournamentRequest):
        grpc_request = pb2_module.CreateTournamentRequest(
            host=cls._to_grpc_actor(request.host),
            settings=cls._to_grpc_settings(request.settings),
            start=request.start,
            is_open=request.is_open,
        )
        if request.prizepool:
            grpc_request.prizepool = request.prizepool
        if request.name:
            grpc_request.name = request.name
        if request.description:
            grpc_request.description = request.description
        if request.avatar:
            grpc_request.avatar = request.avatar
        if request.draft_start:
            grpc_request.draft_start = request.draft_start
        return grpc_request

    @classmethod
    def to_grpc_get_request(cls, request: GetTournamentRequest):
        grpc_request = pb2_module.GetTournamentRequest(ids=request.ids)
        if request.game_type:
            grpc_request.game_type = cls.GAME_TYPE_TO_PROTO.get(request.game_type, 0)
        return grpc_request

    @classmethod
    def to_grpc_pagination(cls, pagination):
        return pb2_module.PaginationRequest(
            page=pagination.page,
            page_size=pagination.page_size,
        )

    @classmethod
    def to_grpc_update_request(cls, request: UpdateTournamentRequest):
        grpc_request = pb2_module.UpdateTournamentRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
            is_open=request.is_open,
        )
        if request.start:
            grpc_request.start = request.start
        if request.prizepool:
            grpc_request.prizepool = request.prizepool
        if request.status:
            grpc_request.status = cls.STATUS_TO_PROTO.get(request.status, 0)
        if request.name:
            grpc_request.name = request.name
        if request.description:
            grpc_request.description = request.description
        if request.draft_start:
            grpc_request.draft_start = request.draft_start
        return grpc_request

    @classmethod
    def to_grpc_delete_request(cls, request: DeleteTournamentRequest):
        return pb2_module.DeleteTournamentRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_list_request(cls, request: ListTournamentsRequest):
        grpc_filter = pb2_module.TournamentFilter(
            is_participant=request.filter.is_participant,
            is_open=request.filter.is_open,
        )
        if request.filter.game_type:
            grpc_filter.game_type = cls.GAME_TYPE_TO_PROTO.get(
                request.filter.game_type, 0
            )
        if request.filter.status:
            grpc_filter.status = cls.STATUS_TO_PROTO.get(request.filter.status, 0)
        if request.filter.host_id:
            grpc_filter.host_id = str(request.filter.host_id)
        if request.filter.min_start_time:
            grpc_filter.min_start_time = request.filter.min_start_time
        if request.filter.max_start_time:
            grpc_filter.max_start_time = request.filter.max_start_time
        return pb2_module.ListTournamentsRequest(
            filter=grpc_filter,
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_add_participant_request(cls, request: AddParticipantRequest):
        team_name = request.team_name or ""
        if request.draft_roles and not team_name:
            team_name = "draft_roles:" + ":".join(request.draft_roles[:2])
        return pb2_module.AddParticipantRequest(
            tournament_id=str(request.tournament_id),
            participant=cls._to_grpc_actor(request.participant),
            team_name=team_name,
            draft_roles=request.draft_roles,
        )

    @classmethod
    def to_grpc_add_team_request(cls, request: AddTeamParticipantRequest):
        return pb2_module.AddTeamParticipantRequest(
            tournament_id=str(request.tournament_id),
            team_participant=cls._to_grpc_team_participant(request.team_participant),
        )

    @classmethod
    def to_grpc_remove_participant_request(cls, request: RemoveParticipantRequest):
        return pb2_module.RemoveParticipantRequest(
            tournament_id=str(request.tournament_id),
            participant_id=request.participant_id,
            actor_id=str(request.actor_id or ""),
        )

    @classmethod
    def to_grpc_update_participant_request(cls, request: UpdateParticipantRequest):
        return pb2_module.UpdateParticipantRequest(
            tournament_id=str(request.tournament_id),
            participant_id=request.participant_id,
            actor_id=str(request.actor_id or ""),
            team_name=request.team_name or "",
        )

    @classmethod
    def to_grpc_start_request(cls, request: StartTournamentRequest):
        return pb2_module.StartTournamentRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id or ""),
        )

    @classmethod
    def to_grpc_finish_request(cls, request: FinishTournamentRequest):
        return pb2_module.FinishTournamentRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id or ""),
            winner_id=request.winner_id or "",
        )

    @classmethod
    def to_grpc_prebuild_bracket_request(cls, request: PreBuildBracketRequest):
        return pb2_module.PreBuildBracketRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id or ""),
            round_settings=[
                cls._to_grpc_round_setting(setting)
                for setting in request.round_settings
            ],
        )

    @classmethod
    def to_grpc_lock_registration_request(cls, request: LockRegistrationRequest):
        return pb2_module.LockRegistrationRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_reschedule_request(cls, request: RescheduleTournamentRequest):
        grpc_request = pb2_module.RescheduleTournamentRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
            start=request.start,
        )
        if request.draft_start:
            grpc_request.draft_start = request.draft_start
        return grpc_request

    @classmethod
    def to_grpc_set_draft_captains_request(cls, request: SetDraftCaptainsRequest):
        return pb2_module.SetDraftCaptainsRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
            captain_count=request.captain_count,
            captain_ids=request.captain_ids,
            pick_direction=cls.DRAFT_PICK_DIRECTION_TO_PROTO.get(
                request.pick_direction,
                1,
            ),
            max_extra_players_per_team=request.max_extra_players_per_team,
        )

    @classmethod
    def to_grpc_update_draft_pick_order_request(
        cls, request: UpdateDraftPickOrderRequest
    ):
        return pb2_module.UpdateDraftPickOrderRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
            captain_ids=request.captain_ids,
        )

    @classmethod
    def to_grpc_draft_pick_player_request(cls, request: DraftPickPlayerRequest):
        return pb2_module.DraftPickPlayerRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
            captain_id=request.captain_id,
            player_id=request.player_id,
        )

    @classmethod
    def to_grpc_update_bracket_match_request(cls, request: UpdateBracketMatchRequest):
        grpc_request = pb2_module.UpdateBracketMatchRequest(
            tournament_id=str(request.tournament_id),
            actor_id=str(request.actor_id),
            game_series_id=request.game_series_id,
        )
        if request.team1:
            grpc_request.team1.CopyFrom(cls._to_grpc_actor(request.team1))
        if request.team2:
            grpc_request.team2.CopyFrom(cls._to_grpc_actor(request.team2))
        if request.best_of is not None:
            grpc_request.best_of = request.best_of
        return grpc_request

    @classmethod
    def to_grpc_change_bracket_request(cls, request: ChangeBracketRequest):
        return pb2_module.ChangeBracketRequest(
            tournament_id=str(request.tournament_id),
            swap_initiator=cls._to_grpc_actor(request.swap_initiator),
            swap_victim=cls._to_grpc_actor(request.swap_victim),
        )

    @classmethod
    def to_grpc_add_waitlist_request(cls, request: AddParticipantToWaitListRequest):
        return pb2_module.AddParticipantToWaitListRequest(
            tournament_id=str(request.tournament_id),
            participant=cls._to_grpc_actor(request.participant),
        )

    @classmethod
    def to_grpc_remove_waitlist_request(cls, request: RemoveFromWaitListRequest):
        return pb2_module.RemoveFromWaitListRequest(
            tournament_id=str(request.tournament_id),
            participant_id=request.participant_id,
        )

    @classmethod
    def to_grpc_get_participants_request(cls, request: GetParticipantsRequest):
        return pb2_module.GetParticipantsRequest(
            tournament_id=str(request.tournament_id),
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_get_waitlist_request(cls, request: GetWaitlistRequest):
        return pb2_module.GetWaitlistRequest(
            tournament_id=str(request.tournament_id),
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_get_bracket_request(cls, request: GetBracketRequest):
        return pb2_module.GetBracketRequest(tournament_id=str(request.tournament_id))

    @classmethod
    def to_grpc_is_participant_request(cls, request: IsParticipantRequest):
        return pb2_module.IsParticipantRequest(
            tournament_id=str(request.tournament_id),
            participant_id=request.participant_id,
        )

    @classmethod
    def to_grpc_stats_request(cls, request: GetTournamentStatsRequest):
        return pb2_module.GetTournamentStatsRequest(
            tournament_id=str(request.tournament_id)
        )


class TournamentStub:
    """Stub for Tournament Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.TournamentServiceStub(channel)
        self.mapper = TournamentMapper()

    async def create_tournament(
        self, request: CreateTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = await self.stub.CreateTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_tournament(
        self, request: GetTournamentRequest
    ) -> ManyTournamentsResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetTournament(grpc_request)
        tournaments = [
            self.mapper.to_pydantic_response(t) for t in response.tournaments
        ]
        return ManyTournamentsResponse(tournaments=tournaments)

    async def update_tournament(
        self, request: UpdateTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_update_request(request)
        response = await self.stub.UpdateTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def delete_tournament(self, request: DeleteTournamentRequest):
        grpc_request = self.mapper.to_grpc_delete_request(request)
        return await self.stub.DeleteTournament(grpc_request)

    async def list_tournaments(
        self, request: ListTournamentsRequest
    ) -> ListTournamentsResponse:
        grpc_request = self.mapper.to_grpc_list_request(request)
        response = await self.stub.ListTournaments(grpc_request)
        return self.mapper.to_pydantic_list_response(response)

    async def start_tournament(
        self, request: StartTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_start_request(request)
        response = await self.stub.StartTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def lock_registration(
        self, request: LockRegistrationRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_lock_registration_request(request)
        response = await self.stub.LockRegistration(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def reschedule_tournament(
        self, request: RescheduleTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_reschedule_request(request)
        response = await self.stub.RescheduleTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def finish_tournament(
        self, request: FinishTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_finish_request(request)
        response = await self.stub.FinishTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def prebuild_bracket(
        self, request: PreBuildBracketRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_prebuild_bracket_request(request)
        response = await self.stub.PreBuildBracket(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def set_draft_captains(
        self, request: SetDraftCaptainsRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_set_draft_captains_request(request)
        response = await self.stub.SetDraftCaptains(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def update_draft_pick_order(
        self, request: UpdateDraftPickOrderRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_update_draft_pick_order_request(request)
        response = await self.stub.UpdateDraftPickOrder(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def draft_pick_player(
        self, request: DraftPickPlayerRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_draft_pick_player_request(request)
        response = await self.stub.DraftPickPlayer(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def add_participant(
        self, request: AddParticipantRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_add_participant_request(request)
        response = await self.stub.AddParticipant(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def add_team(self, request: AddTeamParticipantRequest) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_add_team_request(request)
        response = await self.stub.AddTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def remove_participant(
        self, request: RemoveParticipantRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_remove_participant_request(request)
        response = await self.stub.RemoveParticipant(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def update_participant(
        self, request: UpdateParticipantRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_update_participant_request(request)
        response = await self.stub.UpdateParticipant(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def add_to_waitlist(
        self, request: AddParticipantToWaitListRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_add_waitlist_request(request)
        response = await self.stub.AddParticipantToWaitList(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def remove_from_waitlist(
        self, request: RemoveFromWaitListRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_remove_waitlist_request(request)
        response = await self.stub.RemoveFromWaitList(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def change_bracket(self, request: ChangeBracketRequest) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_change_bracket_request(request)
        response = await self.stub.ChangeBracket(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def update_bracket_match(
        self, request: UpdateBracketMatchRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_update_bracket_match_request(request)
        response = await self.stub.UpdateBracketMatch(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_bracket(self, request: GetBracketRequest) -> GetBracketResponse:
        grpc_request = self.mapper.to_grpc_get_bracket_request(request)
        response = await self.stub.GetBracket(grpc_request)
        return self.mapper.to_pydantic_bracket_response(response)

    async def get_participants(
        self, request: GetParticipantsRequest
    ) -> GetParticipantsResponse:
        grpc_request = self.mapper.to_grpc_get_participants_request(request)
        response = await self.stub.GetParticipants(grpc_request)
        return self.mapper.to_pydantic_participants_response(response)

    async def get_waitlist(self, request: GetWaitlistRequest) -> GetWaitlistResponse:
        grpc_request = self.mapper.to_grpc_get_waitlist_request(request)
        response = await self.stub.GetWaitlist(grpc_request)
        return self.mapper.to_pydantic_waitlist_response(response)

    async def is_participant(
        self, request: IsParticipantRequest
    ) -> IsParticipantResponse:
        grpc_request = self.mapper.to_grpc_is_participant_request(request)
        response = await self.stub.IsParticipant(grpc_request)
        return IsParticipantResponse(
            is_participant=response.is_participant,
            role=response.role or None,
        )

    async def get_tournament_stats(
        self, request: GetTournamentStatsRequest
    ) -> TournamentStatsResponse:
        grpc_request = self.mapper.to_grpc_stats_request(request)
        response = await self.stub.GetTournamentStats(grpc_request)
        return TournamentStatsResponse(
            total_participants=response.total_participants,
            total_teams=response.total_teams,
            waitlist_count=response.waitlist_count,
            status=response.status,
            time_until_start=response.time_until_start,
        )

    def create_tournament_sync(
        self, request: CreateTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_tournament_sync(
        self, request: GetTournamentRequest
    ) -> ManyTournamentsResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetTournament(grpc_request)
        tournaments = [
            self.mapper.to_pydantic_response(t) for t in response.tournaments
        ]
        return ManyTournamentsResponse(tournaments=tournaments)
