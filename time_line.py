
import numpy as np
import matplotlib.pyplot as plt
from utils import get_player_by_id, get_time_by_frames
from plot_utils import timeline_plot


class Timeline:
    def __init__(self, analysis: dict):
        self.analysis = analysis
        self.total_frames = analysis["gameMetadata"]["frames"]
        self.total_time = analysis["gameMetadata"]["length"]

    # get goal information of the match
    def _get_goals(self):
        goals = self.analysis["gameMetadata"]["goals"]

        times = []
        goal_info = []
        teams = []
        for goal in goals:
            time = get_time_by_frames(self.total_frames, self.total_time, goal.get("frameNumber"))
            player, team_ = get_player_by_id(self.analysis, goal.get("playerId").get("id"))

            times.append(time)
            goal_info.append("goal: " + player)
            teams.append(team_)

        return times, goal_info, teams

    # get demolation information of the match
    def _get_demolations(self):
        try:
            demos = self.analysis["gameMetadata"]["demos"]
        except KeyError:
            return [0], [0], [0]

        times = []
        demo_info = []
        teams = []
        for demo in demos:
            time = get_time_by_frames(self.total_frames, self.total_time, demo.get("frameNumber"))
            attacker, att_team = get_player_by_id(self.analysis, demo.get("attackerId").get("id"))
            victim, vic_team = get_player_by_id(self.analysis, demo.get("victimId").get("id"))

            times.append(time)
            demo_info.append((attacker + " -> " + victim))
            teams.append(att_team)

        return times, demo_info, teams

    # plot actions on a time-line
    def _plot_timeline(self, times: list, actions: list, teams: list):
        
        """ from the matplotlib documentation (modified) """

        levels = np.tile([-5, 5, -3, 3, -1, 1],
                    int(np.ceil(len(times)/6)))[:len(times)]
                    
        plt.style.use("ggplot")

        fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
        ax.set(title="timeline")

        markerline, _, _ = ax.stem(times, levels, linefmt="C3-", basefmt="k-", use_line_collection=False)

        plt.setp(markerline, mec="k", mfc="w", zorder=3)

        vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
        for d, l, r, va, c in zip(times, levels, actions, vert, teams):
            if c == None: c = "black"
            ax.annotate(r, xy=(d, l), xytext=(3, np.sign(l)*3),
                        textcoords="offset points", va=va, ha="left", color=c)

        plt.setp(ax.get_xticklabels())
        ax.get_yaxis().set_visible(False)

        ax.plot(self.total_time + 25, 0)
        ax.margins(y=0.1)
        plt.show()

    # plot all given gameplay-actions
    def plot(self, show=["goals", "demos", "saves"]):
        times, actions, teams = [0], ["start"], [None]
        
        for action in show:
            if action == "goals":
                goal_times, goals, goal_team = self._get_goals()
                times.extend(goal_times)
                actions.extend(goals)
                teams.extend(goal_team)
            
            elif action == "demos":
                demolation_times, demolations, demolation_team = self._get_demolations()
                times.extend(demolation_times)
                actions.extend(demolations)
                teams.extend(demolation_team)

            elif action == "saves":
                pass

        times.append(self.total_time)
        actions.append("end: " + str(round(self.total_time, 2)))
        teams.append(None)
        
        self._plot_timeline(times, actions, teams)

            




        

        

    