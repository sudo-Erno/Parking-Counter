import cv2
from video_reader import video_reader
from read_yaml import read_yaml

constants = read_yaml()

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

def select_parking_slot(frame, show=False):
    for i in range(len(parking_slots)):
        start, end = parking_slots[i]

        xi, xf = sorted((start[0], end[0]))
        yi, yf = sorted((start[1], end[1]))
        
        cv2.rectangle(frame, start, end, (0, 255, 0), 2)

        if show:
            ps = frame[yi:yf, xi:xf]
            w, h = ps.shape[:2]

            if w * h < constants['MIN_AREA_THRESHOLD']:
                zf = constants['ZOOM_FACTOR']
                ps = cv2.resize(ps, (int(h*zf), int(w*zf)))
            cv2.imshow(f"PS {i}", ps)

# TODO: Hacerla funcion para que me de cada frame
while True:
    ret, frame = video_reader(cap)

    if ret:

        select_parking_slot(frame, True)

        if clicked_left and clicked_right:
            parking_slots.append([start, end])
            
            clicked_right = False
            clicked_left = False

        cv2.imshow("Frame", frame)
        cv2.setMouseCallback("Frame", click_event)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    else:
        break