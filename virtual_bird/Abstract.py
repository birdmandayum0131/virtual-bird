import abc


class FaceDataTransportHandler:
    @abc.abstractmethod
    def transportFaceData(self, dataDict: dict):
        raise NotImplementedError("Abstract method not implemented!")


class FaceDetector:
    @abc.abstractmethod
    def detect_faces_from_image(self, image_RGB):
        raise NotImplementedError("Abstract method not implemented!")


class LandmarksDetector:
    @abc.abstractmethod
    def detect_landmarks_from_face(self, face_image, detected_face):
        raise NotImplementedError("Abstract method not implemented!")


class HeadPoseEstimator:
    @abc.abstractmethod
    def head_pose_from_68_landmarks(self, landmarks):
        raise NotImplementedError("Abstract method not implemented!")

    @abc.abstractproperty
    def static_landmarks(self):
        raise NotImplementedError("Abstract property not implemented!")

    @abc.abstractproperty
    def camera_matrix(self):
        raise NotImplementedError("Abstract property not implemented!")

    @abc.abstractproperty
    def distance_distortion(self):
        raise NotImplementedError("Abstract property not implemented!")

    @abc.abstractproperty
    def model_size(self):
        raise NotImplementedError("Abstract property not implemented!")
