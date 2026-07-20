# worldcup.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""loading teams, drawing groups, running the group stage, knockout stage, and all simulations"""

from match import Match
from group import Group
from team import Team
from knockoutstage import KnockoutStage
from printer import match_result_printer
import random
import pandas as pd
import matplotlib.pyplot as plt


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
            print(f"\033[38;2;255;0;0m[-] Error: {file_name} not found\033[0m")
            self.file_flag = False
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

        # Convert dictionaries to Group objects
        self.groups = []
        for g in group.keys():
            self.groups.append(Group(g, group[g]))
        return group

    def run_group_stage(self, verbose=True):
        """
        simulate all group matches

        Args:
            verbose: if True, prints the group result
        """
        if not self.groups:
            print("\033[38;2;255;0;0m[-] Error: Seed and Draw is empty - first press 2\033[0m")
            return
        for team in self.teams:
            team.reset_status()
        for i in self.groups:
            i.play_all_matches()
            if verbose:
                print(f" Group {i.name} ".center(46, '='))
            team_list = i.get_ranking()
            if verbose:
                for j in range(0, 2):
                    print(f"{j+1}. \033[38;2;0;149;255m{team_list[j].name:15}: {team_list[j].point:2} pts | {team_list[j].goal_difference:+3} GD | {team_list[j].goals_for:2} GF\033[0m")
                for j in range(2, 4):
                    print(f"{j+1}. {team_list[j].name:15}: {team_list[j].point:2} pts | {team_list[j].goal_difference:+3} GD | {team_list[j].goals_for:2} GF")
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
            
        # Create Round of 16 matches
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
            print(f"|{team_name:^15} | {percent:^5.2f}% |")
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
            print("\033[38;2;255;0;0m[-] No bracket available.\033[0m")
            return
        
        print()
        print(" ROUND OF 16 ".center(40, '='))

        for match in self.round_of_16.matches:
            match_result_printer(match)

        if self.quarterfinals:
            print()
            print(" QUARTER FINALS ".center(40, '='))
            for match in self.quarterfinals.matches:
                match_result_printer(match)

        if self.semifinals:
            print()
            print(" SEMI FINALS ".center(40, '='))

            for match in self.semifinals.matches:
                match_result_printer(match)


        if self.final:
            print()
            print(" FINAL ".center(40, '='))

            match = self.final.matches[0]

            if match.goals1 == match.goals2:
                if match.winner == match.team1.name:
                    print(f"\033[38;2;0;255;0m{match.team1.name:^15} {match.goals1}\033[0m - {match.goals2} {match.team2.name:^15} ({match.team1.pens}-{match.team2.pens} pens)")
                else:
                    print(f"{match.team1.name:^15} {match.goals1} - \033[38;2;0;255;0m{match.goals2} {match.team2.name:^15}\033[0m ({match.team1.pens}-{match.team2.pens} pens)")

            else:
                match_result_printer(match)
            print(f"\nChampion: \033[48;2;0;255;0m\033[38;2;0;0;0m {match.winner.name} \033[0m")
