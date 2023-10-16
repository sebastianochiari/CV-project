import pickle
from utils import loadPKLfile

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

CAMERA = 14

K = loadPKLfile('./calibration-matrices/cameraMatrix-14.pkl')

world_points = 0.01 * np.array (
    [
        [50., 100., 50., 100.], # X
        [0., 0., 0., 0.], # Y
        [50., 50., 100., 100.]  # Z
    ]
)

image_points = np.array(
    [
        [852, 809, 700, 645],
        [904, 1005, 889, 985]
    ]
)

# Example image (since we have a greyscale image, reduce dimensionality down to 2)
img = mpimg.imread('./images/camera-14.png')[:,:,0]
plt.imshow(img, cmap='gray')
plt.scatter(x=image_points[0], y=image_points[1], c='b', s=25)

plt.show()

def DLTPoseEstimation(image_points, world_points, K):
    """
    Estimate the pose of the camera from the given 2D-3D correspondences 
    and the given camera intrinsics.
    :param np.ndarray[float, float] image_points:      vector of undistorted image coordinates
    :param np.ndarray[float, float] world_points:    vector of world coordinates
    :param np.ndarray[float, float] K:               camera matrix, intrinsics
    :return: projection matrix M [R|t] with R (Rotation matrix) t (translation)
    :rtype: np.array(...)
    """
    # convert 2D points to 3D points by adding 1 to the third dimension
    image_3d = np.concatenate((image_points, np.ones((1,len(image_points[0])))), axis=0)
    
    # normalize the coordinates by applying the camera intrinsics
    image_points_normalized = np.linalg.solve(K, image_3d)
                               
    # create Q matrix to fill, initialize with zeros
    Q = np.zeros((2*len(image_points_normalized[0]), 12))
        
    # fill the Q-amtrix according to its definition
    for i in range(len(image_points_normalized[0])):
        u = image_points_normalized[0,i]
        v = image_points_normalized[1,i]
        
        Q[2*i,:3] = world_points[:,i]
        Q[2*i,3] = 1
        Q[2*i,8:11] = -u*world_points[:,i] 
        Q[2*i,11] = -u    
                               
        Q[2*i+1,4:7] = world_points[:,i]
        Q[2*i+1,7] = 1
        Q[2*i+1,8:11] = -v*world_points[:,i] 
        Q[2*i+1,11] = -v
           
    # solve the system Q*M = 0 for M
    u_of_M, s_of_M, vh_of_M = np.linalg.svd(Q)
    # reshape the vector to be 3x4 for the projection matrix M
    M = np.array(vh_of_M[-1,:]).reshape((3, 4))

    # extract the rotation matrix R
    R = M[:,0:3]
    # ensure that the determinant of R is positive. if not multiply M (and R) with -1
    if (np.linalg.det(R)) < 0:
        M = -M
        R = -R
            
    
    # We have to make sure the R is a real rotation matrix so that all eigenvalues are 1
    # so achieve this we use the SVD (R=USV) and multiply the solution together 
    # but with the identity matrix instead of S (R_tilde=UV)
    # TODO use QR
    u_of_R, s_of_R, vh_of_R = np.linalg.svd(R)
    R_tilde = np.matmul(u_of_R,vh_of_R)

    # what we have so far is a projection matrix without the correct scaling factor
    # we can get the scaling alpha by deviding the norm of R_tilde ba the norm of R
    alpha = np.linalg.norm(R_tilde)/np.linalg.norm(R)

    # Now we can put together the final M_tilde=[R_tilde|alpha*t]
    M_tilde = np.concatenate((R_tilde, alpha*M[:,3].reshape(3,1)), axis=1)
    return M_tilde

def worldToPixels(world_points, M, K):
    """
    Convers a vector in world coordinates to uv pixel coordinates (Reprojection)
    :param np.array(x, y, z, 1) Pw:     World vector 
    :return: (u,v) pixel coordinates of world point in image frame
    :rtype: Tuple[number, number]
    """
    world_points_4d = np.concatenate((world_points, np.ones((1,len(world_points[0])))), axis=0)

    Pc = np.matmul(M, world_points_4d)
    Pc_norml = (Pc / Pc[2])
    p = np.matmul(K, Pc_norml)
    uv = p[:-1]
    return uv[0], uv[1]

# get the projection matrix
M_dlt = DLTPoseEstimation(image_points, world_points, K)

pickle.dump(M_dlt, open( "Mdlt-" + str(CAMERA) + ".pkl", "wb" ))

# reproject the world point onto the image
reprojected_points = worldToPixels(world_points, M_dlt, K)

# load the image in gray-scale and plot the reprojected points onto it.
img = mpimg.imread('./images/camera-14.png')[:,:,0]
plt.imshow(img, cmap='gray')
plt.scatter(x=reprojected_points[0], y=reprojected_points[1], c='r', s=25)
plt.show()