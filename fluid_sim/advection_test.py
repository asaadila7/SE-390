import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import advection

dx = 0.1
length = 5
dimension = int(length / dx)

dt = 0.001
T = 1

def init_conds():
    heights = np.empty((dimension, dimension))

    # horizontal
    # for i in range(dimension):
    #     for j in range(dimension):
    #         heights[i][j] = 5 if j < dimension // 2 else 0
    #
    # u = np.full((dimension, dimension + 1), 5)
    # w = np.full((dimension + 1, dimension), 0)

    # diagonal
    for i in range(dimension):
        for j in range(dimension):
            heights[i][j] = 5 if j < i else 0

    u = np.full((dimension, dimension + 1), 10)
    w = np.full((dimension + 1, dimension), 10)

    return u, w, heights

def evolve_step(prev_d, u, w):
    u_A = np.empty_like(u)
    w_A = np.empty_like(w)
    for i in range(dimension):
        for k in range(dimension+1):
            u_A[i][k] = advection.advect(u, u, w, i, k, dx, dt, 0, 0, advection.avg_velocity_u)

    for i in range(dimension+1):
        for k in range(dimension):
            w_A[i][k] = advection.advect(w, u, w, i, k, dx, dt, 0, 0, advection.avg_velocity_w)

    d_A = np.empty_like(prev_d)
    for i in range(dimension):
        for k in range(dimension):
            d_A[i][k] = advection.advect(prev_d, u, w, i, k, dx, dt, 0.5, 0.5, advection.avg_velocity_d)

    return u_A, w_A, d_A

def sim():
    u, w, heights = init_conds()
    heights = [heights]
    for t in range(int(T / dt)):
        u, w, new_d = evolve_step(heights[-1], u, w)
        heights = np.vstack((heights, [new_d]))
    return heights

sim_heights = sim()
x, y = np.meshgrid(np.arange(0, length, dx), np.arange(0, length, dx))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
min_height = sim_heights.min() * 0.9
# min_height = 0
max_height = sim_heights.max() * 1.1
ax.set_zlim(min_height, max_height)

def animate(i):
    ax.clear()
    ax.set_zlim(min_height, max_height)
    ax.plot_surface(x, y, sim_heights[i], cmap=cm.coolwarm)

plot_animation = animation.FuncAnimation(fig, animate, frames=int(T / dt), interval=20)

plt.show()