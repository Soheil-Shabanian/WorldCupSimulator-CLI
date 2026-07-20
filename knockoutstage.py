# knockoutstage.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""manages a knockout round and advances the winning teams to the next stage"""

from team import Team
from match import Match
from printer import match_result_printer


class KnockoutStage:
    """
    Represents one knockout stage

    a knockout stage has multiple matches. the winners of each match go to the next round.
    """
    def __init__(self, round_name: str, matches: list[Match]):
        """
        Initialize a knockout stage

        Args:
            round_name: the name of the knockout round ("Round of 16", "Quarter-finals", "Semi-finals", "Final")
            matches: a list of matches in the round
        """
        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        """
        play all matches in the knockout stage

        each match is simulated and save its result
        """
        # Play every match in the current knockout round
        for match in self.matches:
            match.play()

    def get_winners(self):
        """
        return the winners of all matches in the round

        Returns:
            a list containing the winning teams
        """
        winners: list[Team] = [match.winner for match in self.matches]
        return winners

    def display_results(self, verbose: bool):
        """
        display the results of the knockout stage

        if verbose is True, the score and winner of each match are printed

        Args:
            verbose: option for printing or not
        """
        if verbose:
            if self.round_name == "Final":
                print(f"\n{self.round_name} winners:")
                for match in self.matches:
                    match_result_printer(match)
                print(f"\n{self.round_name} winner: \033[48;2;0;255;0m\033[38;2;0;0;0m {self.get_winners()[0].name} \033[0m")

            else:
                print(f"\n{self.round_name} winners:")
                print(" Table-1 ".center(50, '-'))
                for i, match in enumerate(self.matches):
                    if i == len(self.matches) // 2:
                        print()
                        print(" Table-2 ".center(50, '-'))

                    match_result_printer(match)