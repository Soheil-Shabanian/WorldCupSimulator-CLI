# main.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""command line menu"""

import ctypes
from tkinter.filedialog import askopenfilename
from rich.console import Console
from rich.table import Table
from worldcup import WorldCupSimulator
ctypes.windll.shcore.SetProcessDpiAwareness(True)


def main():
    obj = WorldCupSimulator()
    txt = """\n(1) Import teams from csv file
(2) Seed and draw groups
(3) Running group game and showing the table
(4) Running full game (group + final) & showing the best team
(5) Simulate 1000
(6) Showing last bracket
(7) EXIT\n"""

    # main app loop
    while True:
        # prints the menu option
        print(txt)
        
        try:
            num = int(input(">>> "))
        except ValueError:
            print('\033[38;2;255;0;0m[-] Error: type a number\033[0m\n')
            continue

        if not 1 <= num <= 7:
            print("\033[38;2;255;0;0m[-] Error: Type a number between 1 and 7.\033[0m")
            continue

        if num == 1:
            obj.data_reset(True)
            # file_path = "worldcup_2026_teams.csv"
            file_path = askopenfilename(title="Select file:", filetypes=[("CSV Files", ".csv")])
            obj.load_teams_from_csv(file_path)
        elif num in (2, 3, 4, 5, 6):
            if not obj.file_flag:
                print("\033[38;2;255;0;0m[-] Error: First load the CSV file (option 1).\033[0m")
                continue

            if num == 2:
                result: dict[str, list] = obj.seed_and_draw_groups()

                table = Table(title="Group Table")
                table.add_column("Group", justify="center")
                table.add_column("Team 1")
                table.add_column("Team 2")
                table.add_column("Team 3")
                table.add_column("Team 4")

                for group_name, teams in result.items():
                    table.add_row(
                        group_name,
                        teams[0].name,
                        teams[1].name,
                        teams[2].name,
                        teams[3].name,
                    )

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
                            print("\033[38;2;255;0;0m[-] Simulation count must be greater than zero.\033[0m")
                            continue
                        obj.most_likely_champion(simulations)
                        break
                    except ValueError:
                        print("\033[38;2;255;0;0m[-] Please enter a valid integer\033[0m")
            elif num == 6:
                obj.display_bracket()
        elif num == 7:
            break

if __name__ == "__main__":
    main()