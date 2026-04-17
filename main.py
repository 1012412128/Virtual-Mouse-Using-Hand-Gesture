import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Button, Controller
import math
import time
import random

# -----------------------------
# Setup
# -----------------------------
mouse = Controller()
screen_width, screen_height = pyautogui.size()

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# -----------------------------
# Variables
# -----------------------------
last_click_time = 0
cooldown = 0.5

prev_x, prev_y = 0, 0
smooth_factor = 5

dragging = False
drag_start_time = 0
drag_delay = 0.3  # HOLD time for drag

paused = False

# -----------------------------
# Helper Functions
# -----------------------------
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])     #Euclidean Distance

def move_mouse(finger_tip):
    global prev_x, prev_y

    x = int(finger_tip[0] * screen_width)
    y = int(finger_tip[1] * screen_height)

    x = prev_x + (x - prev_x) / smooth_factor
    y = prev_y + (y - prev_y) / smooth_factor

    pyautogui.moveTo(int(x), int(y))
    prev_x, prev_y = x, y

def is_fist(landmarks):
    return all(landmarks[i][1] > landmarks[0][1] for i in [8, 12, 16, 20])

# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        landmarks = [(lm.x, lm.y) for lm in hand.landmark]

        if len(landmarks) == 21:

            wrist = landmarks[0]
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            pinky_tip = landmarks[20]

            hand_size = distance(wrist, landmarks[9])
            click_thresh = hand_size * 0.4

            current_time = time.time()

            # -----------------------------
            # PAUSE
            # -----------------------------
            if is_fist(landmarks):
                paused = not paused
                time.sleep(0.7)

            if paused:
                cv2.putText(frame, "PAUSED", (200,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
                cv2.imshow("Virtual Mouse", frame)
                continue

            # Move cursor
            move_mouse(index_tip)

            # Distances (Euclidean Distance)
            d_thumb_index = distance(thumb_tip, index_tip)
            d_thumb_middle = distance(thumb_tip, middle_tip)   
            d_thumb_pinky = distance(thumb_tip, pinky_tip)
            d_index_middle = distance(index_tip, middle_tip)

            # -----------------------------
            # DRAG + CLICK (IMPORTANT)
            # -----------------------------
            if d_thumb_index < click_thresh:

                if drag_start_time == 0:
                    drag_start_time = current_time

                # HOLD → DRAG
                elif current_time - drag_start_time > drag_delay:
                    if not dragging:
                        mouse.press(Button.left)
                        dragging = True

            else:
                # RELEASE DRAG
                if dragging:
                    mouse.release(Button.left)
                    dragging = False

                # QUICK TAP → CLICK
                if drag_start_time != 0 and current_time - drag_start_time < drag_delay:
                    if current_time - last_click_time > cooldown:
                        mouse.click(Button.left)
                        last_click_time = current_time

                drag_start_time = 0

            # -----------------------------
            # DOUBLE CLICK
            # -----------------------------
            if d_thumb_index < click_thresh and d_thumb_middle < click_thresh:
                if current_time - last_click_time > cooldown:
                    pyautogui.doubleClick()
                    last_click_time = current_time

            # -----------------------------
            # RIGHT CLICK
            # -----------------------------
            elif d_thumb_middle < click_thresh:
                if current_time - last_click_time > cooldown:
                    mouse.click(Button.right)
                    last_click_time = current_time

            # -----------------------------
            # SCREENSHOT
            # -----------------------------
            elif d_thumb_pinky < click_thresh:
                if current_time - last_click_time > cooldown:
                    img = pyautogui.screenshot()
                    name = f"screenshot_{random.randint(1,1000)}.png"
                    img.save(name)
                    last_click_time = current_time

            # -----------------------------
            # SCROLL (UP & DOWN)
            # -----------------------------
            if d_index_middle < click_thresh:
                if index_tip[1] < wrist[1]:
                    pyautogui.scroll(30)   # UP
                else:
                    pyautogui.scroll(-30)  # DOWN

            # -----------------------------
            # Visual feedback
            # -----------------------------
            for tip in [thumb_tip, index_tip, middle_tip, pinky_tip]:
                cv2.circle(frame,
                           (int(tip[0]*640), int(tip[1]*480)),
                           10, (0,255,255), cv2.FILLED)

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()