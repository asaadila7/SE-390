import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

import advection

dx = 0.1
length = 5
dimension = int(length / dx)

g = 9.81 # gravity

dt = 0.001
T = 1

def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth

def init_height(sim_len, s):
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
                        else init_heights[-1][0] if len(init_heights) != 0 else 0.5
                    )
                )
                + (np.random.exponential(0.005) * np.random.choice([-1, 1]))
            )
        init_heights_row = smooth(init_heights_row, int(sim_len / (s * 10)))
        init_heights.append(init_heights_row)

    init_heights += np.min(init_heights) + 1
    init_heights /= np.sum(init_heights) / (int(sim_len / s) ** 2)

    return init_heights

def init_conds():
    u = np.zeros((dimension, dimension+1))
    w = np.zeros((dimension+1, dimension))

    return u, w

def evolve_u(i, k, prev_u, prev_height):
    if k == 0 or k >= dimension - 1:
        return 0 # boundary condition: solid wall
    h_left = prev_height[i][k-1]
    h_right = prev_height[i][k]
    # mirroring boundary condition
    # h_left = prev_height[i][max(0, k - 1)]
    # h_right = prev_height[i][min(dimension - 1, k)]
    u = prev_u[i][k] - dt * g * (h_right - h_left) / dx
    return u

def evolve_w(i, k, prev_w, prev_height):
    if i == 0 or i >= dimension - 1:
        return 0 # boundary condition: solid wall
    h_top = prev_height[i-1][k]
    h_bottom = prev_height[i][k]
    # mirroring boundary condition
    # h_top = prev_height[max(0, i - 1)][k]
    # h_bottom = prev_height[min(dimension - 1, i)][k]
    w = prev_w[i][k] - dt * g * (h_bottom - h_top) / dx
    return w

def evolve_d(i, k, prev_d, u, w):
    # print(prev_d[i][k])
    return prev_d[i][k] - dt * prev_d[i][k] * ((u[i][k+1] - u[i][k]) / dx + (w[i+1][k] - w[i][k]) / dx)

def evolve_step(prev_d, u, w):
    u_A = np.empty_like(u)
    w_A = np.empty_like(w)
    d_A = np.empty_like(prev_d)
    for i in range(dimension):
        for k in range(dimension+1):
            u_A[i][k] = advection.advect(u, u, w, i, k, dx, dt, 0, 0, advection.avg_velocity_u)

    for i in range(dimension+1):
        for k in range(dimension):
            w_A[i][k] = advection.advect(w, u, w, i, k, dx, dt, 0, 0, advection.avg_velocity_w)

    for i in range(dimension):
        for k in range(dimension):
            d_A[i][k] = advection.advect(prev_d, u, w, i, k, dx, dt, 0.5, 0.5, advection.avg_velocity_d)

    for i in range(dimension):
        for k in range(dimension+1):
            u[i][k] = evolve_u(i, k, u_A, prev_d)

    for i in range(dimension+1):
        for k in range(dimension):
            w[i][k] = evolve_w(i, k, w_A, prev_d)

    new_d = np.empty_like(prev_d)
    for i in range(dimension):
        for k in range(dimension):
            new_d[i][k] = evolve_d(i, k, d_A, u, w)
    return new_d

def sim(init_heights):
    u, w = init_conds()
    heights = [init_heights]
    for t in range(int(T / dt)):
        new_d = evolve_step(heights[-1], u, w)
        heights = np.vstack((heights, [new_d]))
    return heights

init_heights = init_height(length, dx)
sim_heights = sim(init_heights)

x, y = np.meshgrid(np.arange(0, length, dx), np.arange(0, length, dx))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
min_height = sim_heights.min() * 0.9
max_height = sim_heights.max() * 1.1
ax.set_zlim(min_height, max_height)

def animate(i):
    ax.clear()
    ax.set_zlim(min_height, max_height)
    ax.plot_surface(x, y, sim_heights[i], cmap=cm.coolwarm)
    ax.set_title(f'total volume: {round(np.sum(sim_heights[i]), 2)}')

plot_animation = animation.FuncAnimation(fig, animate, frames=int(T / dt), interval=10)

plt.show()
