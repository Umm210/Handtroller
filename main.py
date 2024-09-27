import cv2
import pyautogui
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)

# check to see if the camera opens properly or not
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# importing hand solutions to detect hand landmarks
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,  # confidence detection 50%
    min_tracking_confidence=0.7)

mp_drawing = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()  # captures frame one by one
    if not ret:  # checks if the frames were captured or not
        break  # exits the loop if frames were not captured

    # Flip the frame horizontally for a mirrored effect
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # changing color format so mediapipe can read it
    result = hands.process(image_rgb)  # processes the frames to detect the hand landmarks

    # Default states
    w_key = a_key = s_key = d_key = space_key = False
    w_state = a_state = s_state = d_state = space_state = False
    screen_width, screen_height = pyautogui.size()

    # previous mouse position

    smooth_factor = 1  # higher = smoother but slower response

    # checking for hand detection
    if result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):

            # checking right or left hand
            handedness = result.multi_handedness[idx].classification[0].label

            # draws hand landmarks
            # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # visualizes the hand landmarks

            # extracting hand coordinates
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

            # for left hand (wasd hand)
            if handedness == 'Left':

                # defining hand gestures
                w_key = middle_finger_tip.y > thumb_tip.y or middle_finger_tip.y > middle_finger_mcp.y
                a_key = ring_finger_tip.y > thumb_tip.y or ring_finger_tip.y > ring_finger_mcp.y
                s_key = pinky_finger_tip.y > thumb_tip.y or pinky_finger_tip.y > pinky_finger_mcp.y
                d_key = index_finger_tip.y > thumb_tip.y or index_finger_tip.y > index_finger_mcp.y
                space_key = thumb_tip.y > thumb_mcp.y

                # W key
                if w_key:
                    pyautogui.keyDown('w')
                    print('W down')
                elif not w_key and w_state:
                    pyautogui.keyUp('w')
                    # print('W up')

                # A key
                if a_key:
                    pyautogui.keyDown('a')
                    print('A down')
                elif not a_key and a_state:
                    pyautogui.keyUp('a')
                    # print('A up')

                # S key
                if s_key:
                    pyautogui.keyDown('s')
                    print('S down')
                elif not s_key and s_state:
                    pyautogui.keyUp('s')
                    # print('S up')

                # D key
                if d_key:
                    pyautogui.keyDown('d')
                    print('D down')
                elif not d_key and d_state:
                    pyautogui.keyUp('d')
                    # print('D up')

                # Space key
                # if space_key:
                #     pyautogui.keyDown('space')
                #     print('Space down')
                # elif not space_key and space_state:
                #     pyautogui.keyUp('space')
                #     print('Space up')

                # calculating distance between index and thumb to trigger mouse click
                thumb_index_distance = math.sqrt(
                    (index_finger_mcp.x - thumb_tip.x) ** 2 + (index_finger_mcp.y - thumb_tip.y) ** 2)
                if thumb_index_distance < 0.04:
                    pyautogui.keyDown('space')
                    print('Space down')
                else:
                    pyautogui.keyUp('space')
                    # print('Space up')

                # update the previous states
                w_state = w_key
                a_state = a_key
                s_state = s_key
                d_state = d_key
                space_state = space_key

            # for right hand (mouse hand)
            if handedness == 'Right':

                prev_mouse_x = prev_mouse_y = 0

                # getting new mouse coordinates from the index fingertip
                new_mouse_x = int(index_finger_tip.x * screen_width)
                new_mouse_y = int(index_finger_tip.y * screen_height)

                # applying smoothness by averaging the current position with the previous one
                if prev_mouse_x is not None and prev_mouse_y is not None:
                    mouse_x = int(smooth_factor * new_mouse_x + (1 - smooth_factor) * prev_mouse_x)
                    mouse_y = int(smooth_factor * new_mouse_y + (1 - smooth_factor) * prev_mouse_y)
                else:
                    mouse_x, mouse_y = new_mouse_x, new_mouse_y

                pyautogui.moveTo(mouse_x, mouse_y)

                clicking = False

                # calculating distance between index and thumb to trigger mouse click
                thumb_index_distance = math.sqrt(
                    (index_finger_tip.x - thumb_tip.x) ** 2 + (index_finger_tip.y - thumb_tip.y) ** 2)

                if thumb_index_distance < 0.08:
                    if not clicking:
                        pyautogui.mouseDown()
                        clicking = True
                        print('click')
                else:
                    if clicking:
                        pyautogui.mouseUp()
                        clicking = False
                        print('mouse up')
    # window setting
    window_width = 800
    window_height = 600

    cv2.namedWindow('Handtroller', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Handtroller', window_width, window_height)
    cv2.moveWindow('Handtroller', (screen_width - window_width) // 2, (screen_height - window_height) // 2)
    cv2.imshow('Handtroller', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyWindow('Handtroller')
