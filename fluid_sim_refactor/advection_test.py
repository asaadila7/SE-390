import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import advection

dx = 0.1
length = 5
dimension = int(length / dx)

dt = 0.001
T = 0.5

def init_conds():
    d = np.empty((dimension, dimension), dtype=np.float64)

    # horizontal
    # for i in range(dimension):
    #     for j in range(dimension):
    #         d[i][j] = 5. if j < dimension // 2 else 0

    # diagonal
    # for i in range(dimension):
    #     for j in range(dimension):
    #         d[i][j] = 5. if j < dimension - i else 0

    # spike
    for i in range(dimension):
        for j in range(dimension):
            d[i][j] = max(0, -abs(j - dimension / 2.) + dimension / 2. - 20)

    u = np.full((dimension + 1, dimension), 10.)
    v = np.full((dimension, dimension + 1), 10.)

    return u, v, d

def evolve_step(prev_d, u, v):
    u_A = np.empty_like(u)
    v_A = np.empty_like(v)
    d_A = np.empty_like(prev_d)

    for i in range(len(u_A)):
        for j in range(len(u_A[i])):
            u_A[i][j] = advection.advect(u, u, v, i, j, dx, dt, 0, 0.5, dimension, advection.avg_velocity_u)

    for i in range(len(v_A)):
        for j in range(len(v_A[i])):
            v_A[i][j] = advection.advect(v, u, v, i, j, dx, dt, 0.5, 0, dimension, advection.avg_velocity_v)

    for i in range(len(d_A)):
        for j in range(len(d_A[i])):
            d_A[i][j] = advection.advect(prev_d, u, v, i, j, dx, dt, 0.5, 0.5, dimension, advection.avg_velocity_d)
    return u_A, v_A, d_A

def sim():
    u, v, d = init_conds()
    d = [d]
    for t in range(int(T / dt)):
        u, v, new_d = evolve_step(d[-1], u, v)
        d = np.vstack((d, [new_d]))
    return d

sim_heights = sim()
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

plot_animation = animation.FuncAnimation(fig, animate, frames=int(T / dt), interval=20)

plt.show()
