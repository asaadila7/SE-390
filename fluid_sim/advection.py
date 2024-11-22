import math

# calculate average velocity at d_i,k
def avg_velocity_d(u, w, i, k):
    u_i = (u[i][k + 1] + u[i][k]) / 2
    w_i = (w[i + 1][k] + w[i][k]) / 2
    return u_i, w_i

# calculate average velocity at u_i,k
def avg_velocity_u(u, w, i, k):
    u_i = u[i][k]
    w_i = (w[i][max(0, k-1)] + w[i+1][max(0, k-1)] + w[i][min(k, len(w[0]) - 1)] + w[i+1][min(k, len(w[0]) - 1)]) / 4

    # w_i = (w[i + 1][min(k, len(w[0]) - 1)] + w[i + 1][min(k + 1, len(w[0]) - 1)]
    #        + w[i][min(k, len(w[0]) - 1)] + w[i][min(k + 1, len(w[0]) - 1)]) / 4
    return u_i, w_i

# calculate average velocity at w_i,k
def avg_velocity_w(u, w, i, k):
    # u_i = (u[min(i, len(u) - 1)][k + 1] + u[min(i, len(u) - 1)][k] + u[min(i + 1, len(u) - 1)][k + 1] +
    #        u[min(i + 1, len(u) - 1)][k]) / 4

    u_i = (u[max(0, i-1)][k] + u[max(0, i-1)][k+1] + u[min(i, len(u) - 1)][k] + u[min(i, len(u) - 1)][k+1]) / 4
    w_i = w[i][k]
    return u_i, w_i

def linear_interpolate(s, q_0, q_1):
    return (1-s) * q_0 + s * q_1

def linear_advect(q, j_x, j1_x, a_x, j_y, j1_y, a_y):
    j_y = max(0, min(len(q) - 1, j_y))
    j1_y = max(0, min(len(q) - 1, j1_y))
    j_x = max(0, min(len(q[0]) - 1, j_x))
    j1_x = max(0, min(len(q[0]) - 1, j1_x))

    q_p_yj = linear_interpolate(a_x, q[j_y][j_x], q[j_y][j1_x])
    q_p_yj1 = linear_interpolate(a_x, q[j1_y][j_x], q[j1_y][j1_x])
    q_p = linear_interpolate(a_y, q_p_yj, q_p_yj1)

    return q_p

def cubic_interpolate(s, q_neg_1, q_0, q_1, q_2):
    w_neg_1 = -1/3 * s + 1/2 * s**2 - 1/6 * s**3
    w_0 = 1 - s**2 + 1/2 * (s**3 - s)
    w_1 = s + 1/2 * (s**2 - s**3)
    w_2 = 1/6 * (s**3 - s)
    return w_neg_1 * q_neg_1 + w_0 * q_0 + w_1 * q_1 + w_2 * q_2

def cubic_advect(q, j_x, j1_x, a_x, j_y, j1_y, a_y):
    j_y = max(0, min(len(q) - 1, j_y))
    j1_y = max(0, min(len(q) - 1, j1_y))
    j2_y = max(0, min(len(q) - 1, j1_y+1))
    j_neg1_y = max(0, min(len(q) - 1, j_y-1))

    j_x = max(0, min(len(q[0]) - 1, j_x))
    j1_x = max(0, min(len(q[0]) - 1, j1_x))
    j2_x = max(0, min(len(q[0]) - 1, j1_x + 1))
    j_neg1_x = max(0, min(len(q[0]) - 1, j_x - 1))

    q_p_yj_neg1 = cubic_interpolate(a_x, q[j_neg1_y][j_neg1_x], q[j_neg1_y][j_x], q[j_neg1_y][j1_x], q[j_neg1_y][j2_x])
    q_p_yj = cubic_interpolate(a_x, q[j_y][j_neg1_x], q[j_y][j_x], q[j_y][j1_x], q[j_y][j2_x])
    q_p_yj1 = cubic_interpolate(a_x, q[j1_y][j_neg1_x], q[j1_y][j_x], q[j1_y][j1_x], q[j1_y][j2_x])
    q_p_yj2 = cubic_interpolate(a_x, q[j2_y][j_neg1_x], q[j2_y][j_x], q[j2_y][j1_x], q[j2_y][j2_x])
    q_p = cubic_interpolate(a_y, q_p_yj_neg1, q_p_yj, q_p_yj1, q_p_yj2)

    return q_p

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

    # return linear_advect(q, j_x, j1_x, a_x, j_y, j1_y, a_y)
    return cubic_advect(q, j_x, j1_x, a_x, j_y, j1_y, a_y)