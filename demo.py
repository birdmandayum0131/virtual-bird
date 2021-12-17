import cv2
import time
from virtual_bird.utils.Visualize import landmark_on_frame
from virtual_bird.FaceTracking import FaceTracker
from virtual_bird.TcpServer import TcpServer
from virtual_bird.Models.Adrian_Face import Adrian_Face
from virtual_bird.utils.File import txt2npylandmarks


def main():
    show_landmarks = False
    detecting = False
    adrian_Face = Adrian_Face()
    faceTracker = FaceTracker(cv2.VideoCapture(0), adrian_Face, adrian_Face)
    faceTracker.start()
    unitySender = TcpServer(host="127.0.0.1", port=1208)
    unitySender.startUpListen()
    while True:
        frame = faceTracker.frame
        if frame is None:
            time.sleep(0.5)
            continue
        if detecting:
            face_list = faceTracker.get_current_face_list()
            if len(face_list) > 0:
                first_face = face_list[0]
                dets_dict = first_face.get_all_detect_info()
                unitySender.transportFaceData(dets_dict)
                if show_landmarks:
                    frame = landmark_on_frame(frame, first_face.landmarks)
                    import pdb
                    pdb.set_trace()
        cv2.imshow('frame', frame)
        action = cv2.waitKey(1) & 0xFF
        if action == ord('q'):
            faceTracker.stop()
            break
        elif action == ord('l'):
            show_landmarks = not show_landmarks
            print("show landmarks : "+str(show_landmarks))
        elif action == ord('d'):
            detecting = not detecting
            print("detecting : "+str(detecting))
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
