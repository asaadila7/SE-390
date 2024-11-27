import math

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

# given index, grid spacing, and translation, figure out position on grid
def get_pos(i, dx, trans):
    return (i + trans) * dx

# given point x in grid with spacing dx, find x_j such that x_j <= x <= x_{j-1} and the proportion a that x is between x_j and x_{j-1}
def find_nearest_smaller(x, dx, trans, dimension):
    k = x / dx - trans # hypothetical grid index that x is at
    j = clamp(math.floor(k), 0, dimension)
    a = clamp(k - j, 0, 1)
    return j, a

def avg_velocity_d(u, v, i, j):
    u_avg = (u[i][j] + u[i+1][j]) / 2
    v_avg = (v[i][j] + v[i][j+1]) / 2
    return u_avg, v_avg

def avg_velocity_u(u, v, i, j):
    u_avg = u[i][j]
    i_neg_1 = clamp(i-1, 0, len(v)-1)
    i = clamp(i, 0, len(v)-1)
    v_avg = (v[i_neg_1][j] + v[i_neg_1][j+1] + v[i][j] + v[i][j+1])
    return u_avg, v_avg

def avg_velocity_v(u, v, i, j):
    v_avg = v[i][j]
    j_neg_1 = clamp(j-1, 0, len(u[0])-1)
    j = clamp(j, 0, len(u[0])-1)
    u_avg = (u[i][j_neg_1] + u[i+1][j_neg_1] + u[i][j] + u[i+1][j])
    return u_avg, v_avg

def linear_interpolate(s, q_0, q_1):
    if s == 0: return q_0
    if s == 1: return q_1
    return (1-s) * q_0 + s * q_1

def linear_advect(q, n_x, n_y, a_x, a_y):
    n_x_1 = clamp(n_x + 1, 0, len(q)-1)
    n_y_1 = clamp(n_y + 1, 0, len(q[0])-1)

    q_n_y = linear_interpolate(a_x, q[n_x][n_y], q[n_x_1][n_y])
    q_n_y_1 = linear_interpolate(a_x, q[n_x][n_y_1], q[n_x_1][n_y_1])
    return linear_interpolate(a_y, q_n_y, q_n_y_1)

def cubic_interpolate(s, q_neg_1, q_0, q_1, q_2):
    if s == 0: return q_0
    if s == 1: return q_1
    w_neg_1 = -1/3 * s + 1/2 * s**2 - 1/6 * s**3
    w_0 = 1 - s**2 + 1/2 * (s**3 - s)
    w_1 = s + 1/2 * (s**2 - s**3)
    w_2 = 1/6 * (s**3 - s)
    return w_neg_1 * q_neg_1 + w_0 * q_0 + w_1 * q_1 + w_2 * q_2

def cubic_advect(q, n_x, n_y, a_x, a_y):
    n_x_neg_1 = clamp(n_x + 1, 0, len(q) - 1)
    n_x_1 = clamp(n_x + 1, 0, len(q) - 1)
    n_x_2 = clamp(n_x + 2, 0, len(q) - 1)

    n_y_neg_1 = clamp(n_y - 1, 0, len(q[0]) - 1)
    n_y_1 = clamp(n_y + 1, 0, len(q[0]) - 1)
    n_y_2 = clamp(n_y + 2, 0, len(q[0]) - 1)

    q_n_y_neg_1 = cubic_interpolate(a_x, q[n_x_neg_1][n_y_neg_1], q[n_x][n_y_neg_1], q[n_x_1][n_y_neg_1], q[n_x_2][n_y_neg_1])
    q_n_y = cubic_interpolate(a_x, q[n_x_neg_1][n_y], q[n_x][n_y], q[n_x_1][n_y],q[n_x_2][n_y])
    q_n_y_1 = cubic_interpolate(a_x, q[n_x_neg_1][n_y_1], q[n_x][n_y_1], q[n_x_1][n_y_1], q[n_x_2][n_y_1])
    q_n_y_2 = cubic_interpolate(a_x, q[n_x_neg_1][n_y_2], q[n_x][n_y_2], q[n_x_1][n_y_2], q[n_x_2][n_y_2])
    return cubic_interpolate(a_y, q_n_y_neg_1, q_n_y, q_n_y_1, q_n_y_2)

def advect(q, u, v, i, j, dx, dt, trans_x, trans_y, max_x, max_y, avg_velocity):
    x_cur = get_pos(i, dx, trans_x)
    y_cur = get_pos(j, dx, trans_y)

    u_avg, v_avg = avg_velocity(u, v, i, j)

    x_prev = x_cur - dt * u_avg
    y_prev = y_cur - dt * v_avg

    n_x, a_x = find_nearest_smaller(x_prev, dx, trans_x, max_x)
    n_y, a_y = find_nearest_smaller(y_prev, dx, trans_y, max_y)

    # return linear_advect(q, n_x, n_y, a_x, a_y)
    return cubic_advect(q, n_x, n_y, a_x, a_y)