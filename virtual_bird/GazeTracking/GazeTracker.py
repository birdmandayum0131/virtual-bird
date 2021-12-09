from .Eyes import Eyes
from ..Abstract import GazeDetector
import cv2
import threading


class GazeTracker(object):
    '''
    I think here needs some class to achieve SOLID
    but I have no idea about that now
    may be modify it in future
    '''

    def __init__(self, capture, gaze_detector: GazeDetector, detectInterval=3):
        self.capture = capture
        self.gaze_detector = gaze_detector
        self.eyes = Eyes()
        self.frameCount = 0
        self.detectInterval = detectInterval
        self.is_stop = False
        self._frame = None
        self._landmarks = None
        self.trackingThread = None
        self.gaze = None

    @property
    def frame(self):
        return self._frame

    @property
    def landmarks(self):
        return self._landmarks

    @landmarks.setter
    def landmarks(self, value):
        self._landmarks = value

    def _init_1st_frame(self):
        while not self.is_stop:
            _, frame = self.capture.read()
            self._frame = cv2.flip(frame, 1)
            if self.frame is not None:
                break

    def start(self):
        self.trackingThread = threading.Thread(target=self._tracking_face)
        self.trackingThread.daemon = True
        self.trackingThread.start()

    def _tracking_face(self):
        while not self.is_stop:
            _, frame = self.capture.read()
            self._frame = cv2.flip(frame, 1)
            detectFrame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
            if self.frameCount % self.detectInterval == 0:
                # first face
                detections = self.gaze_detector.detect_faces_from_image(
                    image_RGB=detectFrame)
                box = detections[0] if len(detections) > 0 else None
                if box is not None:
                    box = box[:4].astype(int)
                    landmarks = self.gaze_detector.detect_landmarks_from_faces(
                        face_image=detectFrame, detected_faces=[(box[0], box[1], box[2], box[3])])
                    # first face
                    self._updateProperties(landmarks[0])
            self.frameCount += 1
        self.capture.release()

    def _updateProperties(self, landmarks):
        self._landmarks = landmarks
        self.eyes.refresh(self.frame, self.landmarks)
        self.gaze = self.eyes.gaze
