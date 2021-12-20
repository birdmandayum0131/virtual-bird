import os
import cv2
from ..utils.Camera import *

resolution = res_720p


def main():
    cap = cv2.VideoCapture(0)
    change_resolution(cap, resolution["width"], resolution["height"])
    if not os.path.isdir(resolution["path"]):
        os.mkdir(resolution["path"])
    imageCount = 0
    while True:
        _, frame = cap.read()
        cv2.imshow('frame', frame)
        action = cv2.waitKey(1) & 0xFF
        if action == ord('q'):
            break
        elif action == ord('s'):
            img_path = os.path.join(
                resolution["path"], "%d.png" % (imageCount))
            cv2.imwrite(img_path, frame)
            print("Saved %s" % (img_path))
            imageCount += 1
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
