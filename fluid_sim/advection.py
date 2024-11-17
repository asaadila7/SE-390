import math

def advect_d(q, u, w, i, k, dx, dt):
    x_i = dx * (k + 0.5)
    y_i = dx * (i + 0.5)
    u_i = (u[i][k+1] + u[i][k]) / 2
    w_i = (w[i+1][k] + w[i][k]) / 2
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

    q_p_yj = (1 - a_x) * q[j_y][j_x] + a_x * q[j_y][j1_x]
    q_p_yj1 = (1 - a_x) * q[j1_y][j_x] + a_x * q[j1_y][j1_x]
    q_p = (1 - a_y) * q_p_yj + a_y * q_p_yj1
    return q_p

def advect_u(q, u, w, i, k, dx, dt):
    x_i = dx * k
    y_i = dx * i
    u_i = u[i][k]
    w_i = (w[i + 1][min(k, len(w[0])-1)] + w[i + 1][min(k+1, len(w[0])-1)] + w[i][min(k, len(w[0])-1)] + w[i][min(k+1, len(w[0])-1)]) / 4
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

def advect_w(q, u, w, i, k, dx, dt):
    x_i = dx * k
    y_i = dx * i
    u_i = (u[min(i, len(u)-1)][k+1] + u[min(i, len(u)-1)][k] + u[min(i+1, len(u)-1)][k+1] + u[min(i+1, len(u)-1)][k]) / 4
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