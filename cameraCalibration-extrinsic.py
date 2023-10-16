import os
import sys
import glob
import pickle

import argparse

import csv

import numpy as np
import cv2 as cv

parser = argparse.ArgumentParser()

parser.add_argument('--camera', type = int, default = 0)
parser.add_argument('--calibration_folder', type = str, default = './calibration-matrices/')
parser.add_argument('--output_dir', type = str, default = os.path.join(sys.path[0], './calibration-matrices/'))
# you can omit this parameter if the points are stored inside the points folder and have the worldpoints.csv naming convention
parser.add_argument('--world_coordinates_csv', type = str, default = None)
# you can omit this parameter if the points are stored inside the points folder and have the camera(CAMERA)-points.csv naming convention
parser.add_argument('--image_pixels_csv', type = str, default= None)

args = parser.parse_args()

################ CONFIGURATION PARAMETERS ################

# specify which camera you want to calibrate
CAMERA = args.camera

if CAMERA == 0:
    print("Aborting script!\n>>>> No valid camera has been provided.")
    exit(0)

# specify path where calibration matrices are
pklFolder = args.calibration_folder

output_dir = args.output_dir

################ IMPORT PICKLE FILES ################

matrixFileName = pklFolder + 'cameraMatrix-' + str(CAMERA) + '.pkl'
distFileName = pklFolder + 'dist-' + str(CAMERA) + '.pkl'

with open(matrixFileName, 'rb') as f:
    K = pickle.load(f)
    print(K)

with open(distFileName, 'rb') as f:
    dist = pickle.load(f)
    print(dist)

################ -------- ################

################ LOAD POINTS ################

# ------ world points ------ #

world_coordinates_csv = args.world_coordinates_csv

if(world_coordinates_csv == None):
    world_coordinates_csv = './points/worldpoints.csv'

world_coordinates_list = []

with open(world_coordinates_csv, 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        # Convert the x and y values to integers and create a tuple
        x, y, z = map(float, row)
        point = (x, y, z)
        world_coordinates_list.append(point)

WORLDPOINTS = 0.01 * np.array(world_coordinates_list, dtype = 'double')

# ------ image points ------ #

image_pixels_csv = args.image_pixels_csv

if(image_pixels_csv == None):
    image_pixels_csv = './points/camera' + str(CAMERA) + '-points.csv'

image_pixels_list = []

with open(image_pixels_csv, 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        # Convert the x and y values to integers and create a tuple
        x, y = map(int, row)
        point = (x, y)
        image_pixels_list.append(point)

IMAGEPOINTS = np.array(image_pixels_list, dtype = 'double')

################ -------- ################

################ SOLVEPNP ################

ret, rvec, tvec = cv.solvePnP(WORLDPOINTS, IMAGEPOINTS, K, dist, flags=0)

print("RVEC")
print(rvec)
print(type(rvec))
print("TVEC")
print(tvec)
print(type(tvec))

pickle.dump(rvec, open(output_dir + "rvec-" + str(CAMERA) + ".pkl", "wb" ))
pickle.dump(tvec, open(output_dir + "tvec-" + str(CAMERA) + ".pkl", "wb" ))