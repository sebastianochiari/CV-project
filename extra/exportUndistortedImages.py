import os
import glob
import pickle
import cv2
import numpy as np

def loadPKLfile(pathToPKLFile):
    with open(pathToPKLFile, 'rb') as f:
        PKLfile = pickle.load(f)
    return PKLfile

def extractUndistortedImage(pathToVideo, pathToExport, camera, mtx, dist):
    
    print("Executing extractUndistortedImage() function")
    
    # create a VideoCapture object and read from input file
    videocapture = cv2.VideoCapture(pathToVideo)

    # check if camera opened successfully
    if (videocapture.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(videocapture.isOpened()):

        # capture frame-by-frame
        ret, frame = videocapture.read()

        if ret == True:

            h, w = frame.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

            # undistort
            dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]

            print("\t>>> Exporting frame")
            cv2.imwrite(pathToExport + 'camera' + str(camera) + '-undistorted.jpg', dst)

        break


if __name__ == "__main__":
    
    CAMERA  = 13
    INPUTVIDEO = './videos/calibration-' + str(CAMERA) + '-chessboard.mp4'
    OUTPUTFOLDER = './images/'

    K = loadPKLfile('./calibration-matrices/cameraMatrix-' + str(CAMERA) + '.pkl')
    dist = loadPKLfile('./calibration-matrices/dist-' + str(CAMERA) + '.pkl')

    extractUndistortedImage(INPUTVIDEO, OUTPUTFOLDER, CAMERA, K, dist)