import numpy as np
import cv2
from utils import get_exp_rand_var


def sim(s, c, delta_t, total_time, init_heights):
    if delta_t * c >= s:
        raise RuntimeError("delta_t * c >= s")

    k = (c**2) / (s**2)
    heights = [np.array(init_heights)]
    velocities = np.zeros(heights[0].shape)

    for _ in range(int(total_time / delta_t)):
        accelerations = np.array(
            [
                [
                    k
                    * (
                        heights[-1][max(0, i - 1)][j]
                        + heights[-1][i][max(0, j - 1)]
                        + heights[-1][min(i + 1, len(heights[-1] - 1))][j]
                        + heights[-1][i][min(j + 1, len(heights[-1][0]) - 1)]
                        - 4 * heights[-1][i][j]
                    )
                    for j in range(heights[0].shape[1])
                ]
                for i in range(heights[0].shape[1])
            ]
        )
        velocities = velocities + delta_t * np.array(accelerations)
        heights.append(heights[-1] + delta_t * velocities)

    return heights


def smooth(y, window_size):
    box = np.ones(window_size) / (window_size[0] * window_size[1])
    y_smooth = cv2.filter2D(np.array(y), -1, box)
    return y_smooth


def init_conds(sim_len, s):
    init_heights = []
    for _ in range(int(sim_len / s)):
        init_heights_row = []
        for _ in range(int(sim_len / s)):
            init_heights_row.append(
                (
                    init_heights_row[-1]
                    if len(init_heights_row) != 0
                    else init_heights[-1][0] if len(init_heights) != 0 else 0.5
                )
                + (get_exp_rand_var(0.0001) * np.random.choice([-1, 1]))
            )
        init_heights.append(init_heights_row)

    init_heights = smooth(
        init_heights, (int(sim_len / (s * 10)), int(sim_len / (s * 10)))
    )
    init_heights += np.min(init_heights)
    init_heights /= np.sum(init_heights) / (int(sim_len / s) ** 2)

    return init_heights
