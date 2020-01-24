
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math


class Heatmap:
    def __init__(self, dataframe, player: str="", map_size: tuple=(8192, 10240), down_scale: int=100):
        self.dataframe = dataframe
        self.player = player
        self.map_size = map_size

    # translate coordinates (create cartesian coordinate system, positive values only) and rescale them
    def _translate_coordinates(self, coords: tuple, down_scale: int=100):
        x = int(np.floor((-1 * coords[0]) + (self.map_size[0] / 2)))
        y = int(np.floor(coords[1] + (self.map_size[1] / 2)))

        # rescaling
        x, y = int((x / down_scale)), int((y / down_scale))

        return (x, y)

    # get player coordinates of every frame
    def _get_coordinates(self, down_scale: int=100):
        pos_x_index = ".1" if self.player != "ball" else ""
        pos_y_index = ".2" if self.player != "ball" else ".1"

        x = self.dataframe[(self.player + pos_x_index)].tolist()
        x.remove("pos_x")

        y = self.dataframe[(self.player + pos_y_index)].tolist()
        y.remove("pos_y")

        x = [float(x_) for x_ in x]
        y = [float(y_) for y_ in y]

        coordinates = list(zip(x, y))
        for i in range(len(coordinates)):
            try:
                coords = self._translate_coordinates(coordinates[i], down_scale=down_scale)
            except:
                pass
            finally:
                coordinates[i] = coords

        return coordinates

    # create heatmap
    def create_heatmap(self, down_scale: int=100):
        coordinates = self._get_coordinates(down_scale=down_scale)
        scaled_map_size = (int(self.map_size[0] / down_scale) + 1, int(self.map_size[1] / down_scale) + 1)
        map_ = np.zeros(scaled_map_size)

        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            map_[x][y] += 1

        plt.matshow(map_)
        plt.title(self.player)
        plt.show()

    # create one frame of the tracemap
    def _create_tracemap(self, i, ax, coordinates, down_scale):
        coordinate = coordinates[i]
        x, y = coordinate[0], coordinate[1]

        scaled_map_size = (int(self.map_size[0] / down_scale) + 1, int(self.map_size[1] / down_scale) + 1)
        map_ = np.zeros(scaled_map_size)
        map_[x][y] += 10

        ax.clear()
        ax.matshow(map_)

    # show an animated map that shows the trace of a player/ball
    def animate_tracemap(self, down_scale: int=100):
        # get coordinates, skip the kick-off, skip every 'self.down_scale' frame
        coordinates = self._get_coordinates(down_scale=down_scale)[100:]
        del coordinates[(down_scale - 1)::down_scale]

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ani = FuncAnimation(fig, self._create_tracemap, frames=range(0, len(coordinates) - 1), fargs=(ax, coordinates, down_scale), interval=10)
        plt.tight_layout()
        plt.show()
    





