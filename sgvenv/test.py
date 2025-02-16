import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time

# All the imports go here

# This is the main runninf file (Just a test to see if the concept works).

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
paintWindow = np.zeros((471, 636, 3)) + 255

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7) #This defines the sts
mpDraw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0) # This refers to the video capture device of index 0. More can be added if more are available by changing the index.
ret = True
start_time = time.time()

# Define the absolute path where the image will be saved (on the Raspberry Pi Desktop)
output_filename = "DrawnImages/drawing_output.png"

# The idea here is to have this loop be an inner functioning loop in the overall program.
# We will allow someone to draw an image with the given time below and once time runs out we want to then store the drawn picture frame.
# This frame will then be presented to the model and an evaluation result will then be presented based on the model.
# With the model some tips I can give is to have a class load in the model and see if that can be stored as a property. This can be done on the constructor.
# Then you instantiate the model class at the start so that it all gets initialised and then you can make use of it. This is to save on memory and processing time.

while time.time() - start_time < 120:
    # Read each frame from the webcam
    ret, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    #This code below will probably need modification to make use of a wand of some sorts when drawing over the frame but, this needs to be investigated more.
    # Post process the result
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
    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow) # The paint window represents the actual drawing over the screen and not the video being captured by the webcam.
    # you can also think about not showing the output frame and only show the blank canvas butm the output frame will still be used as reference in the code.

    # Save the image when the time is near the limit (0.5 seconds before it runs out)
    #Look at improving this as this will close out the screen as well event if the while loop is set to close after 2 minutes due to the break in the function.
    if time.time() - start_time >= 60:  # Save 0.5 seconds before the time runs out
        paintWindow = cv2.convertScaleAbs(paintWindow)  # Convert the drawing to 8-bit
        cv2.imwrite(output_filename, paintWindow)  # Save only the drawing, not the frame
        print(f"Image saved as {output_filename}")
        break  # Exit the loop once the image is saved

    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

# General tips will be to remember separation of concerns when it comes to your files.
# Keep each section seperate if the are not related by function and even look at extrating some of the drawing and opencv functionality with the webcam.
# This is to ensure software engineering principles are followed making it much easier to follow, maintain and debug with minimal overhead to set it up.
# The above will be a life saver when it is crunch time. Go and google SOLID principles in software engineering.