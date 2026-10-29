"""
Name: Mahnoor Haider
Course: DS2500
Assignment: HW_02
Date: 10/21/25
Name of File: wsl_goals_analysis.py
"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# Folders relative to this file, so the script runs from any directory
PROJECT_DIR = Path(__file__).resolve().parent
FIGURES_DIR = PROJECT_DIR / "figures"

class Team:
    def __init__(self, name, x = 0, y = 0, color = "purple"):
        """
        Parameters:
            name: The name of the team, a string.
            x: The team’s x-position on the matplotlib grid.
            y: The team’s y-position on the matplotlib grid.
            color: The team’s color when rendered on matplotlib.
        Returns: None
        Does: Initializes a Team object with the given name, initial goals l
        ist, position (x, y), and color for plotting. Sets up the team
        object for later use in visualizations and analysis.
        """
        self.name = name
        self.goals = []
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        """
        Parameters: None
        Returns: None
        Does: Renders the team on the matplotlib grid at its current x,
        y position and with its color.
        """
        plt.scatter(self.x, self.y, color=self.color, s=80, marker=">")

    def add_goals(self, goals):
        """
        Parameters: goals: The number of goals scored in a match (int).
        Returns: None
        Does: Append the given goals, an int, to the team’s list of goals.
        """
        self.goals.append(int(goals))

    def get_total_goals(self):
        """
        Parameters: None
        Returns: Total number of goals scored by a team in a match (int).
        Does: Returns the total goals of all the goals in the goals list, an
        int
        """
        total = 0
        for goal in self.goals:
            total += goal
        return total

    def move_next(self):
        """
        Parameters: None
        Returns: None
        Does: Move the team to the right by the amount found in the next
        position in its goals list.
        """
        if self.goals:
            self.x += self.goals.pop(0)

    def reset_goals(self, team_data):
        """
        Parameters: team_data (dict): Nested dictionary with team names as
        keys and matchweek, goals as values.
        Returns: None
        Does: Resets the team’s goals list and repopulates it from team_data
        for calculations or animations. Used to reset after the implementation
        of move_next().
        """
        self.goals = []
        for goal in team_data[self.name].values():
                self.add_goals(goal)

    def __str__(self):
        """
        Parameters: None
        Returns: String representation of the team object.
        Does: Returns a string showing the team’s name, x and y positions,
        and color.
        """
        return f"Team({self.name}, x={self.x}, y={self.y}, color={self.color})"

def main():
    """
    Parameters: None
    Returns: None
    Does:
        - Reads WSL 2023-2024 CSV goal data from a CSV file.
        - Initializes Team objects and assigns colors and positions. Keeps
            all Team objects in a list (called teams).
        - Animates the teams' updated progress for each matchweek using
            matplotlib. Generates the required plots.
        - Calculates and prints answers to 9 questions.
            1. Which team scored the most goals in season 2023-2024?
            2. What was the average (mean) of total goals scored by all the
            teams?
            3. What was the variance of total goals scored by all the teams?
            4. What was the standard deviation of total goals scored by all
            the teams?
            5. What was the median of goals scored in each game by Arsenal?
            6. What was the mode of goals scored in each game by
            Tottenham Hotspur?
            7. Which team has the most consistent goal-scoring pattern?
            8. Which team had the most impressive scoring streak of at least
            2 goals a game?
            9. Which team improved their average goals per game the most in
            the second half?
    """
    # Reading CSV file
    team_data = {}
    # 12 clearly different colors, one per team
    color_list = ["red", "blue", "green", "orange", "purple", "brown",
                  "hotpink", "gray", "olive", "deepskyblue", "black", "gold"]
    with open(PROJECT_DIR / "wsl_goals_2324.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            team_name = row['team']
            row.pop('team')
            converted_row = {int(matchweek): int('0') if goals in [None," ",""]
                else int(goals) for matchweek, goals in row.items()}
            team_data[team_name] = converted_row
    # Initializing Team objects
    teams = []
    team_to_index = {team: index for index, team in enumerate(
        team_data.keys())}
    for index, (name, row) in enumerate(team_data.items()):
        team = (Team(
            name,
            x=0,  # start at 0; move_next() adds week 1's goals in frame 1
            y=team_to_index[name] + 1,
            color=color_list[index % len(color_list)]
        ))
        teams.append(team)
    # Generating required plots
    abbrev = {
        "Arsenal": "ARS",
        "Aston Villa": "AVL",
        "Brighton and Hove Albion": "BHA",
        "Bristol City": "BCFC",
        "Chelsea": "CHE",
        "Everton": "EFC",
        "Leicester City": "LCFC",
        "Liverpool": "LFC",
        "Manchester City": "MCFC",
        "Manchester United": "MUFC",
        "Tottenham Hotspur": "THFC",
        "West Ham United": "WHU"
    }
    for team in teams:
        team.reset_goals(team_data)
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    # also record each frame into a GIF so the race can be shared
    FIGURES_DIR.mkdir(exist_ok=True)
    writer = PillowWriter(fps=2)
    with writer.saving(fig, FIGURES_DIR / "wsl_goals_race.gif", dpi=80):
        for week in range(1, 23):
            ax.clear()
            ax.set_title(f"WSL 2023–2024 Season: Week {week}", fontsize=14)
            ax.set_xlabel("Total Goals Scored", fontsize=12)
            ax.set_ylabel("Teams", fontsize=12)
            ax.set_xlim(0, 80)
            ax.set_ylim(0, len(teams) + 1)
            # label each row with its team instead of a number
            ax.set_yticks([team.y for team in teams])
            ax.set_yticklabels([abbrev[team.name] for team in teams])
            ax.grid(True, linestyle="--", alpha=0.6)
            for team in teams:
                team.move_next()
                team.draw()
                ax.scatter([], [], color=team.color, marker=">",
                           label=team.name)
            handles, labels = ax.get_legend_handles_labels()
            by_label = {label: handles[i] for i, label in enumerate(labels)}
            # legend sits outside the plot so it never covers a team
            ax.legend(by_label.values(), by_label.keys(), loc="center left",
                      bbox_to_anchor=(1.01, 0.5), fontsize=8)
            fig.subplots_adjust(left=0.08, right=0.75)
            plt.pause(0.5)
            writer.grab_frame()
        # hold on the final standings for a few extra frames
        for _ in range(4):
            writer.grab_frame()
    plt.ioff()
    plt.show()
    for team in teams:
        team.reset_goals(team_data)

    # Calculate and print answers to required questions
    #QUESTION 1
    team_most_goals = ""
    max_goals = 0
    for team in teams:
        total_goals = sum(team.goals)
        if total_goals > max_goals:
            max_goals = total_goals
            team_most_goals = team.name
    print("== Season totals ==")
    print(f"Most goals in the 2023-2024 season: {team_most_goals} "
          f"({max_goals} goals)")

    #QUESTION 2
    total_goals_all_teams = sum(sum(team.goals) for team in teams)
    num_teams = len(teams)
    average_all_teams = round((total_goals_all_teams / num_teams), 2)
    print(f"Average season total per team: {average_all_teams}")

    #QUESTION 3
    sum_all_teams_goals = 0
    num_teams = len(teams)
    for team in teams:
        sum_all_teams_goals += sum(team.goals)
    average_all_teams = sum_all_teams_goals / num_teams
    sum_squared_diffs = 0
    for team in teams:
        total_goals = sum(team.goals)
        sum_squared_diffs += (total_goals - average_all_teams) ** 2
    variance = round(sum_squared_diffs / num_teams, 2)
    print(f"Variance of season totals: {variance}")

    #QUESTION 4
    print(f"Standard deviation of season totals: {round(variance**0.5,2)}")

    #QUESTION 5
    list_goals_Arsenal = []
    for matchweek, goals in team_data["Arsenal"].items():
        list_goals_Arsenal.append(goals)
    sorted_list_Arsenal = sorted(list_goals_Arsenal)
    length = len(sorted_list_Arsenal)
    if length % 2 == 1:
        median = sorted_list_Arsenal[length // 2]
    else:
        mid1 = sorted_list_Arsenal[length // 2 - 1]
        mid2 = sorted_list_Arsenal[length // 2]
        median = (mid1 + mid2) / 2
    print("\n== Goals per game ==")
    print(f"Arsenal median: {median:.2f}")

    #QUESTION 6
    list_goals_Tottenham = []
    for matchweek, goals in team_data["Tottenham Hotspur"].items():
        list_goals_Tottenham.append(goals)
    sorted_list_Tottenham = sorted(list_goals_Tottenham)
    seen_numbers = []
    goal_frequency = {}
    for num in sorted_list_Tottenham:
        if num not in seen_numbers:
            seen_numbers.append(num)
            goal_frequency[num] = 1
        else:
            goal_frequency[num] += 1
    max_occurrence = max(goal_frequency.values())
    modes = [key for key, value in goal_frequency.items() if value ==
             max_occurrence]
    if len(modes) == 1:
        mode_Tottenham = modes[0]
    else:
        mode_Tottenham = modes
    print(f"Tottenham Hotspur mode: {mode_Tottenham}")

    #QUESTION 7
    team_coeff_vars = {}
    for team in teams:
        total_games_played = len(team.goals)
        mean_goals = sum(team.goals) / total_games_played
        variance = (sum((goal - mean_goals) ** 2 for goal in
                        team.goals)/total_games_played)
        std_dev_team = variance**0.5
        coeff_var = std_dev_team / mean_goals
        team_coeff_vars[team.name] = coeff_var
    most_consistent_team = min(team_coeff_vars, key=team_coeff_vars.get)
    lowest_coeff_var = round(team_coeff_vars[most_consistent_team], 2)
    print("\n== Scoring patterns ==")
    print(f"Most consistent scorer: {most_consistent_team} "
          f"(coefficient of variation {lowest_coeff_var})")

    # QUESTION 8
    team_streaks = {}
    for team in teams:
        longest_streak = 0
        current_streak = 0
        for goals in team.goals:
            if goals >= 2:
                current_streak += 1
                if current_streak > longest_streak:
                    longest_streak = current_streak
            else:
                current_streak = 0
        team_streaks[team.name] = longest_streak
    best_team = max(team_streaks, key=team_streaks.get)
    print(f"Longest streak of 2+ goals per game: {best_team} "
          f"({team_streaks[best_team]} games in a row)")

    # QUESTION 9
    team_improvements = {}
    for team in teams:
        goals = team.goals
        halfway = len(goals) // 2
        first_half_avg = sum(goals[:halfway]) / halfway
        second_half_avg = sum(goals[halfway:]) / (len(goals) - halfway)
        improvement = second_half_avg - first_half_avg
        team_improvements[team.name] = improvement
    most_improved_team = max(team_improvements, key=team_improvements.get)
    most_improvement_value = round(team_improvements[most_improved_team], 2)
    print(f"Biggest second-half improvement: {most_improved_team} "
          f"(+{most_improvement_value} goals per game)")

# Main function to call functions and test them
if __name__ == "__main__":
    main()