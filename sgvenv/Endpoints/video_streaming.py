from flask import Blueprint, Response
from Services.ImageProcessingService import image_stream_loop, stop_stream, is_stream_active

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/video-feed', methods=['GET'])
def video_feed():
    return Response(image_stream_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')

@video_routes.route('/stop-video', methods=['GET'])
def stop_video_feed():
    stop_stream()
    return Response(status=200)

@video_routes.route('/stream-health', methods=['GET'])
def stream_health():
    is_active = is_stream_active()
    
    return Response(str(is_active).lower(), status=200)