
from utils import save_replay_json, load_json
from gameplay_stats import get_stats, plot_stats, plot_possession
from heatmap import Heatmap
from time_line import Timeline


def main(replay: str):
    """ load the carball game analysis json file """
    analysis = load_json(replay)

    """ plot the game play stats """
    game_stats = get_stats(analysis)
    plot_stats(game_stats)
    
    """ plot the game play history """
    timeline = Timeline(analysis)
    timeline.plot(show=["goals", "demos"])

    """ plot possession """
    plot_possession(analysis)

    """ ball-hit heatmap """
    heatmap = Heatmap(analysis)
    heatmap.create_map(down_scale=700)


if __name__ == "__main__":
    # save_replay_json("dataset/replays/replay_3/5297D2F811EA2F2AB12780A8F576FE2C.replay")
    
    main("dataset/replays/replay_5/383CE56A11EA2BC4CDAD1994A3FECA7F.json")


