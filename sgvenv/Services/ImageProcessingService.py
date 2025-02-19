import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time
from Services.ImageService import initialize_video_stream, build_stream_frames, create_painting_canvas
from Services.GeastureService import initialize_mediapipe, predict_hand_landmark, draw_hand_landmarks

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

    start_time = time.time()

    # Define the absolute path where the image will be saved (on the Raspberry Pi Desktop)
    output_filename = "DrawnImages/drawing_output.png"
    
    ret, frame, framergb = build_stream_frames(cap)
    
    while time.time() - start_time < 60:
        # Get hand landmark prediction
        handLandmarks = predict_hand_landmark(frame, hands)

        #This code below will probably need modification to make use of a wand of some sorts when drawing over the frame but, this needs to be investigated more.
        # Post process the handLandmarks
        if handLandmarks.multi_hand_landmarks:        
            center, thumb = draw_hand_landmarks(handLandmarks, mpDraw, mpHands, frame)

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

        # Draw lines of all the colors on the canvas and frame
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        # Display the frame (if necessary)

        # display_frame("Output", frame)
        # display_frame("Paint", paintWindow) 

        if time.time() - start_time >= 60:  # Save 0.5 seconds before the time runs out
            paintWindow = cv2.convertScaleAbs(paintWindow)  # Convert the drawing to 8-bit
            cv2.imwrite(output_filename, paintWindow)  # Save only the drawing, not the frame
            print(f"Image saved as {output_filename}")
            
        frame_bytes = get_frame_bytes(frame)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()
    cv2.destroyAllWindows()
    
def get_frame_bytes(frame) -> bytes:
    ret, jpeg = cv2.imencode('.jpg', frame)
    
    frame_bytes = jpeg.tobytes()
    
    return frame_bytes