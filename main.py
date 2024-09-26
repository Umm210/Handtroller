import cv2
import pyautogui
import mediapipe as mp

cap = cv2.VideoCapture(0)

# check to see if the camera opens properly or not
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# importing hand solutions to detect hand landmarks
mp_hands = mp.solutions.hands

# Confidence detection 50%
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

# state of the keys
w_state = False
a_state = False
s_state = False
d_state = False

while True:
    ret, frame = cap.read()  # captures frame one by one
    if not ret:  # checks if the frames were captured or not
        break  # exits the loop if frames were not captured

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # changing color format so mediapipe can read it
    result = hands.process(image_rgb)  # processes the frames to detect the hand landmarks

    # Default to False for key states
    w_key = a_key = s_key = d_key = False

    # If hand is detected will contain landmark data for the hand
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # visualizes the hand landmarks

            # extracting hand landmarks coordinates
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # defining hand gestures
            w_key = middle_finger_tip.y > thumb_tip.y
            a_key = ring_finger_tip.y > thumb_tip.y
            s_key = pinky_tip.y > thumb_tip.y
            d_key = index_finger_tip.y > thumb_tip.y

            # W key
            if w_key:
                pyautogui.keyDown('w')
                print('W down')
            elif not w_key and w_state:
                pyautogui.keyUp('w')
                print('W up')

            # A key
            if a_key:
                pyautogui.keyDown('a')
                print('A down')
            elif not a_key and a_state:
                pyautogui.keyUp('a')
                print('A up')

            # S key
            if s_key:
                pyautogui.keyDown('s')
                print('S down')
            elif not s_key and s_state:
                pyautogui.keyUp('s')
                print('S up')

            # D key
            if d_key:
                pyautogui.keyDown('d')
                print('D down')
            elif not d_key and d_state:
                pyautogui.keyUp('d')
                print('D up')

            # Update the previous states
            w_state = w_key
            a_state = a_key
            s_state = s_key
            d_state = d_key

    cv2.imshow('Handtroller', frame)

    # Ends the script
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyWindow('Handtroller')
