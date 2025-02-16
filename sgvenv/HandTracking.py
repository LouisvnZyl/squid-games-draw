import mediapipe as mp
import cv2
from collections import deque

def initialise_mediapipe():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7) #This defines the sts
    mpDraw = mp.solutions.drawing_utils
    
    return mpHands, hands, mpDraw

def build_hand_tracking(paintWindow, framergb, frame, bpoints, mpHands, hands, mpDraw):    
    result = hands.process(framergb)
    
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])
        cv2.circle(frame, center, 3, (0, 255, 0), -1)
        print(center[1] - thumb[1])
        if (thumb[1] - center[1] < 30):
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        elif center[1] <= 65:
            if 40 <= center[0] <= 140:  # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 1  # Green
            elif 390 <= center[0] <= 485:
                colorIndex = 2  # Red
            elif 505 <= center[0] <= 600:
                colorIndex = 3  # Yellow
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    # Append the next deques when nothing is detected to avoid messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1