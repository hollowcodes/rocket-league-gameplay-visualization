
import os
import json
from gameplay_stats import get_stats

# get analized replay in json format
def save_replay_json(replay_file: str):
    os.system("carball -i " + replay_file + " --json " + replay_file.split(".")[0] + ".json")

# load json content
def load_json(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)

# get players name by id
def get_player_by_id(analysis: dict, id_: int) -> str:
    stats = get_stats(analysis)
    return stats[id_].get("name"), stats[id_].get("team")

# calculate the time through the frames
def get_time_by_frames(total_frames: int, total_time: float, frames: int) -> float:
    return total_time / (total_frames / frames)