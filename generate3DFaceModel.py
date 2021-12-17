import cv2
import time
import numpy as np
from virtual_bird.utils.Visualize import landmark_on_frame
from virtual_bird.utils.File import landmarks2txt
from virtual_bird.FaceTracking import FaceTracker
from virtual_bird.Models.Adrian_Face import Adrian_Face_3D


def main():
    save_landmarks = []
    adrian_Face = Adrian_Face_3D()
    faceTracker = FaceTracker(cv2.VideoCapture(0), adrian_Face, adrian_Face)
    faceTracker.start()
    while True:
        frame = faceTracker.frame
        if frame is None:
            time.sleep(0.5)
            continue
        face_list = faceTracker.get_current_face_list()
        if len(face_list) > 0:
            first_face = face_list[0]
            frame = landmark_on_frame(frame, first_face.landmarks)
        cv2.imshow('frame', frame)
        action = cv2.waitKey(1) & 0xFF
        if action == ord('q'):
            faceTracker.stop()
            break
        elif action == ord('p'):
            want_save = input("want save?: ")
            if want_save == "y":
                i_landmarks = first_face.landmarks
                i_landmarks[:, :2] -= first_face.bbox[:2]
                save_landmarks.append(i_landmarks)
        elif action == ord('c'):
            i_landmarks = first_face.landmarks
            i_landmarks[:, :2] -= first_face.bbox[:2]
            save_landmarks.append(i_landmarks)
        elif action == ord('s'):
            np_landmarks = np.asarray(save_landmarks)
            np_landmarks = np_landmarks.mean(axis=0)
            check_frame = landmark_on_frame(np.zeros_like(frame), np_landmarks)
            cv2.imshow('landmarks', check_frame)
            cv2.waitKey(0)
            want_save = input("save to file?: ")
            if want_save == "y":
                landmarks2txt(np_landmarks, "birdFace.txt")
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
