# Technical Documentation

This is a guide to using the scripts that make up the code to calibrate two independent camera systems. Each script can be called as stand-alone based on the level of information you have for each camera and the output you want to collect. 

**This guide will assume that no previous calibration has been done**.  
**Please stick to the naming convention**.

### Step 1 - Image Extraction

First, you need to retrive images from the camera(s) you want to calibrate. These images must have a detectable checkerboard pattern in order to successfully perform the following step.

#### `extractChessboardImages.py`

If you have a video where you show to the camera the checkerboard pattern, this script will preprocess the video and automatically export some frames that will be used lately to perform camera calibration. The script takes as argument the following parameters:

``` py
--input_video, type = str, default = None
# it specify the path of the video you want to preprocess, SCRIPT WILL ABORT IF THIS PARAMETER IS EQUAL TO NONE
--output_dir, type = str, default = os.path.join(sys.path[0], 'chessboard-images/')
# you can specify where you want the images to be exported to
--camera, type = int, default = 0
# for naming purposes, you can specify the number of the camera you are calibrating
--checkerboard, type = int, nargs='+', default = [6,9]
# if you are using a checkerboard with a pattern that differs from the (6,9) one, you can specify it with this argument
--skip, type = int, default = 30
# this parameter determines how many candidate frames will be skipped after finding one frame having the checkboard pattern (it is used to avoid the export of hundreds of frames) 
```

This script will output the following files:
- a set of images (in the specified folder) having the checkerboard pattern recognized by `cv2.findChessboardCorners` function

### Step 2 - `cameraCalibration-intrinsic.py`

This script performs the intrinsic camera calibration through the `cv2.calibrateCamera` function, given a set of images where it can be detected the chessboard pattern. The script takes as argument the following parameters:

```py
--input_images, type = str, default = None
# specifies where the images with the pattern are stored
--output_dir, type = str, default = os.path.join(sys.path[0], 'calibration-matrices/')
# defines where the calibration matrices will be saved once the script ended
--camera, type = int, default = 0
# for naming purposes, you can specify the number of the camera you are calibrating
--checkerboard, type = int, nargs='+', default = [6,9]
# if you are using a checkerboard with a pattern that differs from the (6,9) one, you can specify it with this argument
```

The script exports the following matrices:
- `cameraMatrix-{CAMERA_NUMBER}.pkl`: it stores the camera matrix of the given camera
- `dist-{CAMERA_NUMBER}.pkl`: it stores the distortion parameters of the given camera

### Step 3 - `cameraCalibration-extrinsic.py`

This step can be tricky, because you need to find a set of points (at least 4) that are shared between both camera systems. They also need to be coplanar. You need to take the world coordinates of those points and the pixel coordinates for each camera.

> World points coordinates must be expressed in centimiters. The points must be represented in a `.csv` file, where each row represents a point in the world coordinate system, having a `X, Y, Z` format.

> Image points must be expressed in pixels. They must be in the same order as the world points coordinates provided before. The points must be represented in a `.csv` file, where each row represents a point in the image coordinates, having a `px, py` format. The `0, 0` point must be in the upper left corner.

This script performs through `cv2.solvePnP` function. The script takes as argument the following parameters:

```py
--camera', type = int, default = 0
# specify the camera number, so the script will automatically handle all the files (IF YOU STICK TO THE NAMING CONVENTION)
--calibration_folder', type = str, default = './calibration-matrices/'
# specifies where the camera matrix and distortion parameters are stored
--output_dir', type = str, default = os.path.join(sys.path[0], './calibration-matrices/')
# defines where the rvec and tvec files will be saved once the script ended
--world_coordinates_csv', type = str, default = None
# you need to specify the path to the world coordinates csv file
# you can omit this parameter if the points are stored inside the points folder and have the worldpoints.csv naming convention
--image_pixels_csv', type = str, default= None
# you need to specify the path to the world coordinates csv file
# you can omit this parameter if the points are stored inside the points folder and have the camera{CAMERA_NUMBER}-points.csv naming convention
```

This script exports the following vectors:
- `rvec-{CAMERA_NUMBER}.pkl`: it stores the rotation vector of the given camera
- `tvec-{CAMERA_NUMBER}.pkl`: it stores the translation vector of the given camera

### Step 4 (*integrity check*) - `worldPointsReprojection.py`

This script transposes on the basis of the corresponding camera matrices the points provided in world coordinates system into pixels. It then plots these coordinates on the provided static image of the corresponding camera.

```py
--camera, type = int, default = 0
# specify the camera, the script will handle all the different files (STICK TO THE NAMING AND FOLDER CONVENTION)
```

If you didn't stick to the naming convention, you can edit the following variables in order to correctly import the four different matrices:

```py
K       # path to the camera matrix
tvec    # path to the translation vector
rvec    # path to the rotation vector
img     # path to the image to display with the reprojected points plotted 
```

More, you can specify the points (using world coordinates **in centimiters**) you want to reproject.
You can edit the following variable, where each row represents a coordinate and each column represents a set of coordinates describing a world point

```py
world_points = 0.01 * np.array(
    [
        [0., 50., 100., 50., 100.], # X coordinate
        [0., 0., 0., 0., 0.], # Y coordinate
        [0., 50., 50., 100., 100.]  # Z coordinate
    ]
)
```

As output, it will be displayed the provided image with the reprojected points.

### Step 5 (*integrity check*) - `checkCalibrationIntegrity.py`

This script is used to visualize in 3D the cameras positioning with respect to the origin of the system in order to have a visual match between the "derived" position obtained via camera calibration and the actual position in the studio.

You need to provide the list of the cameras you want to plot, editing the following variables:

```py
# list of all the cameras you want to plot (this will follow the naming convention)
CAMERAS = [1, ..., 14]

# dictionary that maps camera numbers into colors for visual representation purposes
colors_dict = {
    "1": "#FA6971",
    ... ,
    "14": "#6AFA8E"
}
```

You can also customize which world points (expressed in centimeters) you want to plot, by editing the following variable:

```py
# each entry represents a (X, Y, Z) point
OBJECTPOINTS = 0.01 * np.array([
        (0., 0., 0.),
        (50.0, 0., 50.),
        (100.0, 0., 50.0),
        (50.0, 0., 100.0),
        (100.0, 0., 100.0)
    ])
```

Since in our system the Y axes is the theatre floor, the following variable handles the visual representation of the plot in order to be consistent with our truth orientation. You can edit these parameters to change how the plot is rotated.

```py
ax.view_init(elev=130, azim=-90)
```