import cv2
from virtual_bird.Models.Adrian_Face import *
from virtual_bird.Models.Dlib_model import *
from virtual_bird.Models.OpenCVHeadPose import *

class Config(object):
    '''
    This design of config class is refer to YOLACT config #https://github.com/dbolya/yolact/blob/master/data/config.py
    I hesitated between YOLACT and YAML( like Detectron2) config design
    And I think this project is not huge to need YAML design now
    '''
    def __init__(self, config_dict):
        for key, val in config_dict.items():
            self.__setattr__(key, val)

    def copy(self, new_config_dict={}):
        old_config_dict = Config(vars(self))
        old_config_dict.replace(new_config_dict)
        return old_config_dict

    def replace(self, new_config_dict):
        if isinstance(new_config_dict, Config):
            new_config_dict = vars(new_config_dict)

        for key, val in new_config_dict.items():
            self.__setattr__(key, val)

    def show(self):
        for key, val in vars(self).items():
            print(key, ' = ', val)

res_240p = Config({
    "width": 320,
    "height": 240,
    "save": "virtual_bird/CameraCalibration/240p.yaml"
})

res_480p = Config({
    "width": 640,
    "height": 480,
    "path": "virtual_bird/CameraCalibration/480p",
    "save": "virtual_bird/CameraCalibration/480p.yaml"
})

res_720p = Config({
    "width": 1280,
    "height": 720,
    "path": "virtual_bird/CameraCalibration/720p",
    "save": "virtual_bird/CameraCalibration/720p.yaml"
})

model_config = Config({
    'face_detector' : Config({
        'dlib' : Dlib_Face(),
        'sfd' : Adrian_Face(face_detector=Adrian_Face.S3FD),
        'blazeface' : Adrian_Face(face_detector=Adrian_Face.BlazeFace)
    }),

    'landmarks_detector' : Config({
        'dlib' : Dlib_Landmark(),
        'FAN' : Adrian_Face(landmarksType=Adrian_Face.Landmarks_2D)
    }),

    'head_pose_estimator' : Config({
        'openCV' : OpenCVHeadPoseEstimator
    })
})

criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

base_config = Config({
    'face_detector' : model_config.face_detector.blazeface,
    'landmarks_detector' : model_config.landmarks_detector.FAN,
    'head_pose_estimator' : model_config.head_pose_estimator.openCV,
    'camera' : res_240p,
    'landmarks_static_model' : 'birdFace.txt'
})

cfg = base_config.copy()