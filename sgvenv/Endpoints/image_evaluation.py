from flask import Blueprint, Response
from Services.ImageService import get_latest_drawn_image

image_evaluation_routes = Blueprint('image_evaluation_routes', __name__)

@image_evaluation_routes.route('/drawn-image', methods=['GET'])
def drawn_image():
    image_blob = get_latest_drawn_image()

    return Response(image_blob, mimetype='image/png')
