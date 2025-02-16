from flask import Flask
from Endpoints.health import health_routes

app = Flask(__name__)

app.register_blueprint(health_routes, url_prefix="/health")

if __name__ == "__main__":
    app.run(debug=True)