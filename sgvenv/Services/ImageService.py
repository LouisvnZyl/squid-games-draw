import cv2
import numpy as np

def build_mapped_streams(sourceIndex: int):
    cap = cv2.VideoCapture(sourceIndex)
    
def create_painting_canvas(canvasName: str, windowSize: int):
    paintWindow = np.zeros((471, 636, 3)) + 255
    
    cv2.namedWindow(canvasName, windowSize)
    
def initialize_video_source(sourceIndex: int):
    cap = cv2.VideoCapture(sourceIndex)
    
    ret, frame = cap.read()
    
    x, y, c = frame.shape
    
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    return ret, frame, framergb