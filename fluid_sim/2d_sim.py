import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm

s = 0.01  # col width
width = 1 # total width of simulated fluid
height = 1

c = 0.05  # wave speed

k = (c**2) / (s**2)

dt = 0.01  # time step
total_time = 10  # s

def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth

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
                        else init_heights[-1][0] if len(init_heights) != 0 else 0.5
                    )
                )
                + (np.random.exponential(0.0001) * np.random.choice([-1, 1]))
            )
        init_heights_row = smooth(init_heights_row, int(sim_len / (s * 10)))
        init_heights.append(init_heights_row)

    init_heights += np.min(init_heights)
    init_heights /= np.sum(init_heights) / (int(sim_len / s) ** 2)

    return init_heights

def sim_col_step(heights, velocities, i, j): # index of point we are simulating
    h_cur = heights[i][j]
    h_top = heights[i-1][j] if i > 0 else h_cur # boundary conditions
    h_left = heights[i][j-1] if j > 0 else h_cur # boundary conditions
    h_bottom = heights[i+1][j] if i < len(heights) - 1 else h_cur # boundary conditions
    h_right = heights[i][j+1] if j < len(heights[i]) - 1 else h_cur # boundary conditions
    a_i = k * (h_left + h_right + h_top + h_bottom - 4 * h_cur)
    v = velocities[i][j] + dt * a_i
    h = heights[i][j] + dt * v
    return v, h

def sim_step(heights, velocities):
    sim_heights = []
    sim_velocities = []
    for i in range(len(heights[-1])):
        sim_heights_row = []
        sim_velocities_row = []
        for j in range(len(heights[-1][i])):
            v, h = sim_col_step(heights[-1], velocities[-1], i, j)
            sim_heights_row.append(h)
            sim_velocities_row.append(v)
        sim_heights.append(sim_heights_row)
        sim_velocities.append(sim_velocities_row)
    return np.vstack((heights, [sim_heights])), np.vstack((velocities, [sim_velocities]))


def sim(heights):
    heights = [heights]
    velocities = np.array(np.zeros_like(heights))
    for _ in range(int(total_time / dt)):
        heights, velocities = sim_step(heights, velocities)
    return heights

init_heights = init_conds(width, s)
sim_heights = sim(init_heights)
x, y = np.meshgrid(np.arange(0, width, s), np.arange(0, height, s))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, init_heights, cmap=cm.coolwarm)
ax.set_zlim(-1, 5)


def animate(i):
    ax.clear()
    ax.set_zlim(-1, 5)
    ax.plot_surface(x, y, sim_heights[i], cmap=cm.coolwarm)

plot_animation = animation.FuncAnimation(fig, animate, frames=int(total_time / dt), interval=20)
plt.show()

