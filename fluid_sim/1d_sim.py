import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

s = 0.001  # col width
width = 1 # total width of simulated fluid

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
        init_heights.append(
            (init_heights[-1] if len(init_heights) != 0 else 0)
            + (np.random.exponential(0.0001) * np.random.choice([-1, 1]))
        )
    init_heights = smooth(init_heights, int(sim_len / (s * 10)))
    init_heights += min(init_heights)
    init_heights /= np.sum(init_heights) / len(init_heights)

    return init_heights

def sim_col_step(heights, velocities, i): # index of point we are simulating
    h_cur = heights[i]
    h_left = heights[i-1] if i > 0 else h_cur # boundary conditions
    h_right = heights[i+1] if i < len(heights) - 1 else h_cur # boundary conditions
    a_i = k * (h_left + h_right - 2 * h_cur)
    v = velocities[i] + dt * a_i
    h = heights[i] + dt * v
    return v, h

def sim_step(heights, velocities):
    sim_heights = []
    sim_velocities = []
    for i in range(len(heights[-1])):
        v, h = sim_col_step(heights[-1], velocities[-1], i)
        sim_heights.append(h)
        sim_velocities.append(v)
    return np.vstack((heights, sim_heights)), np.vstack((velocities, sim_velocities))


def sim(heights):
    heights = [heights]
    velocities = np.array(np.zeros_like(heights))
    for _ in range(int(total_time / dt)):
        heights, velocities = sim_step(heights, velocities)
    return heights

init_heights = init_conds(width, s)
sim_heights = sim(init_heights)
fig, ax = plt.subplots()
x = np.arange(0, width, s)
line, = ax.plot(x, init_heights)

def animate(i):
    line.set_ydata(sim_heights[i])
    return line


plot_animation = animation.FuncAnimation(fig, animate, frames=int(total_time / dt), interval=20)
plt.show()
