import cv2
import time
from virtual_bird.utils.Camera import *
from virtual_bird.utils.Visualize import Visualizer
from virtual_bird.FaceTracking import FaceTracker
from virtual_bird.TcpServer import TcpServer
from virtual_bird.Models.Adrian_Face import Adrian_Face
from virtual_bird.Models.OpenCVHeadPose import OpenCVHeadPoseEstimator

resolution = res_480p


def main():
    detecting = False
    camera = cv2.VideoCapture(0)
    w, h = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(
        cv2.CAP_PROP_FRAME_HEIGHT)
    headPoseEstimator = OpenCVHeadPoseEstimator(
        "birdFace.txt", (w, h), resolution["save"])
    faceDetector = Adrian_Face()
    landmarksDetector = faceDetector  # AdrianFace can also be landmarks detector
    faceTracker = FaceTracker(camera, faceDetector,
                              landmarksDetector, headPoseEstimator)
    visualizer = Visualizer()
    faceTracker.start()

    unitySender = TcpServer(host="127.0.0.1", port=1208)
    unitySender.startUpListen()

    while True:
        frame = faceTracker.frame
        if frame is None:
            time.sleep(0.5)
            continue
        visualizer.image = frame
        if detecting:
            face_list = faceTracker.get_current_face_list()
            if len(face_list) > 0:
                first_face = face_list[0]
                dets_dict = first_face.get_all_detect_info()
                unitySender.transportFaceData(dets_dict)
                visualizer.face = first_face
        frame = visualizer.getRenderImage()
        cv2.imshow('frame', frame)
        action = cv2.waitKey(1) & 0xFF
        if action == ord('q'):
            faceTracker.stop()
            break
        elif action == ord('l'):
            visualizer.show_landmarks = not visualizer.show_landmarks
            print("show landmarks : "+str(visualizer.show_landmarks))
        elif action == ord('d'):
            detecting = not detecting
            print("detecting : "+str(detecting))
        elif action == ord('h'):
            visualizer.show_headBox = not visualizer.show_headBox
            print("show head Box : "+str(visualizer.show_headBox))
            #import pdb
            # pdb.set_trace()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
