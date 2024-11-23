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
T = 0.5

def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth

def init_height():
    init_heights = []
    for _ in range(int(length / dx)):
        init_heights_row = []
        for _ in range(int(length / dx)):
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
        init_heights_row = smooth(init_heights_row, int(length / (dx * 10)))
        init_heights.append(init_heights_row)

    init_heights += np.min(init_heights) + 1
    init_heights /= np.sum(init_heights) / (int(length / dx) ** 2)

    return init_heights

def init_sin_height():
    d = np.empty((dimension, dimension), dtype=np.float64)
    for i in range(len(d)):
        for j in range(len(d[i])):
            d[i][j] = np.sin(dx * (i + 0.5) / 0.1) + 1.5
    return d

def init_conds():
    u = np.zeros((dimension + 1, dimension), dtype=np.float64)
    v = np.zeros((dimension, dimension + 1), dtype=np.float64)
    return u, v, init_height()

def evolve_u(i, j, u_A, d_A):
    if i == 0 or i > dimension - 1:
        return 0 # solid wall BC

    return u_A[i][j] - dt * g * (d_A[i][j] - d_A[i-1][j]) / dx

def evolve_v(i, j, v_A, d_A):
    if j == 0 or j > dimension - 1:
        return 0 # solid wall BC

    return v_A[i][j] - dt * g * (d_A[i][j] - d_A[i][j-1]) / dx

def evolve_d(i, j, u, v, d_A):
    return d_A[i][j] - dt * d_A[i][j] * (u[i+1][j] - u[i][j] + v[i][j+1] - v[i][j]) / dx

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

    for i in range(len(u)):
        for j in range(len(u[i])):
            u[i][j] = evolve_u(i, j, u_A, d_A)

    for i in range(len(v)):
        for j in range(len(v[i])):
            v[i][j] = evolve_v(i, j, v_A, d_A)

    new_d = np.empty_like(prev_d)
    for i in range(len(new_d)):
        for j in range(len(new_d[i])):
            new_d[i][j] = evolve_d(i, j, u, v, d_A)
    return new_d

def sim():
    u, v, d = init_conds()
    d = [d]
    for t in range(int(T / dt)):
        new_d = evolve_step(d[-1], u, v)
        d = np.vstack((d, [new_d]))
    return d

sim_heights = sim()
x, y = np.meshgrid(np.arange(0, length, dx), np.arange(0, length, dx))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
min_height = 0
max_height = sim_heights.max() * 1.1
ax.set_zlim(min_height, max_height)

def animate(i):
    ax.clear()
    ax.set_zlim(min_height, max_height)
    ax.plot_surface(x, y, sim_heights[i], cmap=cm.coolwarm)
    ax.set_title(f'total volume: {round(np.sum(sim_heights[i]), 2)}')

plot_animation = animation.FuncAnimation(fig, animate, frames=int(T / dt), interval=20)

plt.show()
