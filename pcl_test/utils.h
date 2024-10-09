#include <pcl/point_cloud.h>
#include <pcl/visualization/pcl_visualizer.h>
using namespace pcl;

PointCloud<PointXYZ>::Ptr readPCDFile(const std::string& filename);

void viewPCDFile(const visualization::PCLVisualizer::Ptr& viewer, const std::string& filename);

void viewPointCloud(const visualization::PCLVisualizer::Ptr& viewer, const PointCloud<PointXYZ>::Ptr& cloud, const std::string& id, int r = 0, int g = 0, int b = 0);

void listPoints(const PointCloud<PointXYZ>::Ptr& cloud);