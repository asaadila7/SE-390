import bpy
import json
import os

script_dir = "change/this/to/yout/script/dir"

with open(os.path.join(script_dir, "cam_transform.json"), "w") as f:
    json.dump(
        [[elem for elem in row] for row in bpy.data.objects["Camera"].matrix_world],
        f,
        indent=4,
    )
