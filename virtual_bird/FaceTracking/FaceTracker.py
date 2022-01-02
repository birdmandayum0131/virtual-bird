from .Face import Face
from ..Abstract import FaceDetector, LandmarksDetector, HeadPoseEstimator
import cv2
import threading


class FaceTracker(object):
    '''
    I think here needs some class to achieve SOLID
    but I have no idea about that now
    may be modify it in future
    '''

    def __init__(self, capture, face_detector: FaceDetector, landmarks_detector: LandmarksDetector, headPoseEstimator: HeadPoseEstimator):
        self.capture = capture
        self._face_detector = face_detector
        self._landmarks_detector = landmarks_detector
        self._headposeEstimator = headPoseEstimator
        self._face_list = []
        self._is_stop = False
        self._frame = None
        self._captureThread = None
        self._initThread = None
        self._detectThread = None

    @property
    def frame(self):
        return self._frame

    def get_current_face_list(self):
        return self._face_list

    def start(self):
        self._initThread = threading.Thread(target=self._init)
        self._initThread.daemon = True
        self._initThread.start()
        self._captureThread = threading.Thread(target=self._capturing)
        self._captureThread.daemon = True
        self._captureThread.start()
        self._detectThread = threading.Thread(target=self._detecting)
        self._detectThread.daemon = True
        self._detectThread.start()

    def stop(self):
        self._is_stop = True

    def _init(self):
        if not self._is_stop:
            _, frame = self.capture.read()
            self._frame = cv2.flip(frame, 1)

    def _capturing(self):
        self._initThread.join()
        while not self._is_stop:
            _, frame = self.capture.read()
            self._frame = cv2.flip(frame, 1)
        self.capture.release()

    def _detecting(self):
        self._initThread.join()
        while not self._is_stop:
            input = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
            dets = self._face_detector.detect_faces_from_image(image_RGB=input)
            self._face_list = [
                Face(input, bbox, self._landmarks_detector, self._headposeEstimator) for bbox in dets]
