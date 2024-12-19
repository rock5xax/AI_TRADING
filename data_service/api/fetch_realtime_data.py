from flask import Blueprint, request, jsonify
from services.session_service import SessionService
from services.icici_service import ICICIService
import logging
import os

# Initialize logging
logger = logging.getLogger(__name__)

# Flask Blueprint for real-time data
realtime_bp = Blueprint("realtime", __name__)

# Initialize services
api_key = os.getenv("BREEZE_API_KEY")
api_secret = os.getenv("BREEZE_API_SECRET")

if not api_key or not api_secret:
    raise RuntimeError("BREEZE_API_KEY or BREEZE_API_SECRET environment variables are missing.")

session_service = SessionService(api_key)
icici_service = ICICIService()

@realtime_bp.route("/fetch", methods=["POST"])
def fetch_realtime_data():
    """
    Endpoint to fetch real-time stock market data.
    """
    try:
        data = request.json
        stock_symbol = data.get("stock_symbol")
        exchange_code = data.get("exchange_code", "NSE")

        # Parameter validation
        if not stock_symbol:
            logger.error("Stock symbol is required.")
            return jsonify({"error": "Stock symbol is required"}), 400

        # Generate session token
        session_token = session_service.get_session_token(api_secret)

        # Fetch data
        realtime_data = icici_service.fetch_realtime_data(
            stock_code=stock_symbol,
            exchange_code=exchange_code,
            session_token=session_token
        )

        return jsonify({"data": realtime_data}), 200

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Failed to fetch real-time data"}), 500
