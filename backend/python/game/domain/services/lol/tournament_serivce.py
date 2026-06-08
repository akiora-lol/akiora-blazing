from uuid import UUID, uuid4
from datetime import datetime, UTC
from domain.value_objects.actors import Actor, TeamParticipant
from domain.entities.lol.tournament import Tournament
from domain.value_objects.settings import (
    BracketType,
    LolGameSeriesSettings,
    LolTournamentSettings,
    DraftType,
    TournamentType,
    TournamentLifecycle,
    DraftState,
    DraftConfig,
    DraftCaptainInfo,
    DraftPickDirection,
)
from domain.value_objects.bracket import Bracket, BracketRoundSettings, Match
from domain.services.lol.game_series_service import GameSeriesService
from domain.entities.lol.game import Game
from domain.value_objects.statuses import GameStatus, TournamentStatus
from domain.services.lol.single_elim_builder import SingleEliminationBuilder
from domain.entities.lol.game_series import GameSeries
from shared.redis import RedisService
from beanie.operators import In


class TournamentService:
    def __init__(
        self,
        redis_service: RedisService,
        game_series_service: GameSeriesService,
        se_bracket: SingleEliminationBuilder,
    ):
        self.redis_service = redis_service
        self.game_series_service = game_series_service
        self.se_bracket = se_bracket

    async def create(
        self,
        host: Actor,
        is_open: bool,
        prize_pool: str,
        start: int,
        settings: LolTournamentSettings,
        draft_start: int | None = None,
    ) -> Tournament:
        t = Tournament.domain_create(
            host=host,
            is_open=is_open,
            prizepool=prize_pool,
            start=start,
            settings=settings,
            draft_start=draft_start,
        )
        await t.save()
        return t

    async def get(
        self,
        id: UUID | list[UUID],
    ) -> Tournament:
        if isinstance(id, list):
            trs = await Tournament.find_many(In(Tournament.id, id)).to_list()
            return trs
        t = await Tournament.get(id)

        return t

    async def add_to_waitlist(self, id: UUID, p: Actor, team: list[UUID]) -> Tournament:
        t = await Tournament.get(id)
        t.add_to_waitlist(p, team)
        await t.save()
        return t

    async def add_participant(
        self,
        id: UUID,
        p: Actor,
        team: list[UUID],
        draft_roles: list[str] | None = None,
    ) -> Tournament:
        t = await Tournament.get(id)
        if any(x.actor and x.actor.id == p.id for x in t.participant_pool):
            raise Exception("Participant already registered")
        if t.settings.tournament_type == TournamentType.DRAFT and p.type != "user":
            raise Exception("Draft tournaments accept individual users before teams are formed")
        if t.settings.tournament_type == TournamentType.PRESIGNED and p.type != "team":
            raise Exception("Presigned tournaments accept team participants")
        t.add_participant(p, team, draft_roles=draft_roles)
        if t.settings.tournament_type == TournamentType.DRAFT and t.lifecycle == TournamentLifecycle.REGISTRATION_OPEN:
            t.draft_state = None
        await t.save()
        return t

    async def lock_registration(self, id: UUID) -> Tournament:
        t = await Tournament.get(id)
        if t.lifecycle != TournamentLifecycle.REGISTRATION_OPEN:
            raise Exception("Registration is already locked")
        t.is_open = False
        t.registration_locked_at = datetime.now(UTC)
        if t.settings.tournament_type == TournamentType.DRAFT:
            draft_player_count = sum(
                1
                for participant in t.participant_pool
                if participant.actor and participant.actor.type == "user"
            )
            team_size = t.settings.game_settings.team_size
            if draft_player_count < team_size * 2:
                raise Exception("Draft pool must contain enough players for at least two teams")
            if not t.draft_state:
                t.lifecycle = TournamentLifecycle.CAPTAIN_SETUP
            else:
                participant_ids = {
                    participant.actor.id
                    for participant in t.participant_pool
                    if participant.actor and participant.actor.type == "user"
                }
                captains = {captain.captain for captain in t.draft_state.config.captains}
                if len(participant_ids) > t.draft_state.config.captain_count * team_size:
                    raise Exception("Draft pool size must fit into captain count * team size")
                if not captains.issubset(participant_ids):
                    raise Exception("Every captain must still be registered")
                t.draft_state.available_player_ids = [
                    player_id for player_id in participant_ids if player_id not in captains
                ]
                t.lifecycle = TournamentLifecycle.DRAFT_READY
        else:
            t.lifecycle = TournamentLifecycle.REGISTRATION_LOCKED
        await t.save()
        return t

    async def reschedule(
        self,
        id: UUID,
        start: int,
        draft_start: int | None = None,
    ) -> Tournament:
        t = await Tournament.get(id)
        if t.status != TournamentStatus.SCHEDULED:
            raise Exception("Only scheduled tournaments can be rescheduled")
        t.reschedule(start, draft_start=draft_start)
        await t.save()
        return t

    async def set_draft_captains(
        self,
        id: UUID,
        captain_count: int,
        captain_ids: list[UUID],
        pick_direction: DraftPickDirection = DraftPickDirection.LINEAR,
        max_extra_players_per_team: int = 4,
    ) -> Tournament:
        t = await Tournament.get(id)
        if t.settings.tournament_type != TournamentType.DRAFT:
            raise Exception("Only draft tournaments have captains")
        if t.lifecycle not in {
            TournamentLifecycle.REGISTRATION_OPEN,
            TournamentLifecycle.CAPTAIN_SETUP,
            TournamentLifecycle.DRAFT_READY,
        }:
            raise Exception("Captains can be edited before draft starts")
        participant_ids = {
            participant.actor.id
            for participant in t.participant_pool
            if participant.actor and participant.actor.type == "user"
        }
        if captain_count <= 0:
            raise Exception("Captain count must be positive")
        if len(captain_ids) != captain_count:
            raise Exception("Captain count must match captain ids")
        if captain_count < 2:
            raise Exception("Draft tournaments require at least two captains")
        team_size = t.settings.game_settings.team_size
        if len(participant_ids) > captain_count * team_size:
            raise Exception("Draft pool size must fit into captain count * team size")
        if len(participant_ids) < team_size * 2:
            raise Exception("Draft pool must contain enough players for at least two teams")
        if len(set(captain_ids)) != len(captain_ids):
            raise Exception("Captain ids must be unique")
        if any(captain_id not in participant_ids for captain_id in captain_ids):
            raise Exception("Every captain must be a registered player")
        available = [player_id for player_id in participant_ids if player_id not in captain_ids]
        t.draft_state = DraftState(
            config=DraftConfig(
                captain_count=captain_count,
                captains=[
                    DraftCaptainInfo(captain=captain_id, order=index)
                    for index, captain_id in enumerate(captain_ids)
                ],
                pick_order_captain_ids=captain_ids,
                pick_direction=pick_direction,
                max_extra_players_per_team=max(0, team_size - 1),
            ),
            current_pick_index=0,
            current_captain_id=captain_ids[0] if captain_ids else None,
            available_player_ids=available,
            finished=False,
        )
        if not t.is_open:
            t.lifecycle = TournamentLifecycle.DRAFT_READY
        await t.save()
        return t

    async def update_draft_pick_order(self, id: UUID, captain_ids: list[UUID]) -> Tournament:
        t = await Tournament.get(id)
        if not t.draft_state:
            raise Exception("Draft captains are not configured")
        configured = {captain.captain for captain in t.draft_state.config.captains}
        if set(captain_ids) != configured:
            raise Exception("Pick order must contain the configured captains")
        t.draft_state.config.pick_order_captain_ids = captain_ids
        for index, captain_id in enumerate(captain_ids):
            for captain in t.draft_state.config.captains:
                if captain.captain == captain_id:
                    captain.order = index
        t.draft_state.current_pick_index = 0
        t.draft_state.current_captain_id = captain_ids[0] if captain_ids else None
        await t.save()
        return t

    def _next_captain_id(self, state: DraftState) -> UUID | None:
        order = state.config.pick_order_captain_ids
        if not order:
            return None
        next_index = state.current_pick_index % len(order)
        if state.config.pick_direction == DraftPickDirection.SNAKE:
            round_index = state.current_pick_index // len(order)
            if round_index % 2 == 1:
                next_index = len(order) - 1 - next_index
        return order[next_index]

    async def draft_pick_player(self, id: UUID, captain_id: UUID, player_id: UUID) -> Tournament:
        t = await Tournament.get(id)
        if not t.draft_state:
            raise Exception("Draft captains are not configured")
        state = t.draft_state
        if state.finished:
            raise Exception("Draft is already finished")
        expected_captain_id = self._next_captain_id(state)
        if state.config.pick_direction != DraftPickDirection.MANUAL and expected_captain_id != captain_id:
            raise Exception("It is another captain's pick")
        if player_id not in state.available_player_ids:
            raise Exception("Player is not available in draft pool")
        captain = next((c for c in state.config.captains if c.captain == captain_id), None)
        if not captain:
            raise Exception("Captain is not configured")
        if len(captain.picked_players) >= state.config.max_extra_players_per_team:
            raise Exception("Captain team is full")
        captain.picked_players.append(player_id)
        state.available_player_ids = [
            available_id for available_id in state.available_player_ids if available_id != player_id
        ]
        state.current_pick_index += 1
        state.current_captain_id = self._next_captain_id(state)
        t.lifecycle = TournamentLifecycle.DRAFT_IN_PROGRESS
        if not state.available_player_ids or all(
            len(c.picked_players) >= state.config.max_extra_players_per_team
            for c in state.config.captains
        ):
            state.finished = True
            state.current_captain_id = None
            t.lifecycle = TournamentLifecycle.DRAFT_FINISHED
            t.participant_pool = [
                TeamParticipant(
                    actor=Actor(id=captain.captain, type="team"),
                    players=[captain.captain, *captain.picked_players],
                )
                for captain in state.config.captains
            ]
        await t.save()
        return t

    async def start_tournament(self, id: UUID) -> Tournament:
        t = await Tournament.get(id)
        if t.lifecycle != TournamentLifecycle.BRACKET_READY:
            raise Exception("Bracket must be ready before tournament start")
        gss = await self.game_series_service.get_by_tournament_id(id)
        for gs in gss:
            await self.game_series_service.start(gs.id)
        t.start()
        await t.save()
        return t

    async def swap_teams(self, id: UUID, t1: Actor, t2: Actor) -> Tournament:
        t = await Tournament.get(id)
        if t.status != TournamentStatus.SCHEDULED:
            raise Exception("Cannot swap teams in active tournament")
        if not t.bracket:
            raise Exception("Bracket not built yet")
        gs_id1, gs_id2 = t.bracket.swap_teams(t1, t2)
        tp1, tp2 = (
            TeamParticipant(
                actor=t1,
                players=next((x.players for x in t.participant_pool if x.actor == t1), []),
            ),
            TeamParticipant(
                actor=t2,
                players=next((x.players for x in t.participant_pool if x.actor == t2), []),
            ),
        )
        await self.game_series_service.swap_teams(gs_id1, tp1, tp2)
        await self.game_series_service.swap_teams(gs_id2, tp2, tp1)
        await t.save()
        return t

    async def _create_series_for_match(
        self,
        tournament: Tournament,
        match: Match,
        round_settings: list[BracketRoundSettings],
    ) -> None:
        match_best_of = next(
            (settings.best_of for settings in round_settings if settings.round == match.round),
            tournament.settings.game_series_settings.best_of or 1,
        )
        match.best_of = match_best_of
        series_settings = tournament.settings.game_series_settings.model_copy(
            update={"best_of": match_best_of}
        )
        await self.game_series_service.create(
            id=tournament.id,
            participants=[
                TeamParticipant(
                    actor=match.team1,
                    players=next(
                        (
                            participant.players
                            for participant in tournament.participant_pool
                            if participant.actor == match.team1
                        ),
                        [],
                    ),
                ),
                TeamParticipant(
                    actor=match.team2,
                    players=next(
                        (
                            participant.players
                            for participant in tournament.participant_pool
                            if participant.actor == match.team2
                        ),
                        [],
                    ),
                ),
            ],
            settings=series_settings,
        )

    def _build_bracket(self, bracket_type: BracketType, actors: list[Actor]) -> Bracket:
        match bracket_type:
            case BracketType.SINGLE_ELIMINATION:
                return self.se_bracket.build_single_elimination(actors)
            case BracketType.SINGLE_ELIMINATION_WITH_THIRD:
                return self.se_bracket.build_single_elimination(actors, with_third_place=True)
            case BracketType.DOUBLE_ELIMINATION:
                return self.se_bracket.build_double_elimination(actors)
            case BracketType.SWISS:
                return self.se_bracket.build_swiss(actors)
            case BracketType.ROUND_ROBIN:
                return self.se_bracket.build_round_robin(actors)
        raise Exception("Unsupported bracket type")

    async def prebuild_bracket(
        self,
        id: UUID,
        round_settings: list[BracketRoundSettings] | None = None,
    ) -> Tournament:
        t = await Tournament.get(id)
        if t.settings.tournament_type == TournamentType.DRAFT:
            if t.lifecycle != TournamentLifecycle.DRAFT_FINISHED:
                raise Exception("Draft must be finished before bracket prebuild")
            if any(participant.actor and participant.actor.type != "team" for participant in t.participant_pool):
                raise Exception("Draft tournament teams must be formed before bracket prebuild")
        elif t.lifecycle != TournamentLifecycle.REGISTRATION_LOCKED:
            raise Exception("Registration must be locked before bracket prebuild")
        actors = [
            participant.actor
            for participant in t.participant_pool
            if participant.actor is not None
        ]
        bracket = self._build_bracket(t.settings.bracket_type, actors)
        bracket.round_settings = round_settings or []
        for round_matches in bracket.rounds:
            for match in round_matches:
                await self._create_series_for_match(t, match, bracket.round_settings)
        t.bracket = bracket
        t.lifecycle = TournamentLifecycle.BRACKET_READY
        await t.save()
        return t

    async def update_bracket_match(
        self,
        id: UUID,
        game_series_id: UUID,
        team1: Actor | None = None,
        team2: Actor | None = None,
        best_of: int | None = None,
    ) -> Tournament:
        t = await Tournament.get(id)
        if not t.bracket:
            raise Exception("Bracket not built yet")
        for round_matches in t.bracket.rounds:
            for match in round_matches:
                if match.game_series_id == game_series_id:
                    if team1 is not None:
                        match.team1 = team1
                    if team2 is not None:
                        match.team2 = team2
                    if best_of is not None:
                        match.best_of = best_of
                    await t.save()
                    return t
        raise Exception("Bracket match not found")

    async def finish_tournament(self, id: UUID) -> Tournament:
        from datetime import datetime, UTC

        t = await Tournament.get(id)
        t.status = TournamentStatus.FINISHED
        t.lifecycle = TournamentLifecycle.TOURNAMENT_FINISHED
        t.end = datetime.now(UTC)
        await t.save()
        return t

    async def remove_participant(self, id: UUID, participant_id: UUID) -> Tournament:
        t = await Tournament.get(id)
        if t.lifecycle in (
            TournamentLifecycle.TOURNAMENT_ACTIVE,
            TournamentLifecycle.TOURNAMENT_FINISHED,
            TournamentLifecycle.TOURNAMENT_CANCELLED,
        ):
            raise Exception("Cannot remove participants after tournament start")
        t.participant_pool = [
            participant
            for participant in t.participant_pool
            if participant.actor and participant.actor.id != participant_id
        ]
        if t.settings.tournament_type == TournamentType.DRAFT and t.lifecycle == TournamentLifecycle.REGISTRATION_OPEN:
            t.draft_state = None
            await t.save()
            return t
        if t.draft_state:
            t.draft_state.available_player_ids = [
                player_id
                for player_id in t.draft_state.available_player_ids
                if player_id != participant_id
            ]
            t.draft_state.config.captains = [
                captain
                for captain in t.draft_state.config.captains
                if captain.captain != participant_id
            ]
            t.draft_state.config.pick_order_captain_ids = [
                captain_id
                for captain_id in t.draft_state.config.pick_order_captain_ids
                if captain_id != participant_id
            ]
        await t.save()
        return t

    async def remove_from_waitlist(self, id: UUID, participant_id: UUID) -> Tournament:
        t = await Tournament.get(id)
        t.wait_list = [
            participant
            for participant in t.wait_list
            if participant.actor and participant.actor.id != participant_id
        ]
        await t.save()
        return t
