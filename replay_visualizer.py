
from gameplay_stats import get_stats
from utils import get_team_by_name, get_player_by_id
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
import numpy as np
import math


class ShowReplay:
    def __init__(self, dataframe, analysis: dict, map_size: tuple=(8192, 10240, 2044)):
        self.dataframe = dataframe
        self.analysis = analysis

        # contains player ids
        self.players = [get_player_by_id(analysis, id_) for id_ in get_stats(analysis)]
        self.players.insert(0, ("ball", "ball"))

        self.down_scale = 100

        self.map_size_original = map_size

        # map-height to map-length ratio is 1:5
        self.map_size = (int(map_size[0] / self.down_scale), int(map_size[1] / self.down_scale), int(int(map_size[0] / self.down_scale) / 5))

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1, projection="3d")

    # translate coordinates (create cartesian coordinate system, positive values only) and rescale them
    def _translate_coordinates(self, coords: tuple):
        x = int(np.floor((-1 * float(coords[0])) + (self.map_size_original[0] / 2)))
        y = int(np.floor(float(coords[1])) + (self.map_size_original[1] / 2))
        z = float(coords[2])

        # rescaling
        x, y, z = int((x / self.down_scale)), int((y / self.down_scale)), int(z / self.down_scale / 5)
        return (x, y, z)

    # get player coordinates of every frame
    def _get_coordinates(self, player):
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

        # find the column which contains the z-positions (because the columns are not sorted)
        for i in range(0, 20):
            # column name is something like 'name.1'
            c = "." + str(i) if i is not 0 else ""
            if self.dataframe[(player + c)].tolist()[0] == "pos_z": 
                z = self.dataframe[(player + c)].tolist()
                break
        
        # remove the labels
        x.remove("pos_x")
        y.remove("pos_y")
        z.remove("pos_z")

        # translate coordinates
        coordinates = list(zip(x, y, z))
        for i in range(len(coordinates)):
            try:
                coordinates[i] = self._translate_coordinates(coordinates[i])
            except:
                pass

        return coordinates

    def _create_map(self, i, all_player_coordinates, goal_coordinates):
        self.ax.clear()

        # create start and end point of map
        self.ax.scatter(0, 0, 0, color="white")
        self.ax.scatter(self.map_size[0], self.map_size[1], self.map_size[2], color="white")
        
        # draw blue and orange goals
        blue_xs, blue_ys, blue_zs, orange_xs, orange_ys, orange_zs = goal_coordinates
        self.ax.plot_surface(blue_xs, blue_ys, blue_zs, color="blue", alpha=0.70)
        self.ax.plot_surface(orange_xs, orange_ys, orange_zs, color="orange", alpha=0.70)

        current_game_state = []
        for idx, player_state in enumerate(all_player_coordinates):

            current_player, team, x, y, z = player_state[0][0], player_state[0][1], player_state[1][i][0], player_state[1][i][1], player_state[1][i][2]

            if team == "ball":
                team = "red"

            # coordinates can be nans if the player joined later or left earlier
            if not (math.isnan(x) or math.isnan(y) or math.isnan(z)):
                self.ax.scatter(x, y, z, c=team)
                

    def animate(self):
        # get coordinates, skip most of the kick-off
        all_player_coordinates = [[player, self._get_coordinates(player[0])[75:]] for player in self.players]

        # create goal coordinates

        # goal-width to map-width ratio is 4.6, goal-height to map-height is 4 (prettified)
        goal_length = self.map_size[0] / 4.6
        blue_xs, blue_zs = np.meshgrid(range(int(self.map_size[0]/2 - goal_length/2), int(self.map_size[0]/2 + goal_length/2)), range(0, int(self.map_size[2] / 4)))
        blue_ys = 0

        orange_xs, orange_zs = np.meshgrid(range(int(self.map_size[0]/2 - goal_length/2), int(self.map_size[0]/2 + goal_length/2)), range(0, int(self.map_size[2] / 4)))
        orange_ys = self.map_size[1]

        goal_coordinates = (blue_xs, blue_ys, blue_zs, orange_xs, orange_ys, orange_zs)

        ani = FuncAnimation(self.fig, self._create_map, fargs=(all_player_coordinates, goal_coordinates), interval=1)
        plt.tight_layout()
        plt.show()
        


