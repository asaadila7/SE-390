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
