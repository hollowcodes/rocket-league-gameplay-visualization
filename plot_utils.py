
import matplotlib.pyplot as plt
import numpy as np

# timeline plot
def timeline_plot(times: list, actions: list, team: list, total_time: float):
    levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(times)/6)))[:len(times)]
                 
    plt.style.use("ggplot")

    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="demolations")

    markerline, _, _ = ax.stem(times, levels, linefmt="C3-", basefmt="k-", use_line_collection=False)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va, c in zip(times, levels, actions, vert, team):
        ax.annotate(r, xy=(d, l), xytext=(3, np.sign(l)*3),
                    textcoords="offset points", va=va, ha="left", color=c)

    plt.setp(ax.get_xticklabels())
    ax.get_yaxis().set_visible(False)

    ax.plot(total_time + 20, 0)
    ax.margins(y=0.1)
    plt.show()