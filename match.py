# match.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""represents a football match between two teams."""

from team import Team


class Match:
    """
    Represents a football match between two teams.

    A match can be played in two ways: group match or a knockout match
    """
    def __init__(self, team1: "Team", team2: "Team", is_knockout: bool):
        """
        Initialize a match

        Args:
            team1: the first team
            team2: the second team
            is_knockout: show that the match is a knockout match or not
        """
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.winner: Team | str | None = None
        self.is_knockout = is_knockout

    def play(self):
        """
        Play the match and store the result

        Updates the goals scored by each team and records the winner
        """
        result = self.team1.simulate_match(self.team2, self.is_knockout)
        self.goals1 = result[0]
        self.goals2 = result[1]
        self.winner = result[2]

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"

    def __repr__(self):
        return f"Match({self.team1}, {self.team2})"
