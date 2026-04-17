from pydantic import BaseModel

from uuid import UUID

from domain.value_objects.actors import Actor


class Match(BaseModel):
    game_series_id: UUID
    team1: Actor | None
    team2: Actor | None
    winner: Actor | None
    round: int
    match_number: int
    next_match_id: int | None


class Bracket(BaseModel):
    rounds: list[list[Match]]

    def swap_teams(self, t1: Actor, t2: Actor) -> tuple[UUID, UUID]:
        m1, m2 = None, None
        for match in self.rounds[0]:
            if match.team1 == t1:
                m1 = (match, 0)
            elif match.team2 == t1:
                m1 = (match, 1)
            if match.team1 == t2:
                m2 = (match, 0)
            elif match.team2 == t2:
                m2 = (match, 1)
        if not m1 or not m2:
            raise Exception("Teams not found in bracket")
        match1, side1 = m1
        match2, side2 = m2
        if side1 == 0:
            match1.team1 = t2
        else:
            match1.team2 = t2
        if side2 == 0:
            match2.team1 = t1
        else:
            match2.team2 = t1
        return match1.game_series_id, match2.game_series_id
