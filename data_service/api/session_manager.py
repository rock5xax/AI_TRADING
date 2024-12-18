from flask import Blueprint, request, jsonify
from services.session_service import SessionService
import os

# Flask Blueprint for session management
session_bp = Blueprint("session", __name__)

# Load API credentials from environment variables
api_key = os.getenv("BREEZE_API_KEY")
api_secret = os.getenv("BREEZE_API_SECRET")

# Initialize SessionService
session_service = SessionService(api_key)

@session_bp.route("/generate-session", methods=["POST"])
def generate_session():
    """
    Endpoint to generate a session token for the Breeze API.
    """
    session_token = request.json.get("session_token")
    if not session_token:
        return jsonify({"error": "Session token is required"}), 400

    try:
        session = session_service.generate_session_token(api_secret, session_token)
        return jsonify({"message": "Session generated successfully", "session": session.session_token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
