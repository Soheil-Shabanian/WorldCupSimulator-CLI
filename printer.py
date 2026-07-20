# printer.py

# Student Name: Soheil Shabanian
# Student Code: 404130833
# Project name: World Cup Simulator
# 1405/04/14

"""a function for displaying match results"""

from match import Match

def match_result_printer(match: Match):
    """print the result of a match with color"""
    if match.winner == match.team1:
        print(f"\033[38;2;0;255;0m{match.team1.name:^15} {match.goals1}\033[0m - {match.goals2} {match.team2.name:^15} | Winner: {match.winner.name}")
    else:
        print(f"{match.team1.name:^15} {match.goals1} - \033[38;2;0;255;0m{match.goals2} {match.team2.name:^15}\033[0m | Winner: {match.winner.name}")
