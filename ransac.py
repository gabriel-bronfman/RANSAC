import open3d as o3d
import numpy as np
import random

pcd_point_cloud = o3d.data.PCDPointCloud()
pcd = o3d.io.read_point_cloud(pcd_point_cloud.path)

points = np.asarray(pcd.points)
num_points = len(points)


# Basic outline:
# Big ol' while loop that does adaptive sampling
# Pick 3 points in the point cloud
# Parameterize a plane, saving normal n
# Check distance between points with respect to some defined distance max
#    take n, cross with b, take abs and then divide by magnitude of n, return value
# Determine inliers, recalculate epsilon
# check if current check count is greater than n for given epsilon
# Increment epsilon

sample_count = 0
current_inliers = []
best_hypothesis_inliers = []
best_inliers = 0

# Estimating with three points, hypothesizing 25% outliers
epsilon = .25  
p = .8
N = 9

while (N > sample_count):
    inliers = 0
    selected_points = [random.randrange(0,num_points),random.randrange(0,num_points),random.randrange(0,num_points)]

    n = np.cross(points[selected_points[2]]-points[selected_points[0]],points[selected_points[1]]-points[selected_points[0]])

    for point in points:
        
        if np.abs(np.dot(n,(point-points[selected_points[0]])))/np.linalg.norm(n) < .022518:
            inliers += 1
            current_inliers.append(point)
    
    if best_inliers < inliers:
        best_inliers = inliers
        best_hypothesis_inliers = current_inliers
    
    current_inliers = []
    
    if inliers > 1:
        epsilon = 1.00 - (inliers)/num_points
        print(epsilon)

    N = np.log(1.00-p)/np.log(1.00-(1.00-epsilon)**3)
    sample_count += 1


inlier_pcd = o3d.geometry.PointCloud()

inlier_pcd.points = o3d.utility.Vector3dVector(np.array(best_hypothesis_inliers))
inlier_pcd.colors = o3d.utility.Vector3dVector([[255,0,0]]*len(best_hypothesis_inliers))



o3d.visualization.draw_geometries([pcd,inlier_pcd],
                                    zoom=1,
                                    front=[0.4257, -0.2125, -0.8795],
                                    lookat=[2.6172, 2.0475, 1.532],
                                    up=[-0.0694, -0.9768, 0.2024])

