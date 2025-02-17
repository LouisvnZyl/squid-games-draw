import mediapipe as mp

def initialize_mediapipe():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7) #This defines the sts
    mpDraw = mp.solutions.drawing_utils
    
    return mpHands, hands, mpDraw

def predict_hand_landmark(frame, hands):
    result = hands.process(frame)
    
    return result;