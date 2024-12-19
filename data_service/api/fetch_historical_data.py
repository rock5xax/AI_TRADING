from flask import Blueprint, request, jsonify
from services.icici_service import ICICIService
import logging
import os

# Initialize logging
logger = logging.getLogger(__name__)

# Flask Blueprint for historical data
historical_bp = Blueprint("historical", __name__)
icici_service = ICICIService()

@historical_bp.route("/fetch", methods=["POST"])
def fetch_historical_data():
    """
    Endpoint to fetch historical stock data.
    """
    try:
        data = request.json
        stock_code = data.get("stock_code")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Parameter validation
        if not all([stock_code, start_date, end_date]):
            logger.error("Missing required parameters.")
            return jsonify({"error": "Missing required parameters"}), 400

        # Fetch data
        historical_data = icici_service.fetch_historical_data(stock_code, start_date, end_date)
        return jsonify({"data": historical_data}), 200

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        return jsonify({"error": "Failed to fetch historical data"}), 500
