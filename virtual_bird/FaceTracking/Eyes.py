from .pupil import Pupil
import numpy as np


class Eyes(object):
    '''
    This class manage two eye informations
    '''
    LEFT_EYE_LANDMARKS_INDEX = list(range(36, 42))
    RIGHT_EYE_LANDMARKS_INDEX = list(range(42, 48))

    def __init__(self, img, landmarks):
        self._image = img
        self._left_eye_landmarks = landmarks[self.LEFT_EYE_LANDMARKS_INDEX].astype(
            np.int32)
        self._right_eye_landmarks = landmarks[self.RIGHT_EYE_LANDMARKS_INDEX].astype(
            np.int32)
        self.left = Pupil(img, self._left_eye_landmarks)
        self.right = Pupil(img, self._right_eye_landmarks)
        self._gaze = None  # {"left": (0, 0), "right": (0, 0)}

    @property
    def gaze(self):
        if self._gaze is None:
            self._gaze = dict()
            self._gaze["left"] = self.left.gaze
            self._gaze["right"] = self.right.gaze
        return self._gaze
