import cv2
import face_alignment
from GazeTracking import GazeTracker
from TcpServer import TcpSender


def main():
    faceAlgnmt = face_alignment.FaceAlignment(
        face_alignment.LandmarksType._2D, flip_input=False)
    gazeTracker = GazeTracker(cv2.VideoCapture(
        0), faceAlgnmt.face_detector, faceAlgnmt)
    gazeTracker.start()
    unitySender = TcpSender(host="127.0.0.1", port=1208)
    unitySender.startUpListen()
    while True:
        frame = gazeTracker.frame
        landmarks = gazeTracker.landmarks
        if landmarks is not None:
            if gazeTracker.gaze is not None:
                unitySender.transportFaceData(gazeTracker.gaze)
            for mark in landmarks:
                cv2.circle(frame, (int(mark[0]), int(mark[1])),
                           1, (255, 255, 255), -1, cv2.LINE_AA)

            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            gazeTracker.is_stop = True
            break
    gazeTracker.capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
