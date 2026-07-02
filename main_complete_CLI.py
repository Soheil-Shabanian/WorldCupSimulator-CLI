import random
import pandas as pd
import numpy as np
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
# import ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(True)


class Team:
    def __init__(self, name: str, attack: int, defence: int, rank: int):
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
        return self.__goals_against

    @property
    def goals_for(self):
        return self.__goals_for

    @property
    def attack(self):
        return self.__attack

    @attack.setter
    def attack(self, value):
        if value < 0:
            raise ValueError("Attack value is wrong.")
        self.__attack = value

    @property
    def defence(self):
        return self.__defence

    @defence.setter
    def defence(self, value):
        if value < 0:
            raise ValueError("Defence value is wrong.")
        self.__defence = value

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        if value < 0:
            raise ValueError("Rank value is wrong.")
        self.__rank = value

    @property
    def goal_difference(self):
        return self.__goals_for - self.__goals_against

    def reset_status(self):
        self.__goals_for = 0
        self.__goals_against = 0
        self.point = 0

    def simulate_match(self, opponent: "Team", is_knockout=False):
        if not isinstance(is_knockout, bool):
            raise ValueError("is_knockout has to be boolean")
        self.pens = 0
        opponent.pens = 0
        winner = None
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defence / 100) * 0.8
        goals_self = np.random.poisson(lam=lambda_self)

        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defence / 100) * 0.8
        goals_opponent = np.random.poisson(lam=lambda_opponent)


        if not is_knockout: # group mode
            if goals_self > goals_opponent:
                winner = self
            elif goals_self < goals_opponent:
                winner = opponent
            else:
                winner = "Draw"
            # print(f"{self.name:^15} {goals_self:^2} | {goals_opponent:^3} {opponent.name:^15}")
            # print('-'*50)

        else: # final enter to 90 min
            if goals_self == goals_opponent:
                # print(f"{self.name} {goals_self} | {goals_opponent} {opponent.name} --> 90 min: draw *** entering to 30 min")
                lambda_self *= 0.33
                lambda_opponent *= 0.33
                goals_self += np.random.poisson(lam=lambda_self)
                goals_opponent += np.random.poisson(lam=lambda_opponent)
                if goals_opponent > goals_self:
                    winner = opponent

                elif goals_self == goals_opponent:
                    # print(f"{self.name} {goals_self} | {goals_opponent} {opponent.name} --> 30 min: draw *** entering to 5 penalty")

                    p_self = 0.75 + (self.attack - opponent.defence) / 250
                    p_opponent = 0.75 + (opponent.attack - self.defence) / 250
                    for _ in range(5):
                        if random.random() < p_self:
                            self.pens += 1
                        if random.random() < p_opponent:
                            opponent.pens += 1

                    if self.pens == opponent.pens: # enter to Sudden Death
                        # print(f"{self.name} {p_goals_self} | {p_goals_opponent} {opponent.name} --> 5 round penalty: draw *** entering Sudden Death penalty")
                        while True:
                            if random.random() < p_self:
                                self.pens += 1
                            if random.random() < p_opponent:
                                opponent.pens += 1
                            if self.pens != opponent.pens:
                                winner = self if self.pens > opponent.pens else opponent
                                # print(f"after Sudden Death penalty result: {self.name} {p_goals_self} | {p_goals_opponent} {opponent.name}")
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
    def __init__(self, team1: "Team", team2: "Team", is_knockout: bool):
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.winner: Team | None = None
        self.is_knockout = is_knockout

    def play(self):
        result = self.team1.simulate_match(self.team2, self.is_knockout)
        self.goals1 = result[0]
        self.goals2 = result[1]
        self.winner = result[2]

    def __str__(self):
        return f"Match({self.team1}, {self.team2})"

    def __repr__(self):
        return f"Match({self.team1}, {self.team2})"


class Group:
    def __init__(self, name: str, teams: list[Team]):
        self.name = name
        self.teams = teams

    def play_all_matches(self):
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
        group_result = sorted(self.teams, key=lambda t: (t.point, t.goal_difference, t.goals_for), reverse=True)
        return group_result

    def advance_teams(self):
        first_team = self.get_ranking()[0]
        second_team = self.get_ranking()[1]
        return first_team, second_team

    def __str__(self):
        return f"Group(name={self.name}, teams={self.teams})"

    def __repr__(self):
        return f"Group(name={self.name}, teams={self.teams})"


