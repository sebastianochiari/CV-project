import os
import glob

import cv2 as cv
import numpy as np

import pickle

import argparse

from utils import loadPKLfile

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

parser = argparse.ArgumentParser()

parser.add_argument('--camera', type = int, default = 0)

args = parser.parse_args()

camera = args.camera

world_points = 0.01 * np.array(
    [
        [0., 50., 100., 50., 100.], # X
        [0., 0., 0., 0., 0.], # Y
        [0., 50., 50., 100., 100.]  # Z
    ]
)

def worldToPixels(world_points, K, rvec, tvec):

    # create a 4D point
    world_points_4D = np.concatenate((world_points, np.ones((1, len(world_points[0])))), axis = 0)

    # retrieve the rotation matrix starting from the rvec
    rotation_matrix, _ = cv.Rodrigues(rvec)

    # concatenate R with T in order to have the R|T matrix
    RT = np.concatenate((rotation_matrix, tvec), axis=1)

    Pc_homogeneous = np.matmul(RT, world_points_4D)

    PcK = np.matmul(K, Pc_homogeneous)

    PcK_normalized = PcK / PcK[2]

    uv = PcK_normalized[:-1]

    return uv

if __name__ == "__main__":

    K = loadPKLfile('./calibration-matrices/cameraMatrix-' + str(camera) + '.pkl')
    rvec = loadPKLfile('./calibration-matrices/rvec-' + str(camera) + '.pkl')
    tvec = loadPKLfile('./calibration-matrices/tvec-' + str(camera) + '.pkl')

    reprojected_points = worldToPixels(world_points, K, rvec, tvec)

    img = mpimg.imread('./images/camera-' + str(camera) + '.png')[:,:,0]
    
    plt.imshow(img, cmap='gray')
    plt.scatter(x=reprojected_points[0], y=reprojected_points[1], c='r', s=25)

    plt.show()