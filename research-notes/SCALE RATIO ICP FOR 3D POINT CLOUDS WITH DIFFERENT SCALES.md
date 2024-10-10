# SCALE RATIO ICP FOR 3D POINT CLOUDS WITH DIFFERENT SCALES
- the second author on this paper is the first author on Scale matching of 3D point clouds by finding keyscales with spin images [1]
- this seems to be a followup or update

## Summary
- issues with keyscales
  - minimum is not stable and may change against small amounts of noise
  - minimum is found at discrete steps (not accurate or efficient)
  - trade off between the two
- find scale ratio directly
  - use mesh resolution for the initial search range
  - PCA on spin images, but this time generate curves for all dimensions
  - scale ratio ICP (variant of ICP) to estimate scale ratio

### Spin Images
- spin images are constructed in the same way as [1]

### Finding the Ratio
1. PCA
    - $c_d^w$ is calculated the same way as [1]
2. Find scale ratio
    - keyscale was determined by the minimum of the cumulative contribute rate curve
    - extend this to use all curves of all dimensions
    - scale difference/ratio is estimated between two sets of curves
      - simplifies the registration problem from matching scales in 3D point clouds to a 1D registration problem
3. Scale ratio ICP
    - want to minimize objective function $E(t)$ where $t$ is the unknown scale ratio (equation in full paper)
    - assume points on a curve have corresponding points on the other curve, but don't know the correspondence
    - ICP:
    1. intialization
        - rough estimate of $t$ is found using mesh-resolutions
    2. find putative correspondences
        - find closest point from one curve to another current the current estimate of $t$
        - performed for different dimensions $d$ independently
    3. estimate $t$
        - obtain an estimate of $t$ from the correspondences
        - take derivative of $E(t)$ with respect to $t$ and set it to 0
    4. iteration
        - repeat steps 2 and 3 until $t$ converges
