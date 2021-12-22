import cv2
import numpy as np


class Visualizer(object):
    def __init__(self):
        self._image = None
        self._face = None
        self._show_landmarks = False
        self._show_headBox = False

    @property
    def show_landmarks(self):
        return self._show_landmarks

    @show_landmarks.setter
    def show_landmarks(self, value):
        self._show_landmarks = value

    @property
    def show_headBox(self):
        return self._show_headBox

    @show_headBox.setter
    def show_headBox(self, value):
        self._show_headBox = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, value):
        self._face = value

    def getRenderImage(self):
        img = self.image.copy()
        if self.show_landmarks:
            img = self._landmark_on_frame(img)
        if self.show_headBox:
            img = self._draw_headpose_box(img)
            #img = self.debug_landmark_on_frame(img)
        return img

    def _landmark_on_frame(self, frame, color=(255, 255, 255), thickness=1):
        return landmark_on_frame(frame, self.face.landmarks, color, thickness)

    def _draw_headpose_box(self, frame, color=(128, 128, 255), thickness=2):
        cpyFrame = frame.copy()
        # get static model center
        x, y, _ = self.face.headPoseEstimator.static_landmarks.mean(axis=0)
        # half width, half height
        hw, hh, _ = self.face.headPoseEstimator.model_size / 2
        rear_box = [(x-hw, y-hh, 0), (x-hw, y+hh, 0),
                    (x+hw, y+hh, 0), (x+hw, y-hh, 0)]
        # scaling width, scaling height, deepth
        d = hw+hh
        front_box = [(x-hw, y-hh, -d), (x-hw, y+hh, -d),
                     (x+hw, y+hh, -d), (x+hw, y-hh, -d)]
        # already translate to center in above(for uncalibrate camera)
        # may fixed in future
        point3D = np.asarray(rear_box + front_box, dtype=np.float)
        point2D, _ = cv2.projectPoints(point3D, self.face.rotation, self.face.translation,
                                       self.face.headPoseEstimator.camera_matrix, self.face.headPoseEstimator.distance_distortion)
        point2D = point2D.reshape(-1, 2).astype(np.int)
        # draw rear box
        # cv2.polylines(cpyFrame, [point2D[:4]], isClosed=True,
        #              color=(64, 64, 255), thickness=thickness, lineType=cv2.LINE_AA)
        cv2.drawContours(cpyFrame, [point2D[:4]], -1, (64, 64, 255, 128), -3)
        # draw front box
        cv2.polylines(cpyFrame, [point2D[4:]], isClosed=True,
                      color=(64, 255, 64), thickness=thickness, lineType=cv2.LINE_AA)
        # connect four side edges
        for i in range(4):
            cv2.line(cpyFrame, tuple(point2D[i]), tuple(
                point2D[i+4]), (255, 64, 64), thickness, cv2.LINE_AA)
        return cpyFrame


def landmark_on_frame(frame, landmarks, color=(255, 255, 255), thickness=1):
    cpyFrame = frame.copy()
    for mark in landmarks:
        cv2.circle(cpyFrame, (int(mark[0]), int(
            mark[1])), thickness, color, -1, cv2.LINE_AA)
    return cpyFrame
