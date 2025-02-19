from flask import Blueprint, Response
from Services.ImageProcessingService import image_stream_loop

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/video_feed')
def video_feed():
    return Response(image_stream_loop(), mimetype='multipart/x-mixed-replace; boundary=frame')
