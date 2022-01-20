from ..Abstract import LandmarksDetector, HeadPoseEstimator
from .Eyes import Eyes
from .Mouth import Mouth
import numpy as np
import cv2


class Face(object):

    LANDMARKS_INDEX = { 'contour':list(range(0,17)), 
                        'left_eyebrow':list(range(17,22)), 
                        'right_eyebrow':list(range(22,27)),
                        'nasal_bridge':list(range(27,31)), 
                        'sinuses':list(range(31,36)), 
                        'left_eye':list(range(36,42)),
                        'right_eye':list(range(42,48)),
                        'mouth_outer':list(range(48,60)),
                        'mouth_inner':list(range(60,68))    }

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
        self._mouth = None
        self._center = None
        self._front_landmarks = None
        self._invCamMtx = np.linalg.inv(headposeEstimator.camera_matrix)

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
    def front_landmarks(self):
        if self._front_landmarks is None:
            self._front_landmarks = self._estimate_front_landmarks()
        return self._front_landmarks

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
    def mouth(self):
        if self._mouth is None:
            self._mouth = Mouth(self.image, self.landmarks)
        return self._mouth

    @property
    def rotation(self):
        if self._rotation is None:
            rotation, translation = self._headposeEstimator.head_pose_from_68_landmarks(
                self.landmarks)
            self._rotation, self._translation = cv2.Rodrigues(rotation)[
                0], translation
        return self._rotation

    @property
    def translation(self):
        if self._translation is None:
            rotation, translation = self._headposeEstimator.head_pose_from_68_landmarks(
                self.landmarks)
            self._rotation, self._translation = cv2.Rodrigues(rotation)[
                0], translation
        return self._translation

    @property
    def headPoseEstimator(self):
        return self._headposeEstimator

    def _headRotation(self):
        #pitch, yaw, roll = cv2.decomposeProjectionMatrix(cv2.hconcat((self.rotation, self.translation)))[6]
        pitch, yaw, roll = cv2.RQDecomp3x3(self.rotation)[0]
        return {"head": "(%.3f, %.3f, %.3f, %s)" % (roll, pitch, yaw, str(self.translation[2][0] < 0))}

    def get_all_detect_info(self):
        if self._detect_info is None:
            self._detect_info = dict()
            self._detect_info.update(self.eyes.gaze)
            self._detect_info.update(self._headRotation())
            self._detect_info.update({'mouth':self.mouth.size})
        return self._detect_info

    def _estimate_front_landmarks(self):
        P = self.headPoseEstimator.camera_matrix
        depth = self.rotation.dot(self.headPoseEstimator.static_landmarks.T) + self.translation
        depth = P.dot(depth).T   #(68,3)
        depth = depth[:,2:3] #(68,1)
        front_lmks = cv2.undistortPoints(np.expand_dims(self.landmarks, axis=0), P, self.headPoseEstimator.distance_distortion, None, P)
        front_lmks = np.concatenate((front_lmks.squeeze(), np.ones((self.landmarks.shape[0],1))), axis=1)
        front_lmks *= depth
        front_lmks = self._invCamMtx.dot(front_lmks.T)
        front_lmks -= self.translation
        front_lmks = np.linalg.inv(self.rotation).dot(front_lmks).T
        return front_lmks
    
    '''
    #deprecated
    def _fixDirectionZinverse(self, rotation, translation):

        sometimes solvePnP will wrong predict the rotation
        because of the 3D to 2D projection(3D point symmetrical to your screen will be project to same 2D point)
        these codes doesn't perfectly make sense(cuz of my space knowledgement)
        will make it better in future
    '''
