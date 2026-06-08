from domain.value_objects.bracket import Bracket, Match
from domain.value_objects.actors import Actor
import math
from uuid import uuid4


class SingleEliminationBuilder:
    def build_bracket(self, participants: list[Actor]) -> Bracket:
        return self.build_single_elimination(participants, with_third_place=False)

    def build_single_elimination(
        self,
        participants: list[Actor],
        with_third_place: bool = False,
    ) -> Bracket:
        if len(participants) < 2:
            raise Exception("At least two participants are required")

        bracket_size = 2 ** math.ceil(math.log2(len(participants)))
        first_round_size = bracket_size // 2
        seeded = [*participants, *([None] * (bracket_size - len(participants)))]
        match_number = 0
        rounds: list[list[Match]] = []

        first_round: list[Match] = []
        for index in range(first_round_size):
            first_round.append(
                Match(
                    game_series_id=uuid4(),
                    team1=seeded[index],
                    team2=seeded[bracket_size - 1 - index],
                    winner=None,
                    round=0,
                    match_number=match_number,
                    next_match_id=None,
                )
            )
            match_number += 1
        rounds.append(first_round)

        previous_round = first_round
        for round_index in range(1, int(math.log2(bracket_size))):
            current_round: list[Match] = []
            for pair_index in range(0, len(previous_round), 2):
                next_match_number = match_number
                previous_round[pair_index].next_match_id = next_match_number
                if pair_index + 1 < len(previous_round):
                    previous_round[pair_index + 1].next_match_id = next_match_number
                current_round.append(
                    Match(
                        game_series_id=uuid4(),
                        team1=None,
                        team2=None,
                        winner=None,
                        round=round_index,
                        match_number=next_match_number,
                        next_match_id=None,
                    )
                )
                match_number += 1
            rounds.append(current_round)
            previous_round = current_round

        if with_third_place:
            rounds.append(
                [
                    Match(
                        game_series_id=uuid4(),
                        team1=None,
                        team2=None,
                        winner=None,
                        round=len(rounds),
                        match_number=match_number,
                        next_match_id=None,
                    )
                ]
            )

        return Bracket(rounds=rounds)

    def build_round_robin(self, participants: list[Actor]) -> Bracket:
        if len(participants) < 2:
            raise Exception("At least two participants are required")

        rotation: list[Actor | None] = [*participants]
        if len(rotation) % 2 == 1:
            rotation.append(None)

        rounds: list[list[Match]] = []
        match_number = 0
        round_count = len(rotation) - 1
        half = len(rotation) // 2

        for round_index in range(round_count):
            matches: list[Match] = []
            for index in range(half):
                team1 = rotation[index]
                team2 = rotation[-index - 1]
                if team1 is None or team2 is None:
                    continue
                matches.append(
                    Match(
                        game_series_id=uuid4(),
                        team1=team1,
                        team2=team2,
                        winner=None,
                        round=round_index,
                        match_number=match_number,
                        next_match_id=None,
                    )
                )
                match_number += 1
            rounds.append(matches)
            rotation = [rotation[0], rotation[-1], *rotation[1:-1]]

        return Bracket(rounds=rounds)

    def build_swiss(self, participants: list[Actor]) -> Bracket:
        if len(participants) < 2:
            raise Exception("At least two participants are required")

        round_count = max(1, math.ceil(math.log2(len(participants))))
        match_count = math.ceil(len(participants) / 2)
        rounds: list[list[Match]] = []
        match_number = 0

        for round_index in range(round_count):
            matches: list[Match] = []
            for index in range(match_count):
                if round_index == 0:
                    team1 = participants[index] if index < len(participants) else None
                    opponent_index = len(participants) - 1 - index
                    team2 = participants[opponent_index] if opponent_index > index else None
                else:
                    team1 = None
                    team2 = None
                matches.append(
                    Match(
                        game_series_id=uuid4(),
                        team1=team1,
                        team2=team2,
                        winner=None,
                        round=round_index,
                        match_number=match_number,
                        next_match_id=None,
                    )
                )
                match_number += 1
            rounds.append(matches)

        return Bracket(rounds=rounds)

    def build_double_elimination(self, participants: list[Actor]) -> Bracket:
        if len(participants) < 2:
            raise Exception("At least two participants are required")

        upper = self.build_single_elimination(participants, with_third_place=False)
        rounds = upper.rounds
        match_number = max(match.match_number for round_matches in rounds for match in round_matches) + 1
        upper_round_count = len(rounds)

        for lower_round_index in range(max(0, (upper_round_count - 1) * 2)):
            lower_match_count = max(
                1,
                2 ** max(0, upper_round_count - 2 - (lower_round_index // 2)),
            )
            round_number = len(rounds)
            lower_round: list[Match] = []
            for _ in range(lower_match_count):
                lower_round.append(
                    Match(
                        game_series_id=uuid4(),
                        team1=None,
                        team2=None,
                        winner=None,
                        round=round_number,
                        match_number=match_number,
                        next_match_id=None,
                    )
                )
                match_number += 1
            rounds.append(lower_round)

        rounds.append(
            [
                Match(
                    game_series_id=uuid4(),
                    team1=None,
                    team2=None,
                    winner=None,
                    round=len(rounds),
                    match_number=match_number,
                    next_match_id=None,
                )
            ]
        )

        return Bracket(rounds=rounds)
