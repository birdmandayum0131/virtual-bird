import numpy as np
import cv2


def landmarks2txt(landmarks, file_path):
    with open(file_path, 'w') as file:
        for idx in range(len(landmarks)):
            landmark = landmarks[idx]
            save_data = str(idx)
            for coord in landmark:
                save_data += " %.2f" % coord
            save_data += "\n"
            file.write(save_data)


def txt2npylandmarks(file_path):
    landmarks = []
    with open(file_path, 'r') as file:
        pointCount = 0
        raw_data = file.readline()
        while raw_data:
            raw_data = [float(item) for item in raw_data.split()[1:]]
            landmarks.append(raw_data)
            raw_data = file.readline()
            pointCount += 1
        print("read %d landmarks" % (pointCount))
    return np.asarray(landmarks)


def save_camera_intrinsic(path, intrinsic):
    cameraMatrix, distanceDistortion = intrinsic
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("camera matrix", cameraMatrix)
    cv_file.write("distance distortion", distanceDistortion)
    cv_file.release()


def load_camera_intrinsic(path):
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    cameraMatrix = cv_file.getNode("camera matrix").mat()
    distanceDistortion = cv_file.getNode("distance distortion").mat()
    cv_file.release()
    return (cameraMatrix, distanceDistortion)
