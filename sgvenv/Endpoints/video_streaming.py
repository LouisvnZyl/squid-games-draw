import cv2
from flask import Blueprint, Response
from Services.ImageProcessingService import build_stream_frames

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/video_feed')
def video_feed():
    return Response(build_stream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def generate():
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
        
#         if not ret:
#             break

#         # Encode the frame as JPEG
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         if not ret:
#             continue
        
#         # Convert the frame to bytes
#         frame_bytes = jpeg.tobytes()

#         # Yield the frame in the multipart response format
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')