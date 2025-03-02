from flask import Blueprint, Response
from Services.ImageService import get_latest_drawn_image_bytes
from Services.ImageEvaluationService import predict_image

image_evaluation_routes = Blueprint('image_evaluation_routes', __name__)

@image_evaluation_routes.route('/drawn-image', methods=['GET'])
def drawn_image():
    image_blob = get_latest_drawn_image_bytes()

    return Response(image_blob, mimetype='image/png')

@image_evaluation_routes.route('/evaluate-image', methods=['GET'])
def evaluate_image():
    evaluation_result = predict_image("DrawnImages/drawing_output.png")

    return Response(evaluation_result, content_type='text/plain')
