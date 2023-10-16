import os
import glob

import cv2 as cv
import numpy as np

import pickle

from utils import loadPKLfile

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

CAMERAS = [1, 3, 5, 12, 13, 14]

colors_dict = {
    "1": "#FA6971",
    "3": "#7DBA8C",
    "5": "#6AFA8E",
    "7": "#A57C7F",
    "12": "#544DFA",
    "13": "#FADD4E",
    "14": "#6C6AA5",
}

def plotObjectPoints(ax):

    OBJECTPOINTS = 0.01 * np.array([
        (0., 0., 0.),
        (50.0, 0., 50.),
        (100.0, 0., 50.0),
        (50.0, 0., 100.0),
        (100.0, 0., 100.0)
    ])

    for entry in OBJECTPOINTS:
        ax.scatter(entry[0], entry[1], entry[2], c='b', marker='o')

def plotCameraPosition(ax, camera):
    
    # import rvec and tvec vectors
    rvec_camera = loadPKLfile('./calibration-matrices/rvec-' + str(camera) + '.pkl')
    tvec_camera = loadPKLfile('./calibration-matrices/tvec-' + str(camera) + '.pkl')
    
    # convert rvec to a rotation matrix
    rotation_matrix, _ = cv.Rodrigues(rvec_camera)
    
    # transform rotation matrix from camera coordinates to world coordinates
    rvec_world = rotation_matrix.transpose()

    # transform rotation matrix from camera coordinates to world coordinates
    tvec_world = np.dot(np.negative(rvec_world), tvec_camera)

    # camera position
    camera_position = tvec_world.flatten()

    camera_direction = rvec_world[:, 2]  # Extract the third column (z-axis)

    # Scale the direction vector to visualize it
    scaling_factor = 10.0  # Adjust the scaling factor as needed
    camera_direction_scaled = camera_position + scaling_factor * camera_direction

    pointLabel = 'Camera ' + str(camera)

    # Plot the camera position
    ax.scatter(camera_position[0], camera_position[1], camera_position[2], c=colors_dict[str(camera)], marker='o', label=pointLabel)

    # Plot the camera direction vector as an arrow
    # ax.quiver(camera_position[0], camera_position[1], camera_position[2],
    #         camera_direction_scaled[0] - camera_position[0],
    #         camera_direction_scaled[1] - camera_position[1],
    #         camera_direction_scaled[2] - camera_position[2],
    #         color='b', arrow_length_ratio=0.1)


if __name__ == "__main__":
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    # plot points on the ground
    plotObjectPoints(ax)

    for camera in CAMERAS:
        plotCameraPosition(ax, camera)

    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # add legend
    ax.legend()

    ax.view_init(elev=130, azim=-90)  # Adjust the elev and azim angles as needed

    # show the plot
    plt.show()