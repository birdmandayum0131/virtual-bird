from ..Abstract import HeadPoseEstimator
from ..utils.File import txt2npylandmarks, load_camera_intrinsic
import numpy as np
import cv2


class OpenCVHeadPoseEstimator(HeadPoseEstimator):

    def __init__(self, static_68_landmarks_path, frame_shape, intrinsic_path=None):
        self._static_facial_landmarks = txt2npylandmarks(static_68_landmarks_path)
        self._frame_shape = frame_shape
        self._camera_matrix = None
        self._distance_distortion = None
        '''
        These two init vector is critical for solvePnP.
        If you didn't give it a correct init direction.
        solvePnP will solve the pose unstably between two ambiguous case(in camera perspective)
        and you will get two very different value(usually normal and flipped) bouncing
        '''
        self.init_front_rvec = np.asarray([[0.0,0.0,0.0]])
        self.init_front_tvec = np.asarray([[0.0],[0.0],[1000.0]])

        if intrinsic_path is not None:
            self._camera_matrix, self._distance_distortion = load_camera_intrinsic(
                intrinsic_path)

    # Override
    @property
    def static_landmarks(self):
        return self._static_facial_landmarks

    # Override
    @property
    def camera_matrix(self):
        if self._camera_matrix is None:
            focal_length = max(self._frame_shape)
            center_coord = (
                self._frame_shape[1]/2, self._frame_shape[0]/2)
            self._camera_matrix = np.asarray([
                [focal_length, 0, center_coord[0]],
                [0, focal_length, center_coord[1]],
                [0, 0, 1]], dtype=np.float64)
        return self._camera_matrix

    # Override
    @property
    def distance_distortion(self):
        if self._distance_distortion is None:
            self._distance_distortion = np.zeros((4, 1))
        return self._distance_distortion

    # Override
    @property
    def model_size(self):
        return self._static_facial_landmarks.max(axis=0) - self._static_facial_landmarks.min(axis=0)

    # Override
    def head_pose_from_68_landmarks(self, landmarks):
        if self.init_front_rvec is None or self.init_front_tvec is None:
            _, rvec, tvec = cv2.solvePnP(self._static_facial_landmarks, landmarks, self.camera_matrix, self.distance_distortion)
        else:
            _, rvec, tvec = cv2.solvePnP(self._static_facial_landmarks, landmarks, self.camera_matrix, self.distance_distortion, self.init_front_rvec, self.init_front_tvec, useExtrinsicGuess=True)
        return (rvec, tvec)
