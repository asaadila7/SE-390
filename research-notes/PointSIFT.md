# PointSIFT

[PointSIFT: A SIFT-like Network Module for 3D Point Cloud Semantic Segmentation](https://arxiv.org/pdf/1807.00652)

- the english in this paper makes it quite difficult to understand, and some parts make almost no sense
  - e.g. "however, using ordered operator could be much more informative while still preserves the invariance to order of input points"

## Summary

### Introduction
- 3D semantic segmentation challenges:
  - sparseness of point cloud in 3D space makes spatial operators inefficient
  - relationship between points is implicit and difficult to represent
- PointSIFT is inspired by SIFT (Scale-invariant feature transform)
  - two key properties:
    - scale-awareness
    - orientation-encoding
  - SIFT algorithm uses handcrafted features, PointSIFT is a parameteric deep learning module
- basic building block is an orientation-encoding unit which convolves the features of nearest points in 8 orientations
  - to make it scale-aware, OE units are connected by shortcuts and optimized for adapted scales
- PointSIFT module receives point cloud with $n$ features each point and outputs points of $n$ features with better representation power
- results: PointSIFT outperforms methods on S3DIS (12%) and ScanNet (8.4%)

### Related Work
- 3D representation
  - volumetric
  - polygonal
  - multiview
- deep learning
  - PointNet
  - rotation equivariance and invariance
- SIFT
- these may or may not be useful to further look into

### Problem Statement
- point cloud $P$, a set point containing $n$ points $p_1, p_2,\dots, p_n\in \R^d$ where $d$ is the dimensional feature
- feature vector of each point $p_i$ is it coordinate in 3D space ($x_i, y_i, z_i$)
- $L$, the set of semantic labels
- $\Psi$, function representing the semantic segmentation of a point
  - i.e. $\Psi: P \longmapsto L$

### Method
- encode-decode (downsample-upsample) framework
- downsampling stage:
  - recursively apply PointSIFT combined with set abstraction for hierachical feature embedding
- upsampling stage:
  - dense features enabled by interleaving feature propagation with PointSIFT
#### PointSIFT Module
- given an $n\times d$ matrix as input (point set of size $n$ with $d$ dimension feature)
- PointSIFT module outputs a $n\times d$ matrix that assigns a new $d$ dimension feaure to every point
#### Orientation-Encoding
- use ordered operation, order by coordinates
- input of the OE unit is a $d$-dimension feature vector $f_0\in \R^d$ of point $p_0$
- followed by a lot of math we can look into later if we need
- OE convolution outputs a $d$ dimension feature
- tl;dr: "orientation-encoding convolution integrates information from eight spatial orientations and obtains a representation that encodes orientation information"
#### Scale-Awareness
- use multi-scale representation by stacking several OE units in the PointSIFT module
- features of various scales are concatenated and transformed to output a $d$ dimensional multi-scale feature
#### Architecture
- not sure how important this part is

### Experiments
#### Orientation-Encoding Convolution
- apply stacked 8-neighbourhood search in OE unit
  - different from ball query search in PointNet++, which searches for global nearest neighbours
  - global nearest neighbour can be less informative
- S8N grouping + OE convolution is much more effective
- more points from individual input point clouds contribute to the final representation for PointSIFT compared to PointNet++
#### Scale-Awareness
- generate 10000 simple shapes with different scales
- train framework on generated data
- test if activation magnitude of PointSIFT module in different layers of a shape match the scale of the shape
- 89% of the time, the position of the PointSIFT module with the highest activation in the hierarchy is aligned with the relative scale of the input shape
- means PointSIFT is aware of scale somewhat

## TL;DR
- PointSIFT is based on SIFT, but uses a machine-learning/neural networks approach
  - Probably not worth it to go with this approach if we don't have the data
- Looks for the nearest points in 8 orientations rather than just the nearest neighbours
- Can at least somewhat deal with differences in scale, but they don't seem very confident
  - They only used a toy experiment with simple shapes, so this is likely something that can be improved
- Could maybe be effective for CAD models but would need to be trained on CAD models
