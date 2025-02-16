from flask import Flask
from Endpoints.health import health_routes
from Endpoints.video_streaming import video_routes

app = Flask(__name__)

app.register_blueprint(health_routes, url_prefix="/health")
app.register_blueprint(video_routes, url_prefix='/video')

if __name__ == "__main__":
    app.run(debug=True)