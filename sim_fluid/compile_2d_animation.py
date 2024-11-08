import cv2
import os

out = None
render_dir = "animation_2d"

for file in sorted(os.listdir(render_dir)):
    frame = cv2.imread(os.path.join(render_dir, file))

    if out is None:
        out = cv2.VideoWriter(
            "output.mp4",
            cv2.VideoWriter_fourcc(*"XVID"),
            20.0,
            (frame.shape[1], frame.shape[0]),
        )

    out.write(frame)

    cv2.imshow("img", cv2.resize(frame, (640, 480)))
    if cv2.waitKey(1) == ord("q"):
        break

out.release()
