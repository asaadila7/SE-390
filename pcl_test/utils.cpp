#include "utils.h"
#include <pcl/io/pcd_io.h>

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

void viewPointCloud(const visualization::PCLVisualizer::Ptr& viewer, const PointCloud<PointXYZ>::Ptr& cloud, const std::string& id, int r, int g, int b) {
    visualization::PointCloudColorHandlerCustom<PointXYZ> single_color (cloud,r, g, b);
    viewer->addPointCloud(cloud, single_color, id);
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
