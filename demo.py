import cv2
import time
from config.config import cfg
from virtual_bird.utils.Camera import *
from virtual_bird.utils.Visualize import Visualizer
from virtual_bird.FaceTracking import FaceTracker
from virtual_bird.SocketServer import UdpServer as SocketServer


def main():
    camera = cv2.VideoCapture(0)
    change_resolution(camera, cfg.camera.width, cfg.camera.height)
    w, h = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(
        cv2.CAP_PROP_FRAME_HEIGHT)
    headPoseEstimator = cfg.head_pose_estimator("birdFace.txt", (w, h), cfg.camera.save)
    faceTracker = FaceTracker(camera, cfg.face_detector, cfg.landmarks_detector, headPoseEstimator)
    visualizer = Visualizer()
    faceTracker.start()
    unitySender = SocketServer(host="127.0.0.1", port=1208)
    unitySender.start()

    while True:
        frame = faceTracker.frame
        if frame is None:
            time.sleep(0.5)
            continue
        visualizer.image = frame
        face_list = faceTracker.get_current_face_list()
        if len(face_list) > 0:
            first_face = face_list[0]
            dets_dict = first_face.get_all_detect_info()
            unitySender.transportFaceData(dets_dict)
            visualizer.face = first_face
        visualizer.show()
        action = cv2.waitKey(1) & 0xFF
        if action == ord('q'):
            faceTracker.stop()
            break
        elif action == ord('f'):
            visualizer.show_face_box = not visualizer.show_face_box
            print("show face box : "+str(visualizer.show_face_box))
        elif action == ord('l'):
            visualizer.show_landmarks = not visualizer.show_landmarks
            print("show landmarks : "+str(visualizer.show_landmarks))
        elif action == ord('h'):
            visualizer.show_headBox = not visualizer.show_headBox
            print("show head Box : "+str(visualizer.show_headBox))
        elif action == ord('a'):
            visualizer.show_axis = not visualizer.show_axis
            print("show head axis : "+str(visualizer.show_axis))
        elif action == ord('e'):
            visualizer.show_emotion = not visualizer.show_emotion
            print("show emotion : "+str(visualizer.show_emotion))
    
    unitySender.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
