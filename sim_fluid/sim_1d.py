import numpy as np
from utils import get_exp_rand_var

# should check that volume conservation constraints etc. are satisfied
# https://www.youtube.com/watch?v=hswBi5wcqAA

# assume units of meters and seconds


def sim(s, c, delta_t, total_time, init_heights):
    if delta_t * c >= s:
        raise RuntimeError("delta_t * c >= s")

    k = (c**2) / (s**2)
    heights = [np.array(init_heights)]
    velocities = np.zeros(len(init_heights))

    for _ in range(int(total_time / delta_t)):
        arr1 = np.concatenate(([heights[-1][0]], heights[-1][:-1]))
        arr2 = np.concatenate((heights[-1][1:], [heights[-1][-1]]))
        accelerations = k * (arr1 + arr2 - (2 * heights[-1]))
        velocities += delta_t * accelerations
        heights.append(heights[-1] + delta_t * velocities)

    return heights


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth


def init_conds(sim_len, s):
    init_heights = []
    for _ in range(int(sim_len / s)):
        init_heights.append(
            (init_heights[-1] if len(init_heights) != 0 else 0)
            + (get_exp_rand_var(0.0001) * np.random.choice([-1, 1]))
        )
    init_heights = smooth(init_heights, int(sim_len / (s * 10)))
    init_heights += min(init_heights)
    init_heights /= np.sum(init_heights) / len(init_heights)

    return init_heights


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import cv2
    import json

    with open("config.json") as f:
        config = json.load(f)

    x_vals = np.linspace(0, config["sim_len"], int(config["sim_len"] / config["s"]))
    init_heights = init_conds(config["sim_len"], config["s"])
    evolved_heights = sim(
        config["s"], config["c"], config["delta_t"], config["total_time"], init_heights
    )

    min_y, max_y = np.min(evolved_heights), np.max(evolved_heights)

    out = None
    fig = plt.figure()

    for index, heights in enumerate(evolved_heights):
        ax = fig.add_subplot(111)
        ax.plot(x_vals, heights)
        ax.set_ylim(min_y, max_y)
        fig.canvas.draw()

        # Now we can save it to a numpy array.
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        ax.remove()

        if out is None:
            out = cv2.VideoWriter(
                "output.mp4",
                cv2.VideoWriter_fourcc(*"XVID"),
                20.0,
                (data.shape[1], data.shape[0]),
            )

        out.write(data)

        cv2.imshow("img", data)
        if cv2.waitKey(1) == ord("q"):
            break

    out.release()
    cv2.destroyAllWindows()
    plt.close(fig)
