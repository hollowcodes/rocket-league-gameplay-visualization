
from gameplay_stats import get_stats
from utils import get_team_by_name, get_player_by_id
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import numpy as np
import math


class PositionHeatmap:
    def __init__(self, dataframe, analysis: dict, map_size: tuple=(8192, 10240), down_scale: int=100):
        self.dataframe = dataframe
        self.analysis = analysis

        # contains player ids
        self.players = [get_player_by_id(analysis, id_) for id_ in get_stats(analysis)]
        self.players.insert(0, ("ball", "ball"))

        self.map_size = map_size

    # translate coordinates (create cartesian coordinate system, positive values only) and rescale them
    def _translate_coordinates(self, coords: tuple, down_scale: int=100):
        x = int(np.floor((-1 * float(coords[0])) + (self.map_size[0] / 2)))
        y = int(np.floor(float(coords[1]) + (self.map_size[1] / 2)))

        # rescaling
        x, y = int((x / down_scale)), int((y / down_scale))

        return (x, y)

    # get player coordinates of every frame
    def _get_coordinates(self, player, down_scale: int=100):
        # find the column which contains the x-positions (because the columns are not sorted)
        for i in range(0, 20): 
            c = "." + str(i) if i is not 0 else ""
            if self.dataframe[(player + c)].tolist()[0] == "pos_x": 
                x = self.dataframe[(player + c)].tolist()
                break

        # find the column which contains the y-positions (because the columns are not sorted)
        for i in range(0, 20):
            # column name is something like 'name.1'
            c = "." + str(i) if i is not 0 else ""
            if self.dataframe[(player + c)].tolist()[0] == "pos_y": 
                y = self.dataframe[(player + c)].tolist()
                break
        
        # remove the labels
        x.remove("pos_x")
        y.remove("pos_y")

        # translate coordinates
        coordinates = list(zip(x, y))
        for i in range(len(coordinates)):
            try:
                coordinates[i] = self._translate_coordinates(coordinates[i], down_scale=down_scale)
            except:
                pass

        return coordinates

    # create heatmap
    def create_heatmap(self, down_scale: int=100):
        #all_player_coordinates = [[get_player_by_id(self.analysis, id_), self._get_coordinates(get_player_by_id(self.analysis, id_)[0], down_scale=down_scale)] for id_ in self.players]
        all_player_coordinates = [[player, self._get_coordinates(player[0], down_scale=down_scale)[100:]] for player in self.players]

        fig, axs = plt.subplots(1, len(self.players))

        # create heatmaps for all players in 'self.players'
        all_player_heatmaps = []
        for i, player_state in enumerate(all_player_coordinates):
            scaled_map_size = (int(self.map_size[0] / down_scale) + 2, int(self.map_size[1] / down_scale) + 2)
            map_ = np.zeros(scaled_map_size)

            current_player, team, current_coordinates = player_state[0][0], player_state[0][1], player_state[1]

            for coordinate in current_coordinates:
                x, y = coordinate[0], coordinate[1]
                # coordinates can be nans if the player joined later or left earlier
                if not (math.isnan(x) or math.isnan(y)):
                    map_[x][y] += 1
                else:
                    pass

            all_player_heatmaps.append([current_player, map_])

        # if 'self.players' contains just one player/ball, the 'axs' is not a list and therefore not iterable 
        # -> make it a list
        if not isinstance(axs, np.ndarray):
            axs = [axs]
        
        # plot subplots
        for i, ax in enumerate(axs):
            ax.matshow(all_player_heatmaps[i][1])
            ax.set_title(all_player_heatmaps[i][0] + "\n")

        plt.style.use("seaborn-dark-palette")
        plt.show()

    # create one frame of the tracemap
    def _create_tracemap(self, i, ax, all_player_coordinates, down_scale):
        scaled_map_size = (int(self.map_size[0] / down_scale) + 1, int(self.map_size[1] / down_scale) + 1)
        map_ = np.zeros(scaled_map_size)

        current_game_state = []
        for idx, player_state in enumerate(all_player_coordinates):

            current_player, team, x, y = player_state[0][0], player_state[0][1], player_state[1][i][0], player_state[1][i][1]
            #team_id = 2 if team == "Orange" else 3
            team_id = 1

            if team == "orange":
                team_id = 2
            elif team == "blue":
                team_id = 3
            elif team_id == "ball":
                team_id = 4

            # coordinates can be nans if the player joined later or left earlier
            if not (math.isnan(x) or math.isnan(y)):
                try:
                    map_[x][y] = team_id
                except:
                    # catch weird out of bounds error
                    pass

        ax.clear()
        ax.matshow(map_, cmap=ListedColormap(["white", "red", "orange", "blue"]))#, "black", "blue", "green", "yellow"]))

    # show an animated map that shows the trace of a player/ball
    def animate_tracemap(self, down_scale: int=100):
        # get coordinates, skip most of the kick-off
        all_player_coordinates = [[player, self._get_coordinates(player[0], down_scale=down_scale)[100:]] for player in self.players]

        # skip every 'self.down_scale' frame
        for i in range(len(all_player_coordinates)):
            del all_player_coordinates[1][(down_scale - 1)::down_scale]

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ani = FuncAnimation(fig, self._create_tracemap, frames=range(0, len(all_player_coordinates[0][1]) - 1), fargs=(ax, all_player_coordinates, down_scale), interval=10)
        plt.tight_layout()
        plt.show()
    


"""
TODO

    [ ] left axis = blue, right axis = orange
    [ ] tracemap colors
    [ ] tracemap legend

"""


