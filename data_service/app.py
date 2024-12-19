from flask import Flask, jsonify
from api.session_manager import session_bp
from api.fetch_historical_data import historical_bp
from api.fetch_realtime_data import realtime_bp
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    # Load configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

    # Register Blueprints
    app.register_blueprint(session_bp, url_prefix="/api/session")
    app.register_blueprint(historical_bp, url_prefix="/api/historical")
    app.register_blueprint(realtime_bp, url_prefix="/api/realtime")

    # Define a root route
    @app.route("/", methods=["GET"])
    def index():
        """
        Root endpoint providing API details.
        """
        return jsonify({
            "message": "Welcome to the AI Trading Data Service API",
            "endpoints": {
                "/api/session": "Session management endpoints",
                "/api/historical": "Historical data fetching endpoints",
                "/api/realtime": "Real-time data fetching endpoints"
            }
        })

    # Error Handlers
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting the AI Trading Data Service API...")

    # Create and run the app
    app = create_app()
    app.run(debug=os.getenv("DEBUG", "True") == "True", host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    