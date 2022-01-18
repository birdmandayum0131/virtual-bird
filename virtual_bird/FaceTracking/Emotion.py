class Emotion(object):
    
    def __init__(self, image, landmarks):
        self.image = image
        self.image_landmarks = landmarks
        self._front_landmarks = None

    @property
    def front_landmarks(self):
        if self._front_landmarks is None:
            pass
        return self._front_landmarks
    