import open3d as o3d

source = o3d.io.read_point_cloud('wolfhead/generated_wolf.pcd')
target = o3d.io.read_point_cloud('wolfhead/scaled_theoretical_n.pcd')

# o3d.visualization.draw_geometries([source, target])


def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


voxel_size = 0.05  # means 5cm for this dataset

source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)


distance_threshold = voxel_size * 1.5
result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
    source_down, target_down, source_fpfh, target_fpfh, True,
    distance_threshold,
    o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
    3, [
        o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
            0.9),
        o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
            distance_threshold)
    ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))


print (result)
print(result.transformation)

def draw_registration_result(source, target, transformation):
    source.paint_uniform_color([1, 0.706, 0])
    target.paint_uniform_color([0, 0.651, 0.929])
    source.transform(transformation)
    o3d.visualization.draw_geometries([source, target])

# draw_registration_result(source_down, target_down, result.transformation)
source.transform(result.transformation)