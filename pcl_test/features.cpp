#include "utils.h"
#include <pcl/features/fpfh.h>
#include <pcl/features/normal_3d.h>
#include <iostream>


using namespace pcl;

PointCloud<Normal>::Ptr estimateNormals() {
    // https://pcl.readthedocs.io/projects/tutorials/en/latest/normal_estimation.html#normal-estimation

    PointCloud<PointXYZ>::Ptr cloudGeneratedWolf = readPCDFile("../Wolfhead/generated_wolf.pcd");

    NormalEstimation<PointXYZ, Normal> ne;
    ne.setInputCloud(cloudGeneratedWolf);
    search::KdTree<PointXYZ>::Ptr tree (new search::KdTree<PointXYZ>());
    ne.setSearchMethod(tree);
    ne.setRadiusSearch(0.03); // radius in m

    PointCloud<Normal>::Ptr cloudGeneratedWolfNormals (new PointCloud<Normal>);
    ne.compute(*cloudGeneratedWolfNormals);

    // visualization::PCLVisualizer::Ptr viewer(new visualization::PCLVisualizer ("3D Viewer"));
    // viewer->addPointCloudNormals<PointXYZ, Normal>(cloudGeneratedWolf, cloudGeneratedWolfNormals);
    // while (!viewer->wasStopped()) {
    //     viewer->spinOnce(100);
    // }
    return cloudGeneratedWolfNormals;
}

void estimateFPFHFeatures() {
    // https://github.com/PointCloudLibrary/pcl/blob/master/examples/features/example_fast_point_feature_histograms.cpp

    PointCloud<PointXYZ>::Ptr cloudGeneratedWolf = readPCDFile("../Wolfhead/generated_wolf.pcd");
    PointCloud<Normal>::Ptr cloudGeneratedWolfNormals = estimateNormals();

    FPFHEstimation<PointXYZ, Normal> pfh;
    pfh.setInputCloud(cloudGeneratedWolf);
    pfh.setInputNormals(cloudGeneratedWolfNormals);
    search::KdTree<PointXYZ>::Ptr tree (new search::KdTree<PointXYZ>());
    pfh.setSearchMethod(tree);
    pfh.setRadiusSearch(0.05); // m, larger than radius from estimating normals

    std::cout << "Estimating FPFH features..." << std::endl;

    PointCloud<FPFHSignature33>::Ptr pfhFeatures (new PointCloud<FPFHSignature33> ());
    pfh.compute(*pfhFeatures);

    std::cout << pfhFeatures->size() << std::endl;

    FPFHSignature33 descriptor = (*pfhFeatures)[0];
    std::cout << descriptor << std::endl;
}

int main() {
    // estimateNormals();
    estimateFPFHFeatures();
}