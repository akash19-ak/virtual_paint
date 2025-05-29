import cv2
import mediapipe as mp
import numpy as np
# Initialize
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
# Canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
draw_color = (255, 0, 255)  # Default: purple
prev_x, prev_y = 0, 0
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    # Show color buttons
    cv2.rectangle(frame, (0, 0), (80, 80), (255, 0, 255), -1)   # Purple
    cv2.rectangle(frame, (80, 0), (160, 80), (0, 255, 0), -1)   # Green
    cv2.rectangle(frame, (160, 0), (240, 80), (0, 0, 255), -1)  # Red
    cv2.rectangle(frame, (240, 0), (320, 80), (50, 50, 50), -1) # Eraser button
    cv2.putText(frame, "ERS", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.rectangle(frame, (560, 0), (640, 80), (0, 0, 0), -1)    # Clear button
    cv2.putText(frame, "CLR", (565, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm = handLms.landmark
            x = int(lm[8].x * w)  # Index fingertip
            y = int(lm[8].y * h)
            # Check finger up (index up, middle down)
            finger_up = lm[8].y < lm[6].y and lm[12].y > lm[10].y
            # Color selection
            if y < 80:
                if x < 80:
                    draw_color = (255, 0, 255)  # Purple
                elif x < 160:
                    draw_color = (0, 255, 0)    # Green
                elif x < 240:
                    draw_color = (0, 0, 255)    # Red
                elif x < 320:
                    draw_color = (0, 0, 0)      # Eraser
                elif x > 560:
                    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
            # Drawing
            if finger_up:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y
                # Set eraser thickness
                thickness = 30 if draw_color == (0, 0, 0) else 5
                cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = 0, 0

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
    # Merge canvas with frame
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow("Virtual Painter", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break
cap.release()
cv2.destroyAllWindows()
