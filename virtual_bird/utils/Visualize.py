import cv2


def landmark_on_frame(cv2_img, landmarks):
    frame = cv2_img.copy()
    for mark in landmarks:
        cv2.circle(frame, (int(mark[0]), int(mark[1])),
                   1, (255, 255, 255), -1, cv2.LINE_AA)
    return frame
