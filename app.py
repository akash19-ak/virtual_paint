from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Canvas and drawing color
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
draw_color = (255, 0, 255)  # Default: purple
prev_x, prev_y = 0, 0

# Video streaming generator
def gen_frames():
    global prev_x, prev_y, canvas, draw_color
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        # UI Buttons
        cv2.rectangle(frame, (0, 0), (80, 80), (255, 0, 255), -1)   # Purple
        cv2.rectangle(frame, (80, 0), (160, 80), (0, 255, 0), -1)   # Green
        cv2.rectangle(frame, (160, 0), (240, 80), (0, 0, 255), -1)  # Red
        cv2.rectangle(frame, (240, 0), (320, 80), (50, 50, 50), -1) # Eraser
        cv2.putText(frame, "ERS", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.rectangle(frame, (560, 0), (640, 80), (0, 0, 0), -1)    # Clear
        cv2.putText(frame, "CLR", (565, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                lm = handLms.landmark
                x = int(lm[8].x * w)  # Index fingertip
                y = int(lm[8].y * h)
                finger_up = lm[8].y < lm[6].y and lm[12].y > lm[10].y

                # Color selection
                if y < 80:
                    if x < 80:
                        draw_color = (255, 0, 255)
                    elif x < 160:
                        draw_color = (0, 255, 0)
                    elif x < 240:
                        draw_color = (0, 0, 255)
                    elif x < 320:
                        draw_color = (0, 0, 0)
                    elif x > 560:
                        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
                    prev_x, prev_y = 0, 0
                elif finger_up:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = x, y
                    thickness = 30 if draw_color == (0, 0, 0) else 5
                    cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                    prev_x, prev_y = x, y
                else:
                    prev_x, prev_y = 0, 0

                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        # Overlay canvas
        frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
