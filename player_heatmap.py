
import matplotlib.pyplot as plt
import numpy as np
import math


class PlayerHeatmap:
    def __init__(self, dataframe, player: str="", map_size: tuple=(8192, 10240)):
        self.dataframe = dataframe
        self.player = player
        self.map_size = map_size

    # translate coordinates (create cartesian coordinate system, positive values only)
    def _translate_coordinates(self, coords: tuple):
        x = int(np.floor((-1 * coords[0]) + (self.map_size[0] / 2)))
        y = int(np.floor(coords[1] + (self.map_size[1] / 2)))
        return (x, y)

    # get player coordinates of every frame
    def _get_coordinates(self):
        x = self.dataframe[(self.player + ".1")].tolist()
        x.remove("pos_x")

        y = self.dataframe[(self.player + ".2")].tolist()
        y.remove("pos_y")

        x = [float(x_) for x_ in x]
        y = [float(y_) for y_ in y]

        coordinates = list(zip(x, y))
        for i in range(len(coordinates)):
            try:
                coords = self._translate_coordinates(coordinates[i])
            except:
                pass
            finally:
                coordinates[i] = coords

        return coordinates

    # create heatmap
    def create_map(self, down_scale: int=100):
        coordinates = self._get_coordinates()
        scaled_map_size = (int(self.map_size[0] / down_scale), int(self.map_size[1] / down_scale))
        map_ = np.zeros(scaled_map_size)

        for coordinate in coordinates:
            x, y = int((coordinate[0] / down_scale)) - 1, int((coordinate[1] / down_scale)) - 1
            map_[x][y] += 1

        plt.matshow(map_)
        plt.title(self.player)
        plt.show()

