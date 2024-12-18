from flask import Blueprint, request, jsonify
from services.session_service import SessionService
from services.icici_service import ICICIService
import os

# Flask Blueprint for real-time data
realtime_bp = Blueprint("realtime", __name__)

# Load API credentials from environment variables
api_key = os.getenv("BREEZE_API_KEY")
api_secret = os.getenv("BREEZE_API_SECRET")

if not api_key or not api_secret:
    raise RuntimeError("Missing BREEZE_API_KEY or BREEZE_API_SECRET environment variables.")

# Initialize services
session_service = SessionService(api_key)
icici_service = ICICIService()

@realtime_bp.route("/fetch", methods=["POST"])
def fetch_realtime_data():
    """
    Endpoint to fetch real-time stock market data.
    Request Body:
        - stock_symbol (str): The stock symbol (e.g., "RELIANCE").
        - exchange_code (str): The exchange code (default: "NSE").
    Returns:
        - Real-time market data in JSON format.
    """
    data = request.json
    stock_symbol = data.get("stock_symbol")
    exchange_code = data.get("exchange_code", "NSE")

    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        # Generate a session token
        session_token = session_service.get_session_token(api_secret)

        # Fetch real-time data using ICICIService
        realtime_data = icici_service.fetch_realtime_data(
            stock_code=stock_symbol,
            exchange_code=exchange_code,
            session_token=session_token
        )

        return jsonify({"data": realtime_data}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
