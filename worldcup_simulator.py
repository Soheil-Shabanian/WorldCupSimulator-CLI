# worldcup_simulator.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/10


import random
import pandas as pd
import numpy as np
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)


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

    def simulate_match(self, opponent: "Team", is_knockout=False):
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


        if not is_knockout:
            if goals_self > goals_opponent:
                winner = self
            elif goals_self < goals_opponent:
                winner = opponent
            else:
                winner = "Draw"

        else:
            if goals_self == goals_opponent:
                lambda_self *= 0.33
                lambda_opponent *= 0.33
                goals_self += np.random.poisson(lam=lambda_self)
                goals_opponent += np.random.poisson(lam=lambda_opponent)
                if goals_opponent > goals_self:
                    winner = opponent

                elif goals_self == goals_opponent:
                    p_self = 0.75 + (self.attack - opponent.defence) / 250
                    p_opponent = 0.75 + (opponent.attack - self.defence) / 250
                    for _ in range(5):
                        if random.random() < p_self:
                            self.pens += 1
                        if random.random() < p_opponent:
                            opponent.pens += 1

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
        self.winner: Team | None = None
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
        return f"Match({self.team1}, {self.team2})"

    def __repr__(self):
        return f"Match({self.team1}, {self.team2})"


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
        first_team = self.get_ranking()[0]
        second_team = self.get_ranking()[1]
        return first_team, second_team

    def __str__(self):
        return f"Group(name={self.name}, teams={self.teams})"

    def __repr__(self):
        return f"Group(name={self.name}, teams={self.teams})"


