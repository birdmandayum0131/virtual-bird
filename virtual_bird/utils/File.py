import numpy as np


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
