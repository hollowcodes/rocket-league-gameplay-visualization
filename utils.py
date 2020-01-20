
import os
import json
from gameplay_stats import get_stats
import carball
import pandas as pd


# get analyzed replay in json format
def save_replay_json(replay_file: str, save_file: str):
    os.system("carball -i " + replay_file + " --json " + save_file)

# load json content
def load_json(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)

# save replay data frame
def save_replay_dataframe(replay_file: str, save_file: str):
    data_frame = carball.analyze_replay_file(replay_file).data_frame
    data_frame.to_csv(save_file)

# load data frame
def load_dataframe(file: str):
    return pd.read_csv(file, low_memory=False)

# get players name and team by id
def get_player_by_id(analysis: dict, id_: int) -> str:
    stats = get_stats(analysis)
    return stats[id_].get("name"), stats[id_].get("team")

# calculate the time through the frames
def get_time_by_frames(total_frames: int, total_time: float, frames: int) -> float:
    return total_time / (total_frames / frames)