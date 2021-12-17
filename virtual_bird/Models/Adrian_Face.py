import face_alignment
from ..Abstract import FaceDetector, LandmarksDetector


class Adrian_Face(FaceDetector, LandmarksDetector):
    def __init__(self):
        self.face_alignment = face_alignment.FaceAlignment(
            face_alignment.LandmarksType._2D, flip_input=False)

    # Overrided
    def detect_faces_from_image(self, image_RGB):
        return self.face_alignment.face_detector.detect_from_image(image_RGB)

    # Overrided
    def detect_landmarks_from_face(self, face_image, detected_face):
        landmarks = self.face_alignment.get_landmarks_from_image(
            face_image, detected_faces=[detected_face])
        return landmarks[0]


class Adrian_Face_3D(FaceDetector, LandmarksDetector):
    def __init__(self):
        self.face_alignment = face_alignment.FaceAlignment(
            face_alignment.LandmarksType._3D, flip_input=False)

    # Overrided
    def detect_faces_from_image(self, image_RGB):
        return self.face_alignment.face_detector.detect_from_image(image_RGB)

    # Overrided
    def detect_landmarks_from_face(self, face_image, detected_face):
        landmarks = self.face_alignment.get_landmarks_from_image(
            face_image, detected_faces=[detected_face])
        return landmarks[0]
