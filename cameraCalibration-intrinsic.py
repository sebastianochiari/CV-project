import os
import sys
import glob
import pickle

import argparse

import numpy as np
import cv2 as cv

parser = argparse.ArgumentParser()

parser.add_argument('--input_images', type = str, default = None)
parser.add_argument('--output_dir', type = str, default = os.path.join(sys.path[0], 'calibration-matrices/'))
parser.add_argument('--camera', type = int, default = 0)
parser.add_argument('--checkerboard', type = int, nargs='+', default = [6,9])

args = parser.parse_args()

################ CONFIGURATION PARAMETERS ################

# specify which camera you want to calibrate
CAMERA = args.camera

# specify path where images are
if args.input_images != None:
	pathToImages = args.input_images
else:
	pathToImages = './chessboard-images/camera' + str(CAMERA) + '/'

# specify output folder
outputFolder = args.output_dir

# define checkboard dimensions
CHECKERBOARD = (args.checkerboard[0], args.checkerboard[1])

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

################ -------- ################

if not os.path.isdir(outputFolder):
    os.makedirs(outputFolder)

# create a vector to store vectors of 3D points for each checkerboard image
objpoints = []
# create a vector to store vectors of 2D points for each checkerboard image
imgpoints = []

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1,2)

images = glob.glob(pathToImages + '*.jpg')

for fname in images:
	
	img = cv.imread(fname)
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	
	# find the chessboard corners
	ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, None)
    
	# if found, add object points, image points (after refining them)
	if ret == True:
		objpoints.append(objp)
		corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners2)

################ CAMERA CALIBRATION ################

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\n")
print(mtx)
print("\n")
print(dist)
print("\n")
print(rvecs)
print("\n")
print(tvecs)

################ EXPORT MATRICES ################

# Save the camera calibration result for later use
pickle.dump(mtx, open(outputFolder + "cameraMatrix-" + str(CAMERA) + ".pkl", "wb" ))
pickle.dump(dist, open(outputFolder + "dist-" + str(CAMERA) + ".pkl", "wb" ))