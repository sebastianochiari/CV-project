
import os
import sys

import argparse

import cv2 as cv
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--input_video', type = str, default = None)
parser.add_argument('--output_dir', type = str, default = os.path.join(sys.path[0], 'chessboard-images/'))
parser.add_argument('--camera', type = int, default = 0)
parser.add_argument('--checkerboard', type = int, nargs='+', default = [6,9])
parser.add_argument('--skip', type = int, default = 30)

args = parser.parse_args()

inputVideo = args.input_video
outputFolder = args.output_dir
camera = args.camera
skip = args.skip

if inputVideo is None:
    print("Aborting script!\n>>>> No video path has been provided.")
    exit(0)

if not os.path.isdir(outputFolder):
    os.makedirs(outputFolder)

# define checkboard dimensions
CHECKERBOARD = (args.checkerboard[0], args.checkerboard[1])

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# create a VideoCapture object and read from input file
videocapture = cv.VideoCapture(inputVideo)

# check if camera opened successfully
if (videocapture.isOpened()== False): 
   print("Aborting script!\n>>>> An error occurred while opening video stream or file")
   exit(0)

frameNumber = 0
controlInteger = 0

length = int(videocapture.get(cv.CAP_PROP_FRAME_COUNT))
print('Videocapture has a total of ' + str(length) + ' frames')

# Read until video is completed
while(videocapture.isOpened()):

    # capture frame-by-frame
    ret, frame = videocapture.read()

    if ret == True:

        print("Analyzing frame " + str(frameNumber))

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        findChessboardCornersRet, corners = cv.findChessboardCorners(gray, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

        if findChessboardCornersRet == True:

            print("\tChessboard pattern found")

            controlInteger += 1

            if controlInteger == skip:
                print("\t>>> Exporting frame")
                cv.imwrite(outputFolder + 'camera' + str(camera) + '-frame' + str(frameNumber) + '.jpg', frame)
                controlInteger = 0

    else:
        break

    frameNumber += 1

# When everything done, release the video capture object
videocapture.release()

# Closes all the frames
cv.destroyAllWindows()