class KnockoutStage:
    def __init__(self, round_name: str, matches: list[Match]):
        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        for match in self.matches:
            match.play()

    def get_winners(self):
        winners_team_name: list[Team] = [match.winner for match in self.matches]
        return winners_team_name

    def display_results(self, verbose):
        if verbose:
            if self.round_name == "Final":
                print(f"{self.round_name} winner: {self.get_winners()[0].name}")
            else:
                print(f"\n{self.round_name} winners:")
                print(" Chart 1 ".center(20, '-'))
                i = 0
                for team_name in self.get_winners():
                    if i == len(self.matches)//2:
                        print(" Chart 2 ".center(20, '-'))
                    print(f"{team_name.name:^20}")
                    i += 1


class WorldCupSimulator:
    def __init__(self):
        self.group_game_num = 0
        self.teams: list[Team] = []
        self.groups: list[Group] = []
        self.round_of_16: KnockoutStage = None
        self.quarterfinals: KnockoutStage = None
        self.semifinals: KnockoutStage = None
        self.final: KnockoutStage = None

    def load_teams_from_csv(self, file_name):
        data = pd.read_csv(file_name).values
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

    def seed_and_draw_groups(self):
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
        if not self.groups:
            print("Seed and Draw empty - first press 2")
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
        self.group_game_num += 1

    def setup_knockout_bracket(self):
        all_matches = []
        bracket_r = []
        bracket_l = []
        i = 0
        for group in self.groups:
            g = group.advance_teams() # (first_team, second_team)
            if i % 2 == 0:
                bracket_r.append(g[0])
            else:
                bracket_l.append(g[1])
            i += 1

        i = 0
        for group in self.groups:
            g = group.advance_teams()  # (first_team, second_team)
            if i % 2 == 0:
                bracket_r.append(g[1])
            else:
                bracket_l.append(g[0])
            i += 1

            # print(f"{group.name}1: {g[0]} | {group.name}2: {g[1]}")
        for t1, t2 in zip(bracket_r, bracket_l):
            all_matches.append(Match(t1, t2, True))


        self.round_of_16 = KnockoutStage("Round Of 16", all_matches)

        return all_matches

    def run_knockout_bracket(self, verbose=True):

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
        for team in self.teams:
            team.reset_status()

        if not seed:
            self.seed_and_draw_groups()

        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None

    def run_full_simulation(self):
        self.data_reset(self.group_game_num != 0)
        self.run_group_stage()
        self.run_knockout_bracket()

    def most_likely_champion(self, num_simulations=1000):
        champions = {}

        for _ in range(num_simulations):

            self.data_reset(False)
            self.run_group_stage(verbose=False)
            self.run_knockout_bracket(verbose=False)

            champion = self.final.get_winners()[0]

            if champion.name not in champions:
                champions[champion.name] = 1
            else:
                champions[champion.name] += 1

        print("\nMost Likely Champions:\n")

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
            print(f"{team_name:15} --> {percent:.2f}%")
        self._plt_most_likely_champion(plt_bar_names, plt_bar_values)

    def _plt_most_likely_champion(self, names, values):
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
    file_flag = False
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
            file_path = "worldcup_2026_teams.csv"
            # file_path = askopenfilename(title="Select file:", filetypes=[("CSV Files", ".csv")])
            obj.load_teams_from_csv(file_path)
            print(f"[+] file {file_path} loaded")
            file_flag = True
        elif num in (2, 3, 4, 5, 6):
            if not file_flag:
                print("[-] Error: First load the CSV file (option 1).")
                continue
            if num == 2:
                result: dict = obj.seed_and_draw_groups()
                for item in result:
                    print(f"Group {item}: ", end='')
                    for i in range(4):
                        print(f"{result[item][i].name:^15} | ", end='')
                    print()
                    print(81*"-")
            elif num == 3:
                obj.run_group_stage()
            elif num == 4:
                obj.run_full_simulation()
            elif num == 5:
                while True:
                    try:
                        simulations = int(input("Number of simulations: "))
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

