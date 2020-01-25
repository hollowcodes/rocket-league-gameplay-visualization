
from utils import save_replay_json, load_json, save_replay_dataframe, load_dataframe
from gameplay_stats import get_stats, plot_stats, plot_possession
from ball_hit_heatmap import BallHitHeatmap
from player_heatmap import PositionHeatmap
from time_line import Timeline
import carball
import requests
import pandas as pd


def main(json_replay: str="", data_frame_replay: str=""):
    """ load the carball game analysis json file and data frame """
    analysis = load_json(json_replay)
    data_frame = load_dataframe(data_frame_replay)

    """ plot the game play stats """
    game_stats = get_stats(analysis)
    plot_stats(game_stats)
    
    """ plot the game play history """
    timeline = Timeline(analysis)
    timeline.plot(show=["goals", "demos"])

    """ plot possession """
    plot_possession(analysis)

    """ ball-hit heatmap """
    heatmap = BallHitHeatmap(analysis)
    heatmap.create_map(down_scale=700)

    """ player/ball-coordinate heatmap and live tracemap (player="ball" possible) """
    playerHeatmap = PositionHeatmap(data_frame, analysis)
    playerHeatmap.create_heatmap(down_scale=500)
    playerHeatmap.animate_tracemap(down_scale=200)



if __name__ == "__main__":
    # save_replay_json("dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.replay", "dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.json")
    # save_replay_dataframe("dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.replay", "dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.csv")
    
    main(json_replay="dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.json",
         data_frame_replay="dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.csv")


