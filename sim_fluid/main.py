import numpy as np
import matplotlib.pyplot as plt
import cv2

s = 0.001  # m
sim_len = 1

c = 0.05  # in m/s?

delta_t = 0.01  # s
total_time = 5  # s

# 1d sim:

# import sim_1d

# x_vals = np.linspace(0, sim_len, int(sim_len / s))
# init_heights = sim_1d.init_conds(sim_len, s)
# evolved_heights = sim_1d.sim(s, c, delta_t, total_time, init_heights)

# min_y, max_y = np.min(evolved_heights), np.max(evolved_heights)

# out = None
# fig = plt.figure()

# for index, heights in enumerate(evolved_heights):
#     ax = fig.add_subplot(111)
#     ax.plot(x_vals, heights)
#     ax.set_ylim(min_y, max_y)
#     fig.canvas.draw()

#     # Now we can save it to a numpy array.
#     data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
#     data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

#     ax.remove()

#     if out is None:
#         out = cv2.VideoWriter(
#             "output.mp4",
#             cv2.VideoWriter_fourcc(*"XVID"),
#             20.0,
#             (data.shape[1], data.shape[0]),
#         )

#     out.write(data)

#     cv2.imshow("img", data)
#     if cv2.waitKey(1) == ord("q"):
#         break

# out.release()
# cv2.destroyAllWindows()
# plt.close(fig)

# 2d sim

import sim_2d
from gen_stl import gen

x_vals, y_vals = np.mgrid[0:sim_len:s, 0:sim_len:s]
init_heights = sim_2d.init_conds(sim_len, s)
print("calculated init heights")
print("min val:", np.min(init_heights))

down_sample_factor = 10
gen(
    init_heights[::down_sample_factor, ::down_sample_factor],
    x_vals[::down_sample_factor, ::down_sample_factor],
    y_vals[::down_sample_factor, ::down_sample_factor],
    "hello.stl",
)
exit(1)

# plot init heights using matplotlib
# ax = plt.figure().add_subplot(projection="3d")
# ax.plot_surface(x_vals, y_vals, init_heights)
# plt.show()

evolved_heights = sim_2d.sim(s, c, delta_t, total_time, init_heights)
print("evolved heights")
