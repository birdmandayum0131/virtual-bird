import numpy as np
import cv2


class Pupil(object):

    def __init__(self):
        self._full_frame = None
        self._landmarks = None
        self._threshold = None
        self._iris = None
        self._tlbr = None
        self._expanded_tlbr = None
        self._frame = None
        self._cropped_margin = 5
        self._gaze = (0, 0)

    def refresh(self, frame, landmarks):
        self._full_frame = frame
        self._landmarks = landmarks

    @property
    def gaze(self):
        if self.iris is None:
            return "(0.0,0.0)"
        x, y = self.iris
        x1, y1, x2, y2 = self._tlbr
        x_align = (x - x1)/(x2 - x1)*2 - 1
        y_align = (y - y1)/(y2 - y1)*2 - 1
        self._gaze = "(%.2f,%.2f)" % (x_align, y_align)
        return self._gaze

    @property
    def iris(self):
        # opencv2 return (contour, hierarchy), but opencv3 return (img, contour, hierarchy)
        # Note: findContours will change input image(self.binary_frame)
        contours, _ = cv2.findContours(
            self.binary_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        contours = sorted(contours, key=cv2.contourArea)
        try:
            # moment:矩
            moments = cv2.moments(contours[-2])
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])
            origin = self._origin
            self._iris = (x + origin[0], y+origin[1])
            return self._iris
        except(IndexError, ZeroDivisionError):
            return None

    @property
    def frame(self):
        '''
        size, contour cropped frame
        '''
        cropped_frame = self._get_cropped_frame()
        min_x, min_y, max_x, max_y = self.expanded_tlbr
        self._frame = cropped_frame[min_y:max_y, min_x:max_x]
        return self._frame

    @property
    def binary_frame(self):
        # maybe change it to class field
        kernel = np.ones((3, 3), np.uint8)
        _binary_frame = cv2.bilateralFilter(self.frame, 10, 15, 15)
        _binary_frame = cv2.erode(_binary_frame, kernel, iterations=3)
        # ignore return value(returned threshold)
        _, _binary_frame = cv2.threshold(
            _binary_frame, self.threshold, 255, cv2.THRESH_BINARY)
        return _binary_frame

    @property
    def threshold(self):
        return np.quantile(self._frame, 0.05)

    @property
    def tlbr(self):
        x1 = np.min(self._landmarks[:, 0])
        y1 = np.min(self._landmarks[:, 1])
        x2 = np.max(self._landmarks[:, 0])
        y2 = np.max(self._landmarks[:, 1])
        self._tlbr = (x1, y1, x2, y2)
        return self._tlbr

    @property
    def expanded_tlbr(self):
        x1, y1, x2, y2 = self.tlbr
        x1, y1 = x1 - self._cropped_margin, y1 - self._cropped_margin
        x2, y2 = x2 + self._cropped_margin, y2 + self._cropped_margin
        x1, x2 = np.clip((x1, x2), 0, self._full_frame.shape[1])
        y1, y2 = np.clip((y1, y2), 0, self._full_frame.shape[0])
        self._expanded_tlbr = (x1, y1, x2, y2)
        return self._expanded_tlbr

    @property
    def _origin(self):
        return self._expanded_tlbr[:2]

    def _get_cropped_frame(self):
        height, width = self._full_frame.shape[:2]
        black_mask = np.zeros((height, width), np.uint8)  # all black mask
        # init eye mask to all white
        mask = np.full((height, width), 255, np.uint8)
        # crop pupil location in eye mask to black
        cv2.fillPoly(mask, [self._landmarks], (0, 0, 0))
        gray = cv2.cvtColor(self._full_frame.copy(), cv2.COLOR_BGR2GRAY)
        eye = cv2.bitwise_not(black_mask, gray, mask=mask)
        return eye
