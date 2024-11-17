import math

# calculate average velocity at d_i,k
def avg_velocity_d(u, w, i, k):
    u_i = (u[i][k + 1] + u[i][k]) / 2
    w_i = (w[i + 1][k] + w[i][k]) / 2
    return u_i, w_i

# calculate average velocity at u_i,k
def avg_velocity_u(u, w, i, k):
    u_i = u[i][k]
    w_i = (w[i + 1][min(k, len(w[0]) - 1)] + w[i + 1][min(k + 1, len(w[0]) - 1)]
           + w[i][min(k, len(w[0]) - 1)] + w[i][min(k + 1, len(w[0]) - 1)]) / 4
    return u_i, w_i

# calculate average velocity at w_i,k
def avg_velocity_w(u, w, i, k):
    u_i = (u[min(i, len(u) - 1)][k + 1] + u[min(i, len(u) - 1)][k] + u[min(i + 1, len(u) - 1)][k + 1] +
           u[min(i + 1, len(u) - 1)][k]) / 4
    w_i = w[i][k]
    return u_i, w_i

def advect(q, u, w, i, k, dx, dt, trans_x, trans_y, get_average_velocity):
    x_i = dx * (k + trans_x)
    y_i = dx * (i + trans_y)

    u_i, w_i = get_average_velocity(u, w, i, k)
    x_p = x_i - dt * u_i
    y_p = y_i - dt * w_i

    j_x = math.floor(x_p / dx - trans_x)
    x_j = dx * (j_x + trans_x)
    j1_x = math.ceil(x_p / dx - trans_x)
    a_x = (x_p - x_j) / dx

    j_y = math.floor(y_p / dx - trans_y)
    y_j = dx * (j_y + trans_y)
    j1_y = math.ceil(y_p / dx - trans_y)
    a_y = (y_p - y_j) / dx

    j_y = max(0, min(len(q) - 1, j_y))
    j1_y = max(0, min(len(q) - 1, j1_y))
    j_x = max(0, min(len(q[0]) - 1, j_x))
    j1_x = max(0, min(len(q[0]) - 1, j1_x))

    q_p_yj = (1 - a_x) * q[j_y][j_x] + a_x * q[j_y][j1_x]
    q_p_yj1 = (1 - a_x) * q[j1_y][j_x] + a_x * q[j1_y][j1_x]
    q_p = (1 - a_y) * q_p_yj + a_y * q_p_yj1
    return q_p