class KnockoutStage:
    """
    represents a knockout stage

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
        for match in self.matches:
            match.play()

    def get_winners(self):
        """
        return the winners of all matches in the round

        Returns:
            a list containing the winning teams
        """
        winners_team_name: list[Team] = [match.winner for match in self.matches]
        return winners_team_name

    def display_results(self, verbose):
        """
        display the results of the knockout stage

        if verbose is True, the score and winner of each match are
        printed. For the final, the tournament champion is also shown.

        Args:
            verbose: option for printing or not
        """
        if verbose:
            if self.round_name == "Final":
                print(f"\n{self.round_name} winners:")
                for match in self.matches:
                    print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15} | Winner: {match.winner.name}")
                print(f"\n{self.round_name} winner: {self.get_winners()[0].name}")

            else:
                print(f"\n{self.round_name} winners:")
                print(" Table-1 ".center(50, '-'))
                i = 0
                for match in self.matches:
                    if i == len(self.matches)//2:
                        print()
                        print(" Table-2 ".center(50, '-'))
                    print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15} | Winner: {match.winner.name}")
                    i += 1


class WorldCupSimulator:
    """
    simulates a complete World Cup

    The simulator loads team data
    group draw
    simulates group and knockout matches
    probabilities for winners in simulations and display the results
    """
    def __init__(self):
        """
        initialize the World Cup simulator

        creates empty list for teams, groups, and knockout
        """
        self.file_flag = False
        self.group_game_flag = False
        self.teams: list[Team] = []
        self.groups: list[Group] = []
        self.round_of_16: KnockoutStage = None
        self.quarterfinals: KnockoutStage = None
        self.semifinals: KnockoutStage = None
        self.final: KnockoutStage = None

    def load_teams_from_csv(self, file_name):
        """
        load team information from a CSV file

        the CSV file must contain exactly 32 teams

        Args:
            file_name: path to the CSV file

        Raises:
            ValueError: if the file does not contain exactly 32 teams
        """
        try:
            data = pd.read_csv(file_name).values
        except FileNotFoundError:
            print(f"[-] Error: {file_name} not found")
            return

        self.teams.clear()
        for i in data:
            self.teams.append(Team(
                name=i[0],
                attack=i[1],
                defence=i[2],
                rank=i[3])
            )
        if len(self.teams) != 32:
            raise ValueError("the number of rows must be 32 (data) + 1 (header)")
        print(f"[+] file {file_name} loaded")
        self.file_flag = True

    def seed_and_draw_groups(self):
        """
        seed teams based on their rankings and randomly draw groups

        Returns:
            a dictionary mapping group names to their assigned teams.
        """
        seed = {
            "seed_1": [],
            "seed_2": [],
            "seed_3": [],
            "seed_4": [],
        }
        group = {
            'A': [],
            'B': [],
            'C': [],
            'D': [],
            'E': [],
            'F': [],
            'G': [],
            'H': [],
        }

        for i in self.teams:
            if 1 <= i.rank <= 8:
                seed["seed_1"].append(i)
            elif 9 <= i.rank <= 16:
                seed["seed_2"].append(i)
            elif 17 <= i.rank <= 24:
                seed["seed_3"].append(i)
            elif 25 <= i.rank <= 32:
                seed["seed_4"].append(i)

        random.shuffle(seed["seed_1"])
        random.shuffle(seed["seed_2"])
        random.shuffle(seed["seed_3"])
        random.shuffle(seed["seed_4"])

        for i, g_name in enumerate(group.keys()):
            group[g_name].append(seed["seed_1"].pop())
            group[g_name].append(seed["seed_2"].pop())
            group[g_name].append(seed["seed_3"].pop())
            group[g_name].append(seed["seed_4"].pop())

        self.groups = []
        for g in group.keys():
            self.groups.append(Group(g, group[g]))
        return group

    def run_group_stage(self, verbose=True):
        """
        simulate all group matches

        teams are ranked according to points, goal difference and goals scored.

        Args:
            verbose: if True, prints the group result
        """
        if not self.groups:
            print("[-] Error: Seed and Draw is empty - first press 2")
            return
        for team in self.teams:
            team.reset_status()
        for i in self.groups:
            i.play_all_matches()
            if verbose:
                print(f" Group {i.name} ".center(46, '='))
            team_list = i.get_ranking()
            if verbose:
                for j in range(4):
                    print(f"{j+1}. {team_list[j].name:15}: {team_list[j].point:2} pts | {team_list[j].goal_difference:+2} GD | {team_list[j].goals_for:2} GF")
                print()
        self.group_game_flag = True

    def setup_knockout_bracket(self):
        """
        create the Round of 16 knockout bracket
        """
        all_matches = []
        bracket_r = []
        bracket_l = []
        i = 0
        for group in self.groups:
            g = group.advance_teams()
            if i % 2 == 0:
                bracket_r.append(g[0])
            else:
                bracket_l.append(g[1])
            i += 1

        i = 0
        for group in self.groups:
            g = group.advance_teams()
            if i % 2 == 0:
                bracket_r.append(g[1])
            else:
                bracket_l.append(g[0])
            i += 1

        for t1, t2 in zip(bracket_r, bracket_l):
            all_matches.append(Match(t1, t2, True))


        self.round_of_16 = KnockoutStage("Round Of 16", all_matches)

    def run_knockout_bracket(self, verbose=True):
        """
        simulate the knockout stage

        Args:
            verbose: if True, prints the results of each round
        """
        self.setup_knockout_bracket()
        self.round_of_16.play_round()
        self.round_of_16.display_results(verbose)

        winners = self.round_of_16.get_winners()
        list_quarterfinals_matches = [Match(winners[i], winners[i + 1], True) for i in range(0, len(winners), 2)]
        self.quarterfinals = KnockoutStage("Quarter Finals", list_quarterfinals_matches)
        self.quarterfinals.play_round()
        self.quarterfinals.display_results(verbose)

        winners = self.quarterfinals.get_winners()
        list_semifinal_matches = [Match(winners[i], winners[i + 1], True) for i in range(0, len(winners), 2)]
        self.semifinals = KnockoutStage("Semi Finals", list_semifinal_matches)
        self.semifinals.play_round()
        self.semifinals.display_results(verbose)

        winners = self.semifinals.get_winners()
        self.final = KnockoutStage("Final", [Match(winners[0], winners[1], True)])
        self.final.play_round()
        self.final.display_results(verbose)

    def data_reset(self, seed):
        """
        Reset all data before a new simulation

        Args:
            seed: if False, generates a new group draw
        """
        for team in self.teams:
            team.reset_status()

        if not seed:
            self.seed_and_draw_groups()

        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None

    def run_full_simulation(self):
        """
        run a complete world cup simulation
        """
        self.data_reset(self.group_game_flag)
        self.run_group_stage()
        self.run_knockout_bracket()

    def most_likely_champion(self, num_simulations=1000):
        """
        calculate each team probability for winning

        Args:
            num_simulations: number of simulations to run
        """
        champions = {team.name: 0 for team in self.teams}

        for _ in range(num_simulations):

            self.data_reset(False)
            self.run_group_stage(verbose=False)
            self.run_knockout_bracket(verbose=False)

            final_winner = self.final.get_winners()[0]
            champions[final_winner.name] += 1

        print(f"\nResult of {num_simulations} simulation:\n")

        sorted_champions = sorted(
            champions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        plt_bar_names = []
        plt_bar_values = []
        for team_name, wins in sorted_champions:
            percent = (wins / num_simulations) * 100
            plt_bar_names.append(team_name)
            plt_bar_values.append(percent)
            print(f"|{team_name:^15} | {percent:^5.2f}%|")
        self._plt_most_likely_champion(plt_bar_names, plt_bar_values)

    def _plt_most_likely_champion(self, names, values):
        """
        display a bar chart of championship probabilities

        Args:
            names: list of team names
            values: list for championship percentages
        """
        plt.figure(figsize=(12, 5))

        plt.title("World Cup Simulator", fontsize=18, fontweight='bold')
        plt.xlabel("Teams", fontsize=14, fontweight='bold')
        plt.ylabel("Wins (%)", fontsize=14, fontweight='bold')
        plt.subplots_adjust(
            left=0.1,
            right=0.95,
            bottom=0.3,
            top=0.9
        )

        plt.bar(names, values)
        plt.xticks(rotation=90, fontsize=12)
        plt.show()

    def display_bracket(self):
        """
        display the knockout bracket and results
        """
        if self.round_of_16 is None:
            print("No bracket available.")
            return
        
        print()
        print(" ROUND OF 16 ".center(40, '='))

        for match in self.round_of_16.matches:
            print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15} | Winner: {match.winner.name}")

        if self.quarterfinals:
            print()
            print(" QUARTER FINALS ".center(40, '='))
            for match in self.quarterfinals.matches:
                print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15} | Winner: {match.winner.name}")

        if self.semifinals:
            print()
            print(" SEMI FINALS ".center(40, '='))

            for match in self.semifinals.matches:
                print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15} | Winner: {match.winner.name}")


        if self.final:
            print()
            print(" FINAL ".center(40, '='))

            match = self.final.matches[0]

            if match.goals1 == match.goals2:
                print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15} ({match.team1.pens}-{match.team2.pens} pens)")
            else:
                print(f"{match.team1.name:^15} {match.goals1} - {match.goals2} {match.team2.name:^15}")
            print(f"\nChampion: {match.winner.name}")


def run_main():
    obj = WorldCupSimulator()
    txt = """\n(1) Import teams from csv file
