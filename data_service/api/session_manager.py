from flask import Blueprint, request, jsonify
from services.session_service import SessionService
import logging
import os

# Initialize logging
logger = logging.getLogger(__name__)

# Flask Blueprint for session management
session_bp = Blueprint("session", __name__)

# Initialize SessionService
api_key = os.getenv("BREEZE_API_KEY")
api_secret = os.getenv("BREEZE_API_SECRET")

if not api_key or not api_secret:
    raise RuntimeError("Missing API credentials in environment variables.")

session_service = SessionService(api_key)

@session_bp.route("/generate-session", methods=["POST"])
def generate_session():
    """
    Endpoint to generate a session token for the Breeze API.
    """
    try:
        session_token = request.json.get("session_token")
        if not session_token:
            logger.error("Session token is required.")
            return jsonify({"error": "Session token is required"}), 400

        # Generate the session
        session = session_service.generate_session_token(api_secret, session_token)
        logger.info("Session generated successfully.")
        return jsonify({"message": "Session generated successfully", "session": session.session_token}), 200

    except Exception as e:
        logger.error(f"Error generating session: {e}")
        return jsonify({"error": "Failed to generate session"}), 500
