# Real-Time Scale Invariant 3D Range Point CloudRegistration

Link: [Real-Time Scale Invariant 3D Range Point CloudRegistration](https://www.researchgate.net/publication/221472830_Real-Time_Scale_Invariant_3D_Range_Point_Cloud_Registration)

## Summary

### Intro:
* 3D point cloud data is obtained via sensors, stereo cameras
* Rare to have a single representation of all required data, so need to register multiple frames of point clouds with respect to each other
    * Construct composite map/scene for use 
* Full automation of registration for range image 3D point clouds is active research topic:
    * Systems rely on user input
    * Algorithms highly processor intensive - makes real-time registration difficult
* Additional challenges with point clouds:
    * Point cloud may be too sparse
    * Noise can cause false artifacts
        * Ie. IR ranger point cloud data is highly noisy due to ambient light and surface properties
    * Erroneous data (ie. Noise) may create matchable artifacts
        * Leads to highly deformed registered point clouds
        * Algorithm must be able to account for noise

### Approach:
Locate robust features (feature descriptors) that are invariant to scale, rotation, and perspective
  * Use robust features to locate correspondences between point clouds with high certainty
  * Use point correspondences algorithm to register these point clouds
  * To reduce effect of noise, important that the feature descriptors  are:
      * Very robust
      * Invariant to scale and rotation

Use Scale Invariant Feature Transform (SIFT) to find robust features
  * Features are highly robust (to changes in illumination and minor changes in POV), orientation invariant, applicable in multiple scale
  * Generates large number of localized features at low computational cost
  * Only works on 2D data sets - must perform preprocessing to use on 3D point cloud
  
#### SIFT algorithm:
* Detect possible points of interest:
    1) Convolve input data with successive Gaussian filters at different scales
    2) Take Difference of Gaussians (DoG): difference of successive Gaussian blurred images
    3) Use local extremum points in the DoG's at multiple scales as key points
        * These approximate the Laplacian
    4) Determine if key points are local minimum or maximum by analyzing them within their neighbourhoods and adjacent scales
* Discard key points in noisy spaces:
    1) Eliminate candidates that are in low contrast regions or on an edge
* Rotation invariance - assign each key point 1+ orientations
    1) Assign orientation and gradient magnitude to the each DoG that a key point came from
    2) Perform magnitude and direction calculations for each key point and every pixel in its neighbourhood
    3) Use these calculations to generate an orientation histogram with 36 bins (each covering 10 degrees)
    4) Assign the orientations with peaks within the highest 80% to the key point (the histogram is generated for each key point)
* Compute descriptor vector used to identify and match each key point
    1)  Compute orientation histogram and 4x4 neighbourhood around each key point
        * Histogram is relative to the key point's orientation and orientation data based on key point's scale
    2)  Histogram contains 8 bins
    3)  Use bins to derive a SIFT feature vector with 128 elements
  
Registration:
* Currently, use Iterative Closest Point (ICP)
    * Requires pre-computed correspondences between point clouds 
        * Correspondences must be:
            * Quickly calculated
            * Accurate when translating, rotating, scaling
        * So use SIFT to find correspondences
  
### Overall algorithm:
1)  Data preprocessing
    * Makes point cloud data suitable for SIFT feature detection
        * SIFT feature detector requires continuous points in neighbourhood of pixels
    * Square root scale Euclidean distance from each point to the origin to get information to fit between 0-255
    * Pass scaled data through PNG converter to obtain image with SIFT operator applied
2)  SIFT feature detection and matching
    * Implement SIFT feature detector using Open CV based on SIFT algorithm
    * SIFT algorithm: take in PNG image and outputs the SIFT feature vector (as described above)
    * Search for matching SIFT descriptors using RANSAC algorithm:
        * Select feature pairs at random and compute their transformation
        * Determine all the set of feature pairs that match this transformation
        * Reject this feature pair if set size if below threshold
    * Derive correspondences in point cloud from the RANSAC algorithm matches
        □ Map back from the square-root scaled data to a key point in the point cloud
3)  Point cloud registration
    * Use known points correspondence registration algorithm based on quaternions:
        * Each point is represented by quaternions c=0 and its x, y, z coordinates
        * Find quaternion of rotation matrix as the eigenvector corresponding to the max positive eigenvalue of N:
        * Obtain rotation matrix from rotation quaternion
        * Use rotation matrix to determine translation quaternion and scale factor
    * Matrix calculations done via GSL library with some extensions

 ### Extensions:
  * Extended work to derive roll, pitch, yaw between consecutive frames
      * Done by selecting appropriate row/column pairs from rotation matrix

### Testing/Results:
  * Used data obtained from Swiss IR Ranger - 290 frames
  * RANSAC was able to find > 1 correspondence in adjacent fames
  * Can locate an object in a point cloud by registering a reference template point cloud of an object with a target point cloud using the described approach
      * Was able to detect a stack of cardboard boxes using a template of part of a cardboard box
      * Was able to withstand rotating the template data
  * Tested ability to derive roll, pitch, yaw:
      * Compared by those measured by onboard sensors on robot
      * Was a close match, especially in graph shape, but not exact
      * Deviation due to frames having multiple correspondences
          * Reduced error by applying Kalman filter on SIFT matching results
  * Runtime performance:
      * Was able to achieve frame rate of 6.36 fps

### Limitations:
  * When using data from Swiss IR ranger, the quick movement caused images to be blurry which reduced the number of features to be able to match
      * Found that the approach needed at least 3 correspondences 
      * There is usually a high number of correspondences even in noisy / blurred data
  * There was some error when some frames had multiple possible correspondences
      * Was able to reduce error by applying Kalman filter on SIFT matching results
      * Could likely further improve by applying more filtering
  * Could likely improve performance by adding optimization methods

## Takeaways:
  * Could build on existing things by:
      * Increasing accuracy - applying filters / additional pre-processing
      * Improve performance - apply optimization
      * Increasing application - find additional values that can be calculated from data that is relevant for our use-case
  * Mapping onto CAD model:
      * This paper suggests that object detection is possible by taking some template point cloud and using their approach for registration
          * Template seems to have been obtained by placing the target object in front of the Swiss IR Ranger and obtaining a point cloud of that
      * This paper maps from a template point cloud to a different point cloud:
          * If using their method, problem would be to convert from CAD model to point cloud
  * This paper used a cardboard box which is a relatively uniform object with little variation - only variation that was applied to template was rotating it
      * Could look into performing object detection when there is more variance between template and real-life objects
      * Did not appear to test results while scaling template object (ie. Detecting larger/smaller boxes than template)
