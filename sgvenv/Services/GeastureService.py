import mediapipe as mp
import cv2
from mediapipe.python.solutions.hands import Hands
from mediapipe.framework.formats import landmark_pb2
from typing import Tuple


def initialize_mediapipe() -> tuple[mp.solutions.hands, Hands, mp.solutions.drawing_utils]:
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)  # This defines the hands solution
    mpDraw = mp.solutions.drawing_utils
    
    return mpHands, hands, mpDraw

def predict_hand_landmark(frame, hands) -> landmark_pb2.NormalizedLandmarkList:
    result = hands.process(frame)
    
    return result

def draw_hand_landmarks(
    handLandmarks: landmark_pb2.NormalizedLandmarkList,
    mpDraw: mp.solutions.drawing_utils,
    mpHands: mp.solutions.hands,
    frame
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    landmarks = []
    
    for handslms in handLandmarks.multi_hand_landmarks:
        for lm in handslms.landmark:
            lmx = int(lm.x * 640)
            lmy = int(lm.y * 480)

            landmarks.append([lmx, lmy])
            
        mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        
    fore_finger = (landmarks[8][0], landmarks[8][1])
    center = fore_finger
    thumb = (landmarks[4][0], landmarks[4][1])
    cv2.circle(frame, center, 3, (0, 255, 0), -1)
    
    return center, thumb