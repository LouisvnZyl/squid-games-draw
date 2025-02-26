from flask import Blueprint, Response
from Services.ImageProcessingService import image_stream_loop, stop_stream

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/video-feed', methods=['GET'])
def video_feed():
    return Response(image_stream_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')

@video_routes.route('/stop-video', methods=['POST'])
def stop_video_feed():
    return Response(stop_stream(), status=200)
