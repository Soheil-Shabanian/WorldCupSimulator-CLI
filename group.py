# group.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""a Group manages four teams and simulates all the group matches"""

from team import Team
from match import Match

class Group:
    """
    Represents a group of teams in the group game

    the class can play for each team and save the winners
    """
    def __init__(self, name: str, teams: list[Team]):
        """
        Initialize a group

        Args:
            name: the group name
            teams: a list of teams in the group
        """
        self.name = name
        self.teams = teams

    def play_all_matches(self):
        """
        simulate all matches between teams in the group

        Every team plays once against every other team
        Points:
            - Win: 3 points
            - Draw: 1 point
            - Loss: 0 points
        """
        for x_team in range(len(self.teams)-1):
            for y_team in range(x_team+1, len(self.teams)):

                match = Match(self.teams[x_team], self.teams[y_team], False)
                match.play()
                result = match.winner

                if result == 'Draw':
                    self.teams[x_team].point += 1
                    self.teams[y_team].point += 1
                elif result == self.teams[y_team]:
                    self.teams[y_team].point += 3
                elif result == self.teams[x_team]:
                    self.teams[x_team].point += 3

    def get_ranking(self):
        """
        return the teams sorted by their group ranking

        teams are ranked by these:
            1. Point
            2. Goal difference
            3. Goals scored

        Returns:
            a list of teams sorted from highest to lowest rank
        """
        group_result = sorted(self.teams, key=lambda t: (t.point, t.goal_difference, t.goals_for), reverse=True)
        return group_result

    def advance_teams(self):
        """
        return the top two teams in the group

        Returns:
            a tuple containing the first and second teams
        """
        # The first two teams
        first_team = self.get_ranking()[0]
        second_team = self.get_ranking()[1]
        return first_team, second_team

    def __str__(self):
        return f"Group(name={self.name}, teams={self.teams})"

    def __repr__(self):
        return f"Group(name={self.name}, teams={self.teams})"