(2) seed and draw groups
(3) running group game and showing the table
(4) running full game (group + final) & showing the best team
(5) simulate 1000
(6) showing last bracket
(7) exit\n""".title()
    
    while True:
        print(txt)
        try:
            num = int(input(">>> "))
        except ValueError:
            print('[-] Error: type a number\n')
            continue

        if not 1 <= num <= 7:
            print("[-] Error: Type a number between 1 and 7.")
            continue

        if num == 1:
            obj.data_reset(True)
            # file_path = "worldcup_2026_teams.csv"
            file_path = askopenfilename(title="Select file:", filetypes=[("CSV Files", ".csv")])
            obj.load_teams_from_csv(file_path)
        elif num in (2, 3, 4, 5, 6):
            if not obj.file_flag:
                print("[-] Error: First load the CSV file (option 1).")
                continue

            if num == 2:
                result: dict = obj.seed_and_draw_groups()
                table = Table(title="Group Table")

                table.add_column("Group", justify="center")
                table.add_column("Team 1")
                table.add_column("Team 2")
                table.add_column("Team 3")
                table.add_column("Team 4")

                for i in result:
                    table.add_row(i, result[i][0].name, result[i][1].name, result[i][2].name, result[i][3].name)

                Console().print(table)
            elif num == 3:
                obj.run_group_stage()
            elif num == 4:
                obj.run_full_simulation()
            elif num == 5:
                while True:
                    try:
                        simulations = int(input("[*] Number of simulations: "))
                        if simulations <= 0:
                            print("[-] Simulation count must be greater than zero.")
                            continue
                        obj.most_likely_champion(simulations)
                        break
                    except ValueError:
                        print("[-] Please enter a valid integer")
            elif num == 6:
                obj.display_bracket()
        elif num == 7:
            break


run_main()

