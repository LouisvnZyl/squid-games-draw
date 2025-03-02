import cv2
import numpy as np
import io

def initialize_video_stream(sourceIndex: int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(sourceIndex)
    
    return cap
    
def create_painting_canvas() -> np.ndarray:
    paintWindow = np.zeros((471, 636, 3)) + 255
    
    return paintWindow
    
def build_stream_frames(cap: cv2.VideoCapture):    
    # Read each frame from the capture source
    ret, frame = cap.read()
    
    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    return ret, frame, framergb

def display_frame(frameName: str ,frame):
    cv2.imshow(frameName, frame)
