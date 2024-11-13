import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import math

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

    # height = np.zeros((dimension, dimension)) # todo: change this
    # for x in range(dimension):
    #     for y in range(dimension):
    #         height[x][y] =  abs(-x**2 + y**2) / 10
    # height = init_height(length, dx)
    return u, w

def evolve_u(i, k, prev_u, prev_height):
    # print(prev_u[i][k])
    if k == 0 or k >= dimension - 1:
        return 0 # boundary condition: solid wall
    h_left = prev_height[i][k-1]
    h_right = prev_height[i][k]
    u = prev_u[i][k] - dt * g * (h_right - h_left) / dx
    return u

def evolve_w(i, k, prev_w, prev_height):
    if i == 0 or i >= dimension - 1:
        return 0 # boundary condition: solid wall
    h_top = prev_height[i-1][k]
    h_bottom = prev_height[i][k]
    w = prev_w[i][k] - dt * g * (h_bottom - h_top) / dx
    return w

def evolve_d(i, k, prev_d, u, w):
    # print(prev_d[i][k])
    return prev_d[i][k] - dt * prev_d[i][k] * ((u[i][k+1] - u[i][k]) / dx + (w[i+1][k] - w[i][k]) / dx)

def advect(q, u, w, i, j):
    # j_p = j - u[min(99, i)][j] / dx * dt
    # i_p = i - w[i][min(99, j)] / dx * dt
    # left = max(0, min(len(q[0])-1, math.floor(j_p)))
    # right = max(0, min(len(q[0])-1, math.ceil(j_p)))
    # top = max(0, min(len(q)-1, math.floor(i_p)))
    # bottom = max(0, min(len(q)-1, math.ceil(i_p)))
    # return 0.5 * q[bottom][left] + 0.5 * q[top][right]
    return q[i][j]

def advect_d(q, u, w, i, k):
    x_i = dx * (k + 0.5)
    y_i = dx * (i + 0.5)
    u_i = (u[i][k+1] - u[i][k]) / dx
    w_i = (w[i+1][k] - w[i][k]) / dx
    x_p = x_i - dt * u_i
    y_p = y_i - dt * w_i

    j_x = math.floor(x_p / dx - 0.5)
    x_j = dx * (j_x + 0.5)
    j1_x = math.ceil(x_p / dx - 0.5)
    a_x = (x_p - x_j) / dx

    j_y = math.floor(y_p / dx - 0.5)
    y_j = dx * (j_y + 0.5)
    j1_y = math.ceil(y_p / dx - 0.5)
    a_y = (y_p - y_j) / dx

    j_y = max(0, min(len(q) - 1, j_y))
    j1_y = max(0, min(len(q) - 1, j1_y))
    j_x = max(0, min(len(q[0]) - 1, j_x))
    j1_x = max(0, min(len(q[0]) - 1, j1_x))

    # print(a_x, a_y)
    q_p_yj = (1 - a_x) * q[j_y][j_x] + a_x * q[j_y][j1_x]
    q_p_yj1 = (1 - a_x) * q[j1_y][j_x] + a_x * q[j1_y][j1_x]
    q_p = (1 - a_y) * q_p_yj + a_y * q_p_yj1
    return q_p

def advect_u(q, u, w, i, k):
    x_i = dx * k
    y_i = dx * i
    u_i = u[i][k]
    w_i = (w[i + 1][min(k, len(w[0])-1)] - w[i][min(k, len(w[0])-1)]) / dx
    x_p = x_i - dt * u_i
    y_p = y_i - dt * w_i

    j_x = math.floor(x_p / dx)
    x_j = dx * j_x
    j1_x = math.ceil(x_p / dx)
    a_x = (x_p - x_j) / dx

    j_y = math.floor(y_p / dx)
    y_j = dx * j_y
    j1_y = math.ceil(y_p / dx)
    a_y = (y_p - y_j) / dx

    j_y = max(0, min(len(q) - 1, j_y))
    j1_y = max(0, min(len(q) - 1, j1_y))
    j_x = max(0, min(len(q[0]) - 1, j_x))
    j1_x = max(0, min(len(q[0]) - 1, j1_x))

    q_p_yj = (1 - a_x) * q[j_y][j_x] + a_x * q[j_y][j1_x]
    q_p_yj1 = (1 - a_x) * q[j1_y][j_x] + a_x * q[j1_y][j1_x]
    q_p = (1 - a_y) * q_p_yj + a_y * q_p_yj1

    return q_p

