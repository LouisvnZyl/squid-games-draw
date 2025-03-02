from flask import Flask
from Endpoints.health import health_routes
from Endpoints.video_streaming import video_routes
from Endpoints.image_evaluation import image_evaluation_routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(health_routes, url_prefix="/health")
app.register_blueprint(video_routes, url_prefix='/video')
app.register_blueprint(image_evaluation_routes, url_prefix='/image-processing')

if __name__ == "__main__":
    app.run(debug=True)