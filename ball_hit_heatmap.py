
import matplotlib.pyplot as plt
import numpy as np
from utils import get_player_by_id, get_time_by_frames


class BallHitHeatmap:
    def __init__(self, analysis: dict, map_size: tuple=(8192, 10240)):
        self.analysis = analysis
        self.map_size = map_size
        self.hits = analysis["gameStats"].get("hits")
        self.total_frames = analysis["gameMetadata"]["frames"]
        self.total_time = analysis["gameMetadata"]["length"]

    # translate coordinates (create cartesian coordinate system, positive values only)
    def _translate_coordinates(self, coords: dict) -> dict:
        coords["posX"] = int(np.floor((-1 * coords["posX"]) + (self.map_size[0] / 2)))
        coords["posY"] = int(np.floor(coords["posY"] + (self.map_size[1] / 2)))

        return coords

    # get hit information (time, player, coordinates)
    def _get_hit_coordinates(self) -> list:
        hit_info = []
        for hit in self.hits:
            time = round(get_time_by_frames(self.total_frames, self.total_time, hit.get("frameNumber")), 4)
            player = get_player_by_id(self.analysis, hit.get("playerId").get("id"))
            ball_coordinates = hit.get("ballData")

            hit_info.append([time, player, self._translate_coordinates(ball_coordinates)])

        return hit_info

    # create heatmap
    def create_map(self, down_scale: int=100):
        hit_coordinates = self._get_hit_coordinates()
        scaled_map_size = (int(self.map_size[0] / down_scale), int(self.map_size[1] / down_scale))
        map_ = np.zeros(scaled_map_size)

        for hit in hit_coordinates:
            x, y = int(hit[2]["posX"] / down_scale) - 1, int(hit[2]["posY"] / down_scale) - 1
            map_[x][y] += 1

        plt.matshow(map_)
        plt.show()
























