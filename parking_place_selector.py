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

def select_parking_slot(box_frame, processed_framed, debug=False): # Debug use to show how many white pixels are in each selected parking slot
    for i in range(len(parking_slots)):
        is_free = True

        start, end = parking_slots[i]

        xi, xf = sorted((start[0], end[0]))
        yi, yf = sorted((start[1], end[1]))
        
        ps = processed_framed[yi:yf, xi:xf]

        non_zero_pixels = cv2.countNonZero(ps)

        if non_zero_pixels > constants['NONZERO_PIXELS']:
            is_free = False
        
        if debug:
            w, h = ps.shape[:2]

            if w * h < constants['MIN_AREA_THRESHOLD']:
                zf = constants['ZOOM_FACTOR']
                ps = cv2.resize(ps, (int(h*zf), int(w*zf)))
            
            if debug:
                cv2.putText(box_frame, str(non_zero_pixels),
                            ((xi + xf)//2, (yi + yf)//2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 0), 2)

            cv2.imshow(f"PS {i}", ps)
        
        if not is_free:
            cv2.rectangle(box_frame, start, end, (0, 0, 255), 2)
        else:
            cv2.rectangle(box_frame, start, end, (0, 255, 0), 2)

# TODO: Hacerla funcion para que me de cada frame
while True:
    ret, frame = video_reader(cap)
    if ret:

        if clicked_left and clicked_right:
            parking_slots.append([start, end])
            
            clicked_right = False
            clicked_left = False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th_frame = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)

        select_parking_slot(frame, th_frame, True)

        cv2.imshow("Parking", frame)
        cv2.setMouseCallback("Parking", click_event)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break