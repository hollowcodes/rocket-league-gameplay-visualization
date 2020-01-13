
import matplotlib.pyplot as plt
import numpy as np


# get player stats
def get_stats(analysis: dict) -> dict:
    players = analysis["players"]

    total_stats = {}
    for player in players:
        stats = {
                    "name": player.get("name"),
                    "team": "blue" if player.get("isOrange") == 0 else "orange",
                    "score": player.get("score"),
                    "goals": player.get("goals"),
                    "assists": player.get("assists"),
                    "saves": player.get("saves"),
                    "shots": player.get("shots"),
                    "bot": player.get("isBot")
                }

        total_stats[player["id"].get("id")] = stats

    return total_stats


# plots player stats
def plot_stats(stats: dict):
    names = [a if (a := stats[player].get("name")) is not None else 0 for player in stats]
    scores = [a if (a := stats[player].get("score")) is not None else 0 for player in stats]
    goals = [a if (a := stats[player].get("goals")) is not None else 0 for player in stats]
    assists = [a if (a := stats[player].get("assists")) is not None else 0 for player in stats]
    saves = [a if (a := stats[player].get("saves")) is not None else 0 for player in stats]
    shots = [a if (a := stats[player].get("shots")) is not None else 0 for player in stats]

    # get indices of blue players and create the color sequence of the bar chart
    blue_team_indices = [i for i, player in enumerate(stats) if stats[player].get("team") == "blue"]
    color_range = ["blue" if i in blue_team_indices else "orange" for i in range(4)]

    plt.style.use("ggplot")

    fig, axs = plt.subplots(2, 3, figsize=(9, 3))
    fig.set_size_inches(8, 4)

    # scores
    axs[0][0].bar(names, scores, align="center", alpha=0.7, color=color_range)
    axs[0][0].set_title("scores")
    # goals
    axs[0][1].bar(names, goals, align="center", alpha=0.7, color=color_range)
    axs[0][1].set_title("goals")
    # assists
    axs[0][2].bar(names, assists, align="center", alpha=0.7, color=color_range)
    axs[0][2].set_title("assists")
    # saves
    axs[1][0].bar(names, saves, align="center", alpha=0.7, color=color_range)
    axs[1][0].set_title("saves")
    # shots
    axs[1][1].bar(names, shots, align="center", alpha=0.7, color=color_range)
    axs[1][1].set_title("shots")

    fig.delaxes(axs[1][2])

    plt.show()


# plot player possession
def plot_possession(analysis: dict):
    players = analysis["players"]

    names, possessions, team_colors = [], [], []
    for player in players:
        name = player.get("name")
        possession = player.get("stats").get("possession").get("possessionTime")

        if not player.get("isBot"):
            names.append(name)
            possessions.append(possession)
            if player.get("isOrange"): team_colors.append((250/255, 147/255, 29/255)) 
            else: team_colors.append((16/255, 104/255, 205/255))

    fig1, ax1 = plt.subplots()
    ax1.pie(possessions, explode=([0.03 for _ in range(len(names))]), labels=names, autopct='%1.1f%%',
                         shadow=True, startangle=90, colors=team_colors)
    ax1.axis("equal")
    plt.title("possession")

    plt.show()

