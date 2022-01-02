import dlib
import numpy as np
from ..Abstract import FaceDetector, LandmarksDetector

class Dlib_Face(FaceDetector):
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def detect_faces_from_image(self, image_RGB):
        return [[dlib_rectangle.left(), dlib_rectangle.top(), dlib_rectangle.right(), dlib_rectangle.bottom()] for dlib_rectangle in self.detector(image_RGB, 1)]

class Dlib_Landmark(LandmarksDetector):
    def __init__(self, dat_file="./virtual_bird/weights/shape_predictor_68_face_landmarks.dat"):
        self.detector = dlib.shape_predictor(dat_file)

    def detect_landmarks_from_face(self, face_image, detected_face):
        left, top, right, bottom = detected_face[:4]
        shape = self.detector(face_image, dlib.rectangle(int(left), int(top), int(right), int(bottom)))
        return np.asarray([(shape.part(i).x, shape.part(i).y) for i in range(68)], dtype=np.float)