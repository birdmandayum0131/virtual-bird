import os
import cv2
import glob
import numpy as np

from ..utils.File import save_camera_intrinsic
from ..utils.Camera import *

resolution = res_720p


def calibrate(img_path, extension, square_size=0.024, width=9, height=6):
    # width, height : intersection points square corners met
    # numpy.float will throw out error later
    grid_coord = np.zeros((width * height, 3), np.float32)
    grid_coord[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)
    grid_coord = grid_coord * square_size
    obj_coord, img_coord = [], []
    images = glob.glob(os.path.join(img_path, "*"+extension))
    for path in images:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # find chessboard corners
        found, corners = cv2.findChessboardCorners(gray, (width, height), None)
        if found:
            obj_coord.append(grid_coord)
            preciseCorners = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            img_coord.append(preciseCorners)
            img = cv2.drawChessboardCorners(
                img, (width, height), preciseCorners, found)
            cv2.imshow(path, img)
            cv2.waitKey(0)
    cv2.destroyAllWindows()
    ret, cameraMatrix, distance_distortion, rvecs, tvecs = cv2.calibrateCamera(
        obj_coord, img_coord, gray.shape[::-1], None, None)
    return (ret, cameraMatrix, distance_distortion, rvecs, tvecs)


def main():
    ret, cameraMatrix, distance_distortion, _, _ = calibrate(
        resolution["path"], ".png")
    save_camera_intrinsic(resolution["save"],
                          (cameraMatrix, distance_distortion))
    print("Calibration is finished. RMS: ", ret)


if __name__ == '__main__':
    main()
