from .Eyes import Eyes
import cv2
import threading
import time


class GazeTracker(object):
    '''
    I think here needs some class to achieve SOLID
    but I have no idea about that now
    may be modify it in future
    '''

    def __init__(self, capture, face_detector, landmark_detector, detectInterval=3):
        self.capture = capture
        self.face_detector = face_detector
        self.landmark_detector = landmark_detector
        self.eyes = Eyes()
        self.frameCount = 0
        self.detectInterval = detectInterval
        self.is_stop = False
        self._frame = None
        self._landmarks = None
        self.captureThread = None
        self.trackingThread = None
        self.initThread = None
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
        '''
        self.initThread = threading.Thread(target=self._init_1st_frame)
        self.initThread.daemon = True
        self.initThread.start()

        self.captureThread = threading.Thread(target=self._queryframe)
        self.captureThread.daemon = True
        self.captureThread.start()
        '''
        self.trackingThread = threading.Thread(target=self._tracking_face)
        self.trackingThread.daemon = True
        self.trackingThread.start()

    def _tracking_face(self):
        # self.initThread.join()
        while not self.is_stop:
            _, frame = self.capture.read()
            self._frame = cv2.flip(frame, 1)
            detectFrame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
            if self.frameCount % self.detectInterval == 0:
                # first face
                detections = self.face_detector.detect_from_image(detectFrame)
                box = detections[0] if len(detections) > 0 else None
                if box is not None:
                    box = box[:4].astype(int)
                    landmarks = self.landmark_detector.get_landmarks_from_image(
                        detectFrame, detected_faces=[(box[0], box[1], box[2], box[3])])
                    # first face
                    self._landmarks = landmarks[0]
                    self.eyes.refresh(self.frame, self.landmarks)
                    self.gaze = self.eyes.gaze

            self.frameCount += 1
        self.capture.release()
