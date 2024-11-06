import open3d as o3d

mesh = o3d.io.read_triangle_mesh("hello.stl")
mesh.compute_triangle_normals()
o3d.visualization.draw_geometries([mesh])
