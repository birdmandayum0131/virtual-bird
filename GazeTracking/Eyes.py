from .pupil import Pupil
import numpy as np


class Eyes(object):
    '''
    This class manage two eye informations
    '''

    def __init__(self):
        self._frame = None
        self._landmarks = None
        self._left_eye_landmarks = None
        self._right_eye_landmarks = None
        self.left = Pupil()
        self.right = Pupil()
        self.LEFT_EYE_LANDMARKS_INDEX = list(range(36, 42))
        self.RIGHT_EYE_LANDMARKS_INDEX = list(range(42, 48))
        self._gaze = {"left": (0, 0), "right": (0, 0)}

    def refresh(self, frame, landmarks):
        self._frame = frame
        self._landmarks = landmarks
        self.left.refresh(frame, self.left_eye_landmarks)
        self.right.refresh(frame, self.right_eye_landmarks)

    @property
    def gaze(self):
        self._gaze["left"] = self.left.gaze
        self._gaze["right"] = self.right.gaze
        return self._gaze

    @property
    def left_eye_landmarks(self):
        self._left_eye_landmarks = self._landmarks[self.LEFT_EYE_LANDMARKS_INDEX].astype(
            np.int32)
        return self._left_eye_landmarks

    @property
    def right_eye_landmarks(self):
        self._right_eye_landmarks = self._landmarks[self.RIGHT_EYE_LANDMARKS_INDEX].astype(
            np.int32)
        return self._right_eye_landmarks
