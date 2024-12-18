from flask import Flask, jsonify
from api.session_manager import session_bp
from api.fetch_historical_data import historical_bp
from api.fetch_realtime_data import realtime_bp
import os

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    # Load configuration from environment variables or default
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

    # Register Blueprints
    app.register_blueprint(session_bp, url_prefix="/api/session")
    app.register_blueprint(historical_bp, url_prefix="/api/historical")
    app.register_blueprint(realtime_bp, url_prefix="/api/realtime")

    # Define a root route
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "message": "Welcome to the AI Trading Data Service API",
            "endpoints": {
                "/api/session": "Session management endpoints",
                "/api/historical": "Historical data fetching endpoints",
                "/api/realtime": "Real-time data fetching endpoints"
            }
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

