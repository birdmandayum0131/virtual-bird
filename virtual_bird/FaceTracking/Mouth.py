import numpy as np
import cv2
from .Eyes import Eyes

class Mouth(object):
    '''
    This class manage mouth informations
    '''
    MOUTH_OUTER_LANDMARKS_INDEX = list(range(48, 60))
    MOUTH_INNER_LANDMARKS_INDEX = list(range(60, 68))

    def __init__(self, img, landmarks):
        self._image = img
        self._mouth_inner_landmarks = landmarks[self.MOUTH_INNER_LANDMARKS_INDEX].astype(
            np.int32)
        self._mouth_outer_landmarks = landmarks[self.MOUTH_OUTER_LANDMARKS_INDEX].astype(
            np.int32)
        self._left_eye_landmarks = landmarks[Eyes.LEFT_EYE_LANDMARKS_INDEX].astype(
            np.int32)
        self._right_eye_landmarks = landmarks[Eyes.RIGHT_EYE_LANDMARKS_INDEX].astype(
            np.int32)
        self._countours = None
        self._size = None

    @property
    def size(self):
        '''
        Here I use eye size to estimate how size the mouth opening
        Because I think the shape of eye is similar to mouth
        So the variant in scene may be similar too(and make the estimation more reliable).
        '''
        if self._size is None:
            _, mouth_inner, left_eye, right_eye = self.countours
            avg_eye_area = (cv2.contourArea(left_eye) + cv2.contourArea(right_eye)) / 2
            mouth_inner_area = cv2.contourArea(mouth_inner)
            self._size = mouth_inner_area / avg_eye_area
        return self._size

    @property
    def countours(self):
        if self._countours is None:
            mouth_outer = self._mouth_outer_landmarks.reshape((-1,1,2))
            mouth_inner = self._mouth_inner_landmarks.reshape((-1,1,2))
            left_eye = self._left_eye_landmarks.reshape((-1,1,2))
            right_eye = self._right_eye_landmarks.reshape((-1,1,2))
            self._countours = [mouth_outer, mouth_inner, left_eye, right_eye]
        return self._countours


    
