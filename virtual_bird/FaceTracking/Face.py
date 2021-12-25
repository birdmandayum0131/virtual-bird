from ..Abstract import LandmarksDetector, HeadPoseEstimator
from .Eyes import Eyes
from ..utils.Camera import euler2quaternion
from math import pi, atan2, asin
import numpy as np
import cv2


class Face(object):

    def __init__(self, img, bbox, landmarks_detector: LandmarksDetector, headposeEstimator: HeadPoseEstimator):
        self._img = img
        self._bbox = bbox
        self._landmarks_detector = landmarks_detector
        self._headposeEstimator = headposeEstimator
        self._detect_info = None
        self._landmarks = None
        self._rotation = None
        self._translation = None
        self._gaze = None
        self._eyes = None
        self._center = None

    @property
    def image(self):
        return self._img

    @property
    def landmarks(self):
        if self._landmarks is None:
            self._landmarks = self._landmarks_detector.detect_landmarks_from_face(
                self._img, self._bbox)
        return self._landmarks

    @property
    def bbox(self):
        return self._bbox

    @property
    def center(self):
        if self._center is None:
            self._center = np.asarray(
                [(self._bbox[0] + self._bbox[2])/2, (self._bbox[1] + self._bbox[3])/2]).ravel()
        return self._center

    @property
    def eyes(self):
        if self._eyes is None:
            self._eyes = Eyes(self.image, self.landmarks)
        return self._eyes

    @property
    def rotation(self):
        if self._rotation is None:
            rotation, self._translation = self._headposeEstimator.head_pose_from_68_landmarks(
                self.landmarks)
            self._rotation = self._fixDirectionZinverse(rotation)
        return self._rotation

    @property
    def translation(self):
        if self._translation is None:
            self._rotation, self._translation = self._headposeEstimator.head_pose_from_68_landmarks(
                self.landmarks)
        return self._translation

    @property
    def headPoseEstimator(self):
        return self._headposeEstimator

    def _headRotation(self):
        '''
        roll = 180*atan2(-self.rotation[2][1], self.rotation[2][2])/pi
        pitch = 180*asin(self.rotation[2][0])/pi
        yaw = 180*atan2(-self.rotation[1][0], self.rotation[0][0])/pi
        '''
        _, _, _, _, _, _, angle = cv2.decomposeProjectionMatrix(
            cv2.hconcat((self.rotation, self.translation)))
        roll, pitch, yaw = angle
        w, x, y, z = euler2quaternion(roll*pi/180, pitch*pi/180, yaw*pi/180)
        return {"head": "(%.3f, %.3f, %.3f, %.3f)" % (w, x, y, z)}

    def get_all_detect_info(self):
        if self._detect_info is None:
            self._detect_info = dict()
            self._detect_info.update(self.eyes.gaze)
            self._detect_info.update(self._headRotation())
        return self._detect_info

    def _fixDirectionZinverse(self, rotation):
        '''
        this function use simple/rough conditional expression to determine whether to inverse to symmetric the z axis

        sometimes solvePnP will wrong predict the rotation
        because of the 3D to 2D projection(3D point symmetrical to your screen will be project to same 2D point)
        these codes doesn't perfectly make sense(cuz of my space knowledgement)
        will make it better in future
        '''
        _r, _ = cv2.Rodrigues(rotation)
        if _r[:2].sum() < 0:
            _r[2, :] *= -1
        return _r
