import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time
from Services.ImageService import initialize_video_stream, build_stream_frames, create_painting_canvas, display_frame
from Services.GeastureService import initialize_mediapipe, predict_hand_landmark, draw_hand_landmarks

shouldStreamBeOpen = True

def image_stream_loop():
    # Giving different arrays to handle colour points of different colour
    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]

    # These indexes will be used to mark the points in particular arrays of specific colour
    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0

    # The kernel to be used for dilation purpose 
    kernel = np.ones((5, 5), np.uint8)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    colorIndex = 0

    # Here is code for Canvas setup
    paintWindow = create_painting_canvas()

    # Initialize mediapipe
    mpHands, hands, mpDraw = initialize_mediapipe()

    # Initialize the webcam
    cap = initialize_video_stream(0)

    # Start time for 60-second streaming duration
    start_time = time.time()

    # Define the absolute path where the image will be saved (on the Raspberry Pi Desktop)
    output_filename = "DrawnImages/drawing_output.png"

    global shouldStreamBeOpen
    shouldStreamBeOpen = True
    
    while shouldStreamBeOpen:
        # Capture frame from webcam
        ret, frame, framergb = build_stream_frames(cap)
        
        if not ret:
            print("Failed to grab frame")
            break
        
        # Get hand landmark prediction
        handLandmarks = predict_hand_landmark(frame, hands)

        if handLandmarks.multi_hand_landmarks:        
            center, thumb = draw_hand_landmarks(handLandmarks, mpDraw, mpHands, frame)

            if (thumb[1] - center[1] < 30):
                # When thumb touches the center, start a new color
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

        else:
            # Append new points to the deque when no hand is detected
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        # Draw the lines on the frame (canvas and drawing window)
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        # Save the drawing if the time exceeds 60 seconds
        if time.time() - start_time >= 60:
            paintWindow = cv2.convertScaleAbs(paintWindow)  # Convert drawing to 8-bit
            cv2.imwrite(output_filename, paintWindow)  # Save drawing, not the frame
            print(f"Image saved as {output_filename}")
            break
        
        # Convert frame to bytes for streaming
        frame_bytes = get_frame_bytes(frame)

        display_frame("Test", frame)
        # Yield the frame for the MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()
    cv2.destroyAllWindows()

def get_frame_bytes(frame) -> bytes:
    # Encode frame as JPEG image
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        print("Failed to encode frame")
        return b""
    
    return jpeg.tobytes()

def stop_stream():
    global shouldStreamBeOpen
    shouldStreamBeOpen = False
