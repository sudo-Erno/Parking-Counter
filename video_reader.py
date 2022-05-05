import cv2

def video_reader(cap, factor=0.6):

    ret, frame = cap.read()

    if ret:
        h, w = frame.shape[:2]
        h *= factor
        w *= factor

        frame = cv2.resize(frame, (int(w), int(h)))

        return ret, frame