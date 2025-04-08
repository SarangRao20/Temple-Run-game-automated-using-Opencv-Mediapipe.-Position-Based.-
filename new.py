import cv2
import mediapipe as mp
import pydirectinput
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

last_action_time = time.time()
cooldown = 0.005  # seconds

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, c = img.shape

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            index_tip = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_tip.x * w), int(index_tip.y * h)

            # Draw index tip
            cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)

            current_time = time.time()

            if current_time - last_action_time > cooldown:
                if x < w // 3:
                    pydirectinput.press("left")
                    action = "Left"
                elif x > 2 * w // 3:
                    pydirectinput.press("right")
                    action = "Right"
                elif y < h // 3:
                    pydirectinput.press("up")
                    action = "Jump"
                elif y > 2 * h // 3:
                    pydirectinput.press("down")
                    action = "Slide"
                else:
                    action = "Run"

                last_action_time = current_time

                cv2.putText(img, f'Action: {action}', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Draw region lines
    cv2.line(img, (w // 3, 0), (w // 3, h), (255, 255, 255), 2)
    cv2.line(img, (2 * w // 3, 0), (2 * w // 3, h), (255, 255, 255), 2)
    cv2.line(img, (0, h // 3), (w, h // 3), (255, 255, 255), 2)
    cv2.line(img, (0, 2 * h // 3), (w, 2 * h // 3), (255, 255, 255), 2)

    cv2.imshow("Finger Control - Temple Run", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
