import face_alignment
from ..Abstract import FaceDetector, LandmarksDetector


class Adrian_Face(FaceDetector, LandmarksDetector):

    S3FD = 'sfd'
    BlazeFace = 'blazeface'
    '''
    Dlib = 'dlib'
    I can't use it on my device(I guess some bugs related to dlib-gpu version occurred)
    '''
    Landmarks_2D = face_alignment.LandmarksType._2D
    Landmarks_3D = face_alignment.LandmarksType._3D

    def __init__(self, face_detector=S3FD, landmarksType = Landmarks_2D):
        self.face_alignment = face_alignment.FaceAlignment(
            landmarksType, flip_input=False, face_detector=face_detector)

    # Overrided
    def detect_faces_from_image(self, image_RGB):
        return self.face_alignment.face_detector.detect_from_image(image_RGB)

    # Overrided
    def detect_landmarks_from_face(self, face_image, detected_face):
        landmarks = self.face_alignment.get_landmarks_from_image(
            face_image, detected_faces=[detected_face])
        return landmarks[0]