def advect_w(q, u, w, i, k):
    x_i = dx * k
    y_i = dx * i
    u_i = (u[min(i, len(u)-1)][k+1] - u[min(i, len(u)-1)][k]) / dx
    w_i = w[i][k]
    x_p = x_i - dt * u_i
    y_p = y_i - dt * w_i

    j_x = math.floor(x_p / dx)
    x_j = dx * j_x
    j1_x = math.ceil(x_p / dx)
    a_x = (x_p - x_j) / dx

    j_y = math.floor(y_p / dx)
    y_j = dx * j_y
    j1_y = math.ceil(y_p / dx)
    a_y = (y_p - y_j) / dx

    j_y = max(0, min(len(q) - 1, j_y))
    j1_y = max(0, min(len(q) - 1, j1_y))
    j_x = max(0, min(len(q[0]) - 1, j_x))
    j1_x = max(0, min(len(q[0]) - 1, j1_x))

    q_p_yj = (1 - a_x) * q[j_y][j_x] + a_x * q[j_y][j1_x]
    q_p_yj1 = (1 - a_x) * q[j1_y][j_x] + a_x * q[j1_y][j1_x]
    q_p = (1 - a_y) * q_p_yj + a_y * q_p_yj1
    return q_p


def evolve_step(prev_d, u, w):
    # velocity_field_u = np.copy(u)
    # velocity_field_w = np.reshape(w, np.shape(u))
    # print(np.shape(velocity_field_w))
    # u_A = calc.advection(u, velocity_field_u, velocity_field_w, dx=dx * units('m'), dy=dx * units('m'))

    u_A = np.empty_like(u)
    w_A = np.empty_like(w)
    for i in range(dimension):
        for k in range(dimension+1):
            u_A[i][k] = advect_u(u, u, w, i, k)

    for i in range(dimension+1):
        for k in range(dimension):
            w_A[i][k] = advect_w(w, u, w, i, k)

    for i in range(dimension):
        for k in range(dimension+1):
            u[i][k] = evolve_u(i, k, u_A, prev_d)
    # print(u)
    for i in range(dimension+1):
        for k in range(dimension):
            w[i][k] = evolve_w(i, k, w_A, prev_d)

    d_A = np.empty_like(prev_d)
    for i in range(dimension):
        for k in range(dimension):
            d_A[i][k] = advect_d(prev_d, u, w, i, k)
    # print(d_A)

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
# print(sim_heights[0])

x, y = np.meshgrid(np.arange(0, length, dx), np.arange(0, length, dx))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
min_height = sim_heights.min() * 0.9
# min_height = 0
max_height = sim_heights.max() * 1.1
ax.set_zlim(min_height, max_height)

# x = x.ravel()
# y = y.ravel()
# bottom = np.full_like(x + y, min_height)
# ax.bar3d(x, y, bottom, dx, dx, init_heights.ravel(), shade=True)

def animate(i):
    ax.clear()
    ax.set_zlim(min_height, max_height)
    ax.plot_surface(x, y, sim_heights[i], cmap=cm.coolwarm)
    # ax.bar3d(x, y, bottom, dx, dx, sim_heights[i].ravel(), shade=True)

plot_animation = animation.FuncAnimation(fig, animate, frames=int(T / dt), interval=10)

plt.show()
