from ..Abstract import LandmarksDetector
from .Eyes import Eyes


class Face(object):

    def __init__(self, img, bbox, landmarks_detector: LandmarksDetector):
        self._img = img
        self._bbox = bbox
        self._landmarks_detector = landmarks_detector
        self._detect_info = None
        self._landmarks = None
        self._gaze = None
        self._eyes = None

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
    def eyes(self):
        if self._eyes is None:
            self._eyes = Eyes(self.image, self.landmarks)
        return self._eyes

    def get_all_detect_info(self):
        if self._detect_info is None:
            self._detect_info = dict()
            self._detect_info.update(self.eyes.gaze)
        return self._detect_info
