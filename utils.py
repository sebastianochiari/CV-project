import os
import glob
import pickle

import numpy as np
import cv2 as cv

def loadPKLfile(pathToPKLFile):
    with open(pathToPKLFile, 'rb') as f:
        PKLfile = pickle.load(f)
    return PKLfile