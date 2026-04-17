from domain.value_objects.bracket import Bracket, Match
from domain.value_objects.actors import Actor
import math
from uuid import uuid4


class SingleEliminationBuilder:
    def build_bracket(self, participants: list[Actor]) -> Bracket:
        N = math.ceil(math.log2(len(participants)))
        n_matches = 2 ** (N - 1)

        first_round: list[tuple[Actor | None, Actor | None]] = [
            (None, None)
        ] * n_matches

        matches_order = []
        for i in range(n_matches):
            matches_order.extend([i, n_matches - 1 - i])

        matches_order = list(dict.fromkeys(matches_order))[
            : len(participants) // 2 + len(participants) % 2
        ]

        pos = 0
        for match_idx in matches_order:
            if pos < len(participants):
                first_round[match_idx] = (participants[pos], first_round[match_idx][1])
                pos += 1
            if pos < len(participants):
                first_round[match_idx] = (first_round[match_idx][0], participants[pos])
                pos += 1
        matches = []
        for el in first_round:
            matches.append(
                Match(
                    game_series_id=uuid4(),
                    team1=el[0],
                    team2=el[1],
                    winner=None,
                    round=0,
                    match_number=first_round.index(el),
                    next_match_id=None,
                )
            )
        rounds: list[list[Match]] = []
        rounds.append(matches)
        for i in range(1, N):
            round_matches = []
            for j in range(0, len(rounds[-1]) - 1, 2):
                idx = (
                    round_matches[-1].match_number + 1
                    if len(round_matches) > 0
                    else rounds[-1][-1].match_number + j + 1
                )
                rounds[-1][j].next_match_id = idx
                rounds[-1][j + 1].next_match_id = idx
                round_matches.append(
                    Match(
                        game_series_id=uuid4(),
                        team1=None,
                        team2=None,
                        winner=None,
                        round=i,
                        match_number=idx,
                        next_match_id=None,
                    )
                )
            rounds.append(round_matches)

        return Bracket(matches=rounds)
