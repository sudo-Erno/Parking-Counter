import cv2

def video_reader(cap, factor=0.6):
    # is_first = True

    ret, frame = cap.read()

    if ret:
        h, w = frame.shape[:2]
        h *= factor
        w *= factor

        frame = cv2.resize(frame, (int(w), int(h)))
        
        # if is_first:
        #     cv2.imwrite('ParkingSaved.jpg', frame)
        #     is_first = False

        return ret, frame