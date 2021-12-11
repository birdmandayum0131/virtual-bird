from .Face import Face
from ..Abstract import FaceDetector, LandmarksDetector
import cv2
import threading


class FaceTracker(object):
    '''
    I think here needs some class to achieve SOLID
    but I have no idea about that now
    may be modify it in future
    '''

    def __init__(self, capture, face_detector: FaceDetector, landmarks_detector: LandmarksDetector, detectInterval=3):
        self.capture = capture
        self._face_detector = face_detector
        self._landmarks_detector = landmarks_detector
        self._face_list = []
        self.frameCount = 0
        self.detectInterval = detectInterval
        self._is_stop = False
        self._frame = None
        self._captureThread = None

    @property
    def frame(self):
        return self._frame

    def get_current_face_list(self):
        return self._face_list

    def start(self):
        self._captureThread = threading.Thread(target=self._capturing)
        self._captureThread.daemon = True
        self._captureThread.start()

    def stop(self):
        self._is_stop = True

    def _capturing(self):
        while not self._is_stop:
            _, frame = self.capture.read()
            self._frame = cv2.flip(frame, 1)
            input = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
            if self.frameCount % self.detectInterval == 0:
                dets = self._face_detector.detect_faces_from_image(
                    image_RGB=input)
                self._face_list = [
                    Face(input, bbox, self._landmarks_detector) for bbox in dets]
            self.frameCount += 1
        self.capture.release()
