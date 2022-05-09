import cv2
from matplotlib.style import available
from video_reader import video_reader
from utils.read_yaml import read_yaml
from utils.read_coordinates import get_coordinates

constants = read_yaml()

parking_place_coordinates = get_coordinates()
parking_slots = []

cap = cv2.VideoCapture('src/Parking.mp4')

# Load the parking slots coordinates
for parking in parking_place_coordinates[1:]:
    parking = parking.split('\n')[0]
    parking = parking.split(',')
    parking_slots.append(parking)

def draw_parking_slots(box_frame, processed_framed, empty=0.22): # Debug use to show how many white pixels are in each selected parking slot
    painting_frame = box_frame.copy()
    
    total_slots = len(parking_slots)
    occupied_slots = 0

    for i in range(len(parking_slots)):
        is_free = True
        ratio = 0

        slot_id, xi, yi, xf, yf = parking_slots[i]

        xi, xf = sorted((xi, xf))
        yi, yf = sorted((yi, yf))

        xi, yi, xf, yf = int(xi), int(yi), int(xf), int(yf)
        
        ps = processed_framed[yi:yf, xi:xf]
        h, w = ps.shape[:2]

        non_zero_pixels = cv2.countNonZero(ps)
        if w * h != 0:
            ratio = non_zero_pixels / (w * h)
        
        if ratio > empty:
            is_free = False
            occupied_slots += 1
    
        # cv2.putText(box_frame, str(slot_id),
        #             ((xi + xf)//2, (yi + yf)//2),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             0.5, (0, 255, 255), 1, cv2.LINE_AA)
        
        if not is_free:
            cv2.rectangle(painting_frame, (xi, yi), (xf, yf), (0, 0, 255), -1)
            cv2.rectangle(box_frame, (xi, yi), (xf, yf), (0, 0, 255), 2)
        else:
            cv2.rectangle(painting_frame, (xi, yi), (xf, yf), (0, 255, 0), -1)
            cv2.rectangle(box_frame, (xi, yi), (xf, yf), (0, 255, 0), 2)

        available_slots = total_slots - occupied_slots
        cv2.putText(box_frame, f"Available: {available_slots}/{total_slots}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    
    return cv2.addWeighted(box_frame, constants['ALPHA'], painting_frame, 1-constants['ALPHA'], 0)

while True:
    ret, frame = video_reader(cap)
    
    if ret:
        
        # Process frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th_frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)

        final_frame = draw_parking_slots(frame, th_frame, constants['EMPTY'])

        cv2.imshow("Parking", final_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break