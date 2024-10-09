#include <pcl/common/pca.h>
#include "utils.h"
#include <pcl/common/common.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

using namespace pcl;

int main() {
    PointCloud<PointXYZ>::Ptr cloudGeneratedWolf = readPCDFile("../Wolfhead/generated_wolf.pcd");
    PCA<PointXYZ> pcaGeneratedWolf;
    pcaGeneratedWolf.setInputCloud(cloudGeneratedWolf);

    PointCloud<PointXYZ>::Ptr cloudTheoreticalN = readPCDFile("../Wolfhead/Theoretical_n_noback.pcd");
    PCA<PointXYZ> pcaTheoreticalN;
    pcaTheoreticalN.setInputCloud(cloudTheoreticalN);

    // PCA using ordered eigenvalues
    Eigen::Vector3f generatedWolfEigenvalues = pcaGeneratedWolf.getEigenValues();
    std::sort(generatedWolfEigenvalues.begin(), generatedWolfEigenvalues.end());

    Eigen::Vector3f theoreticalNEigenvalues = pcaTheoreticalN.getEigenValues();
    std::sort(theoreticalNEigenvalues.begin(), theoreticalNEigenvalues.end());

    // 0.0394889, 0.0814504, 0.143187 - scale factors are all drastically different
    double scaleFactors[3];
    for (int i = 0; i < 3; i++) {
        scaleFactors[i] = generatedWolfEigenvalues[i] / theoreticalNEigenvalues[i];
        std::cout << scaleFactors[i] << std::endl;
    }

    // PCA using binding box
    // source https://stackoverflow.com/questions/59395218/pcl-scale-two-point-clouds-to-the-same-size
    Eigen::Matrix3f generatedWolfEigenvectors = pcaGeneratedWolf.getEigenVectors();
    Eigen::Vector4f generatedWolfMidPoint = pcaGeneratedWolf.getMean();
    Eigen::Matrix4f generatedWolfTransform = Eigen::Matrix4f::Identity();
    generatedWolfTransform.block<3, 3>(0, 0) = generatedWolfEigenvectors;
    generatedWolfTransform.block<4, 1>(0, 3) = generatedWolfMidPoint;
    PointCloud<PointXYZ>::Ptr orientedGeneratedWolf(new PointCloud<PointXYZ>);
    transformPointCloud(*cloudGeneratedWolf, *orientedGeneratedWolf, generatedWolfTransform.inverse());
    PointXYZ generatedWolfMin, generatedWolfMax;
    getMinMax3D(*orientedGeneratedWolf, generatedWolfMin, generatedWolfMax);

    Eigen::Matrix3f theoreticalNEigenvectors = pcaTheoreticalN.getEigenVectors();
    Eigen::Vector4f theoreticalNMidPoint = pcaTheoreticalN.getMean();
    Eigen::Matrix4f theoreticalNTransform = Eigen::Matrix4f::Identity();
    theoreticalNTransform.block<3, 3>(0, 0) = theoreticalNEigenvectors;
    theoreticalNTransform.block<4, 1>(0, 3) = theoreticalNMidPoint;
    PointCloud<PointXYZ>::Ptr orientedTheoreticalN(new PointCloud<PointXYZ>);
    transformPointCloud(*cloudTheoreticalN, *orientedTheoreticalN, theoreticalNTransform.inverse());
    PointXYZ theoreticalNMin, theoreticalNMax;
    getMinMax3D(*orientedTheoreticalN, theoreticalNMin, theoreticalNMax);

    double xScale =  (generatedWolfMax.x - generatedWolfMin.x) / (theoreticalNMax.x - theoreticalNMin.x);
    double yScale =  (generatedWolfMax.y - generatedWolfMin.y) / (theoreticalNMax.y - theoreticalNMin.y);
    double zScale =  (generatedWolfMax.z - generatedWolfMin.z) / (theoreticalNMax.z - theoreticalNMin.z);

    cout << "xScale = " << xScale << endl; // 0.45845
    cout << "yScale = " << yScale << endl; // 0.443423
    cout << "zScale = " << zScale << endl; // 0.353402

    for (int i = 0; i < orientedTheoreticalN->points.size(); i++)
    {
        orientedTheoreticalN->points[i].x = orientedTheoreticalN->points[i].x * xScale;
        orientedTheoreticalN->points[i].y = orientedTheoreticalN->points[i].y * yScale;
        orientedTheoreticalN->points[i].z = orientedTheoreticalN->points[i].z * zScale;
    }

    // pcl::transformPointCloud(*orientedSample, *cloudTheoreticalN, sampleTransform);
    visualization::PCLVisualizer::Ptr boundingBoxViewer(new visualization::PCLVisualizer ("3D Viewer"));
    boundingBoxViewer->setBackgroundColor(255, 255, 255);
    viewPointCloud(boundingBoxViewer, cloudGeneratedWolf, "wolf", 4, 44, 99); // blue
    viewPointCloud(boundingBoxViewer, cloudTheoreticalN, "theoretical_n", 4, 44, 99); // blue
    viewPointCloud(boundingBoxViewer, orientedTheoreticalN, "scaled + oriented theoretical_n",23, 99, 4 ); // green
    // viewPointCloud(boundingBoxViewer, orientedGeneratedWolf, "oriented theoretical_n", 99, 4, 4); // red
    while (!boundingBoxViewer->wasStopped()) {
        boundingBoxViewer->spinOnce(100);
    }
}