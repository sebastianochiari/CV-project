# Computer Vision Project
This course projected consisted in implementing a combined calibration system for two different sets of camera, one having RGB cameras and another one using Motion Capture ones.

The `computervision-report.pdf` can be found inside the `report` folder.

Project for *Computer Vision* course @ UNITN

## ⚙️ Requirements

- `Python 3.8` or higher
- Latest version of [`OpenCV`](https://pypi.org/project/opencv-python/)

Specific requirements are listed in the `requirements.txt` file.

## 🔧 How to use

1. `extractChessboardImages.py`

Extracts  images (there is a skip parameter in order to avoid every frame export) where the checkerboard pattern is recognized

2. `cameraCalibration-intrinsic.py`

Once we have the images with the chessboard pattern, we fed these images to this script, which performs an intrinsc camera calibration. As output, the script exports 2 pickle files, one containing the camera matrix and the other containing the distortion parameters

3. `cameraCalibration-extrinsic.py`

In order to perform the extrinsic camera calibration, we have to find at least 4 points in the image from the camera for which we know both the in-camera plane coordinates and the world-coordinates.

> World points coordinates must be expressed in centimiters. The points must be represented in a `.csv` file, where each row represents a point in the world coordinate system, having a `X, Y, Z` format.

> Image points must be expressed in pixels. They must be in the same order as the world points coordinates provided before. The points must be represented in a `.csv` file, where each row represents a point in the image coordinates, having a `px, py` format. The `0, 0` point must be in the upper left corner.

- `worldPointsReprojection.py`

This script transposes on the basis of the corresponding camera matrices the points provided in world coordinates system into pixels. It then plots these coordinates on the provided static image of the corresponding camera.

> World points coordinates must be expressed in centimiters.

- `checkCalibrationIntegrity.py`

This script is used to visualize in 3D the cameras positioning with respect to the origin of the system in order to have a visual match between the "derived" position obtained via camera calibration and the actual position in the studio.

- `extra/DLT.py`

This script is an alternative implementation to the Perspective-n-Point Pose Computation, in order to extract the extrinsic parameters of the camera.

- `extra/exportUndistortedImages.py`

This script is used to view and later export images to which distortion is corrected.



> **N.B.** *If you are using an MJPEG video format, you have to convert the video file to an H264 codec, otherwise OpenCV will fail to read properly all the video frames.* Convert the MJPEG video to an H264 video with the following bash command.  
```
ffmpeg -i source_file.mov -pix_fmt yuv420p -b:v 4000k -c:v libx264 destination_file.mp4
```