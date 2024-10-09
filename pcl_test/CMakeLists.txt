cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
set(CMAKE_CXX_STANDARD 20)

project(capstone_point_cloud_matching)

find_package(PCL 1.2 REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
add_executable(capstone_point_cloud_matching pcaScaling.cpp
        utils.cpp
        utils.h
)
target_link_libraries (capstone_point_cloud_matching ${PCL_LIBRARIES})


