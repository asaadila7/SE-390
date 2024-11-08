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
        arr1 = np.concatenate(
            (np.expand_dims(heights[-1][0, :], 0), heights[-1][:-1, :]), axis=0
        )
        arr2 = np.concatenate(
            (heights[-1][1:, :], np.expand_dims(heights[-1][-1, :], 0)), axis=0
        )
        arr3 = np.concatenate(
            (np.expand_dims(heights[-1][:, 0], 1), heights[-1][:, :-1]), axis=1
        )
        arr4 = np.concatenate(
            (heights[-1][:, 1:], np.expand_dims(heights[-1][:, -1], 1)), axis=1
        )
        accelerations = k * (arr1 + arr2 + arr3 + arr4 - (4 * heights[-1]))
        velocities += delta_t * accelerations
        heights.append(heights[-1] + delta_t * velocities)

    return heights


def smooth(y, window_size):
    box = np.ones(window_size) / (window_size[0] * window_size[1])
    return cv2.filter2D(np.array(y), -1, box)


def init_conds(sim_len, s):
    init_heights = []
    for _ in range(int(sim_len / s)):
        init_heights_row = []
        for _ in range(int(sim_len / s)):
            init_heights_row.append(
                (
                    (init_heights[-1][len(init_heights_row) - 1] + init_heights_row[-1])
                    / 2
                    if len(init_heights) != 0 and len(init_heights_row) != 0
                    else (
                        init_heights_row[-1]
                        if len(init_heights_row) != 0
                        else init_heights[-1][0] if len(init_heights) != 0 else sim_len
                    )
                )
                + (get_exp_rand_var(1 / s) * np.random.choice([-1, 1]))
            )
        init_heights.append(init_heights_row)

    init_heights[0][0] = init_heights[0][-1] = init_heights[-1][0] = init_heights[-1][
        -1
    ] = sim_len
    window_side_len = int(sim_len / (s * 5))
    init_heights = smooth(init_heights, (window_side_len, window_side_len))
    init_heights -= np.min(init_heights)
    init_heights *= sim_len**3 / (np.sum(init_heights) * (s**2))

    return init_heights


if __name__ == "__main__":
    import os
    import math
    import json
    import matplotlib.pyplot as plt
    from gen_stl import create_mesh

    with open("config.json") as f:
        config = json.load(f)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshes")
    if os.path.exists(out_dir):
        print("ERROR: Folder exists:", out_dir)
        exit(1)

    os.mkdir(out_dir)

    x_vals, y_vals = np.mgrid[
        0 : config["sim_len"] : config["s"], 0 : config["sim_len"] : config["s"]
    ]
    init_heights = init_conds(config["sim_len"], config["s"])
    print("calculated init heights")

    # plot init heights using matplotlib
    ax = plt.figure().add_subplot(projection="3d")
    ax.plot_surface(x_vals, y_vals, init_heights)
    plt.show()

    evolved_heights = sim(
        config["s"], config["c"], config["delta_t"], config["total_time"], init_heights
    )
    print("evolved heights")

    for idx, heights in enumerate(evolved_heights):
        if idx % config["time_downsample_factor"] != 0:
            continue
        create_mesh(
            heights[
                :: config["space_downsample_factor"],
                :: config["space_downsample_factor"],
            ],
            x_vals[
                :: config["space_downsample_factor"],
                :: config["space_downsample_factor"],
            ],
            y_vals[
                :: config["space_downsample_factor"],
                :: config["space_downsample_factor"],
            ],
            os.path.join(
                out_dir,
                str(idx).zfill(math.ceil(math.log10(len(evolved_heights)))) + ".stl",
            ),
            scale_factor=config["mesh_scale_factor"],
        )
