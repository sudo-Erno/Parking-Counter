import cv2
from video_reader import video_reader
from read_yaml import read_yaml
from time import time

start_time = time()

parking_place_coordinates = []

cap = cv2.VideoCapture('src/Parking.mp4')

start = (0, 0)
end = (0, 0)

parking_slots = []

clicked_right, clicked_left = False, False

def click_event(event, x, y, flags, params):
    global start, end, clicked_right, clicked_left

    if event == cv2.EVENT_LBUTTONDOWN:
        start = x, y
        clicked_left = True
    
    if event == cv2.EVENT_RBUTTONDOWN:
        if clicked_left:
            end = x, y
            clicked_right = True
        else:
            for coords in parking_slots:
                start, end = coords
                
                xi, xf = start[0], end[0]
                yi, yf = start[1], end[1]

                if (xi <= x <= xf or xi >= x >= xf) and (yi<= y <= yf or yi >= y >= yf):
                    parking_slots.remove([start, end])

frame = []

while True:
    ret, frame = video_reader(cap)
    finish_time = time()

    if finish_time - start_time > 3:
        break

while True:
    clean_frame = frame.copy()
    
    if clicked_left and clicked_right:
        parking_slots.append([start, end])
        
        clicked_right = False
        clicked_left = False

    for s in parking_slots:
        cv2.rectangle(clean_frame, s[0], s[1], (0, 255, 0), 2)
    
    cv2.imshow("Parking", clean_frame)
    cv2.setMouseCallback("Parking", click_event)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

with open('utils\slots_coordinates.txt', 'a') as f:
    for coord in parking_slots:
        start, end = coord
        xi, xf = sorted((start[0], end[0]))
        yi, yf = sorted((start[1], end[1]))
        
        f.writelines([f"{str(xi)},{str(yi)},{str(xf)},{str(yf)}\n"])