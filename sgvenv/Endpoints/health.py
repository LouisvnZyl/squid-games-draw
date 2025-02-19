from flask import Blueprint, jsonify

health_routes = Blueprint('health_routes', __name__)

@health_routes.route('/', methods=['GET'])
def check_health():
    return jsonify({"Status": "Good"})