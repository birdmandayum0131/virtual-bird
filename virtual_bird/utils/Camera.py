import numpy as np
import cv2

res_480p = {"width": 640, "height": 480, "path": "virtual_bird/CameraCalibration/480p",
            "save": "virtual_bird/CameraCalibration/480p.yaml"}
res_720p = {"width": 1280, "height": 720, "path": "virtual_bird/CameraCalibration/720p",
            "save": "virtual_bird/CameraCalibration/720p.yaml"}
criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def change_resolution(capture, width, height):
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print("camera resolution set to %d × %d" %
          (capture.get(3), capture.get(4)))


def euler2quaternion(roll, pitch, yaw):
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - \
        np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + \
        np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - \
        np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + \
        np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    return (qw, qx, qy, qz)
