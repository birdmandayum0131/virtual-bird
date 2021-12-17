from ..Abstract import HeadPoseEstimator


class OpenCVHeadPoseEstimator(HeadPoseEstimator):

    def __init__(self, static_face_file):
        self._static_face_file = static_face_file
        self._static_68_landmarks = None

    # Override
    def head_pose_from_68_landmarks(self, landmarks):
        return super().head_pose_from_68_landmarks(landmarks)

    def static_68_landmarks(self):
        if self._static_68_landmarks is None:
            pass
        return self._static_68_landmarks
