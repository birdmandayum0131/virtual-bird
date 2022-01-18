import cv2
import numpy as np
import time
from collections import deque



class Visualizer(object):
    def __init__(self):
        self._image = None
        self._face = None
        self._show_landmarks = False
        self._show_headBox = False
        self._show_axis = False
        self._show_face_box = False
        self._show_fps = True
        self._show_emotion = False
        self._fps = 0
        self._fps_interval = deque(maxlen=10)
        self._start_time = time.time()
        self._end_time = None
               

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
    def show_axis(self):
        return self._show_axis

    @show_axis.setter
    def show_axis(self, value):
        self._show_axis = value

    @property
    def show_face_box(self):
        return self._show_face_box

    @show_face_box.setter
    def show_face_box(self, value):
        self._show_face_box = value

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

    @property
    def show_fps(self):
        return self._show_fps

    @show_fps.setter
    def show_fps(self, value):
        self._show_fps = value

    @property
    def show_emotion(self):
        return self._show_emotion

    @show_emotion.setter
    def show_emotion(self, value):
        self._show_emotion = value
        if not self._show_emotion:
            cv2.destroyWindow('emotion')
        
    def show(self):
        frame = self.getDetectImage()
        emotion = self.getEmotionImage()
        cv2.imshow('frame', frame)
        if self.show_emotion:
            cv2.imshow('emotion', emotion)
    
    def getDetectImage(self):
        img = self.image.copy()
        self._update_fps()
        if self.face is not None:
            if self.show_face_box:
                img = self._draw_face_box(img)
            if self.show_landmarks:
                img = self._landmark_on_frame(img)
            if self.show_headBox:
                img = self._draw_headpose_box(img)
            if self.show_axis:
                img = self._draw_head_axis(img)
        if self.show_fps:
            img = self._draw_fps(img)
        return img

    def getEmotionImage(self):
        img = np.zeros(self.image.shape, dtype=np.uint8)
        if self.face is not None:
            landmarks = self.face.front_landmarks
            landmarks[:, 0] = landmarks[:, 0] - np.mean(landmarks[:, 0]) + self.image.shape[1]/2
            landmarks[:, 1] = landmarks[:, 1] - np.mean(landmarks[:, 1]) + self.image.shape[0]/2
            img = self._landmark_on_frame(img, landmarks)
        return img

    def _draw_face_box(self, frame, color=(160,202,181), thickness=2):
        cpyFrame = frame.copy()
        x1, y1, x2, y2 = self.face.bbox[:4]
        cv2.rectangle(cpyFrame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        return cpyFrame
    
    def _landmark_on_frame(self, frame, landmarks=None, color=(255, 255, 255), thickness=1):
        if landmarks is None:
            landmarks = self.face.landmarks
        return landmark_on_frame(frame, landmarks, color, thickness)
    
    def _draw_headpose_box(self, frame, thickness=2):
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
        # for i in range(4):
        #    cv2.line(cpyFrame, tuple(point2D[i]), tuple(point2D[i+4]), (255, 64, 64), thickness, cv2.LINE_AA)
        cv2.line(cpyFrame, tuple(point2D[0]), tuple(
            point2D[4]), (255, 0, 0), thickness, cv2.LINE_AA)
        cv2.line(cpyFrame, tuple(point2D[1]), tuple(
            point2D[5]), (0, 255, 0), thickness, cv2.LINE_AA)
        cv2.line(cpyFrame, tuple(point2D[2]), tuple(
            point2D[6]), (0, 0, 255), thickness, cv2.LINE_AA)
        cv2.line(cpyFrame, tuple(point2D[3]), tuple(
            point2D[7]), (0, 0, 0), thickness, cv2.LINE_AA)

        return cpyFrame
    
    def _draw_head_axis(self, frame, thickness=3):
        cpyFrame = frame.copy()
        center = self.face.headPoseEstimator.static_landmarks.mean(axis=0)
        axis = np.float32([[0, 0, 0], [100, 0, 0], [0, 100, 0],
                          [0, 0, -100]]).reshape(-1, 3)
        axis = axis + center
        rotated_axis, _ = cv2.projectPoints(axis, self.face.rotation, self.face.translation,
                                            self.face.headPoseEstimator.camera_matrix, self.face.headPoseEstimator.distance_distortion)
        rotated_axis = [tuple(rotated_axis[i].ravel().astype(np.int))
                        for i in range(len(rotated_axis))]
        cpyFrame = cv2.line(
            cpyFrame, rotated_axis[0], rotated_axis[1], (0, 0, 255), thickness)
        cpyFrame = cv2.line(
            cpyFrame, rotated_axis[0], rotated_axis[2], (0, 255, 0), thickness)
        cpyFrame = cv2.line(
            cpyFrame, rotated_axis[0], rotated_axis[3], (255, 0, 0), thickness)
        return cpyFrame
    
    def _draw_fps(self, frame):
        cpyFrame = frame.copy()
        text = "FPS:%.1f"%(self._fps)
        textsize, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 2)
        text_w, text_h = textsize
        cv2.rectangle(cpyFrame, (0,0), (text_w+10, text_h+10), (119, 66, 141), -1)
        cv2.putText(cpyFrame, "FPS:%.1f"%(self._fps), (5, 5 + text_h + 2 - 1), cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness=2, color=(255, 255, 255))
        return cpyFrame

    def _update_fps(self):
        self._end_time = time.time()
        self._fps_interval.append(self._end_time - self._start_time)
        self._start_time = self._end_time
        self._fps = 1 / np.mean(self._fps_interval)


def landmark_on_frame(frame, landmarks, color=(255, 255, 255), thickness=1):
    cpyFrame = frame.copy()
    for mark in landmarks:
        cv2.circle(cpyFrame, (int(mark[0]), int(
            mark[1])), thickness, color, -1, cv2.LINE_AA)
    return cpyFrame
