# Scale matching of 3D point clouds by finding keyscales with spin images

## Summary
- a reason that there are few papers on scale invariance of point clouds is because for most applications of point clouds, scales are absolute and thus known
- another reason is that 2D scale invariant features (e.g. SIFT) are not directly applicable to 3D point clouds
### Spin Images
- a spin image is a local feature of a 3D point with an associated normal vector
- they can be constructed from a point cloud (more details and math are in the full paper)
- they're not scale-invariant, so can't be used for matching unless the scales are aligned
  - this is because you give the image width/size of neighbourhood during construction
### Keyscale
- definition: "the scale that gives the minimum of the cumulative contribution rates of the PCA of spin images over different scales"
- approach: find an appropriate image width $w$ (i.e. scale) for a given 3D point cloud
  - if $w$ is too small, local geometry doesn't get represented (everything is flat if you look at a small enough spot)
  - if $w$ is too large, spin images look very similar to each other as well
- there is a minimum similarity between spin images as $w$ changes, and this scale is the keyscale
#### Steps
1. PCA
    - PCA is performed on a set of spin images
    - Obtain the cumulative contibution rate $c_d^w$ at dimension $d$ (math in full paper)
2. Find keyscale
    - Find the minimum of $c_d^w$ by varying $w$
    - $c_d^w$ tends to 1 when $w\to 0$ or $w\to\infty$, and has a minimum between
    - keyscale is defined as $\argmin_{0<w}c_d^w$ 
