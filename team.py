# team.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""storing the teams information about the games and running simulations"""

import numpy as np
import random

class Team:
    """
    a team has attack, defence, rank, goal, goals from opponent, name
    the team class save this values for each team
    """
    def __init__(self, name: str, attack: int, defence: int, rank: int):
        """
        Initialize a new team.

        Args:
            name: Team name
            attack: attack power (0-100)
            defence: defence power (0-100)
            rank: Team ranking value
        """
        self.name = name
        self.__attack = attack
        self.__defence = defence
        self.__rank = rank

        self.point = 0
        self.__goals_for = 0
        self.__goals_against = 0
        self.pens = 0

    @property
    def goals_against(self):
        """
        Return the total number of goals from opponent
        """
        return self.__goals_against

    @property
    def goals_for(self):
        """
        Return the total number of team goals
        """
        return self.__goals_for

    @property
    def attack(self):
        """
        Return the team attack number
        """
        return self.__attack

    @attack.setter
    def attack(self, value):
        """
        Set the team attack number

        Raises:
            ValueError: If the value is negative
        """
        if value < 0:
            raise ValueError("Attack value is wrong.")
        self.__attack = value

    @property
    def defence(self):
        """
        Return the team defence number
        """
        return self.__defence

    @defence.setter
    def defence(self, value):
        """
        Set the team defence number

        Raises:
            ValueError: If the value is negative
        """
        if value < 0:
            raise ValueError("Defence value is wrong.")
        self.__defence = value

    @property
    def rank(self):
        """
        Return the team ranking
        """
        return self.__rank

    @rank.setter
    def rank(self, value):
        """
        Set the team ranking

        Raises:
            ValueError: If the value is negative
        """
        if value < 0:
            raise ValueError("Rank value is wrong.")
        self.__rank = value

    @property
    def goal_difference(self):
        """
        Return the team goal difference
        """
        return self.__goals_for - self.__goals_against

    def reset_status(self):
        """
        Reset the team data

        team Goals, goals from opponenet, and points are reset to zero
        """
        self.__goals_for = 0
        self.__goals_against = 0
        self.point = 0

    def simulate_match(self, opponent: "Team", is_knockout: bool = False):
        """
        Simulate a football match against another team

        In knockout mode we have extra time and penalty if needed

        Args:
            opponent: The opposing team
            is_knockout: Whether the match is a knockout match

        Returns:
            tuple:
                - goals scored by this team
                - goals scored by the opponent
                - the winning team or Draw in group matches

        Raises:
            ValueError: If is_knockout is not a boolean
        """
        if not isinstance(is_knockout, bool):
            raise ValueError("is_knockout has to be boolean")
        self.pens = 0
        opponent.pens = 0
        winner = None
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defence / 100) * 0.8
        goals_self = np.random.poisson(lam=lambda_self)

        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defence / 100) * 0.8
        goals_opponent = np.random.poisson(lam=lambda_opponent)

        # group mode
        if not is_knockout:
            if goals_self > goals_opponent:
                winner = self
            elif goals_self < goals_opponent:
                winner = opponent
            else:
                winner = "Draw"

        # knockout mode
        else:
            # 90-min draw -> extra time
            if goals_self == goals_opponent:
                lambda_self *= 0.33
                lambda_opponent *= 0.33
                goals_self += np.random.poisson(lam=lambda_self)
                goals_opponent += np.random.poisson(lam=lambda_opponent)

                if goals_opponent > goals_self:
                    winner = opponent

                # 30-min draw -> 5 penalty
                elif goals_self == goals_opponent:
                    p_self = 0.75 + (self.attack - opponent.defence) / 250
                    p_opponent = 0.75 + (opponent.attack - self.defence) / 250
                    for _ in range(5):
                        if random.random() < p_self:
                            self.pens += 1
                        if random.random() < p_opponent:
                            opponent.pens += 1

                    # 5 penalty draw -> sudden penalty
                    if self.pens == opponent.pens:
                        while True:
                            if random.random() < p_self:
                                self.pens += 1
                            if random.random() < p_opponent:
                                opponent.pens += 1
                            if self.pens != opponent.pens:
                                winner = self if self.pens > opponent.pens else opponent
                                break

                    elif self.pens > opponent.pens:
                        winner = self
                    elif self.pens < opponent.pens:
                        winner = opponent

                elif goals_opponent < goals_self:
                    winner = self
            elif goals_self > goals_opponent:
                winner = self
            elif goals_self < goals_opponent:
                winner = opponent

        self.__goals_for += goals_self
        opponent.__goals_for += goals_opponent

        self.__goals_against += goals_opponent
        opponent.__goals_against += goals_self


        return goals_self, goals_opponent, winner

    def __repr__(self):
        return f'Team(name={self.name}, attack={self.__attack}, defence={self.__defence}, rank={self.__rank})'

    def __str__(self):
        return f"name: {self.name} attack: {self.__attack} defence: {self.__defence} rank: {self.__rank}"