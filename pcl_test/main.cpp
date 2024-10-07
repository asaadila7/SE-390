#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/visualization/cloud_viewer.h>

using namespace pcl;

PointCloud<PointXYZ>::Ptr readPCDFile(const std::string& filename) {
    PointCloud<PointXYZ>::Ptr cloud (new PointCloud<PointXYZ>);
    io::loadPCDFile(filename, *cloud);
    return cloud;
}

void viewPCDFile(const visualization::PCLVisualizer::Ptr& viewer, const std::string& filename) {
    PointCloud<PointXYZ>::Ptr cloud = readPCDFile(filename);
    viewer->setBackgroundColor(255, 255, 255);
    visualization::PointCloudColorHandlerCustom<PointXYZ> single_color (cloud, 0, 0, 0);
    viewer->addPointCloud(cloud, single_color, "cloud" + filename);
}

void listPoints(const PointCloud<PointXYZ>::Ptr& cloud) {
    std::cout << "Loaded "
            << cloud->width * cloud->height
            << " data points with the following fields: "
            << std::endl;
    for (const auto& point: *cloud)
        std::cout << "    " << point.x
                  << " "    << point.y
                  << " "    << point.z << std::endl;
}

int main() {
    visualization::PCLVisualizer::Ptr viewer(new visualization::PCLVisualizer ("3D Viewer"));
    viewer->setBackgroundColor(255, 255, 255);

    viewPCDFile(viewer, "../Wolfhead/generated_wolf.pcd");
    viewPCDFile(viewer, "../Wolfhead/Theoretical_n_noback.pcd");

    while (!viewer->wasStopped()) {
        viewer->spinOnce(100);
    }

}