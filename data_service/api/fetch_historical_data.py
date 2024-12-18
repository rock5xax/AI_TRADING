from flask import Blueprint, request, jsonify
from services.session_service import SessionService
from services.icici_service import ICICIService
import os

# Flask Blueprint for historical data
historical_bp = Blueprint("historical", __name__)
icici_service = ICICIService()

# Load API credentials from environment variables
api_key = os.getenv("BREEZE_API_KEY")
api_secret = os.getenv("BREEZE_API_SECRET")

# Initialize the SessionService
session_service = SessionService(api_key)

@historical_bp.route("/fetch", methods=["POST"])
def fetch_historical_data():
    data = request.json
    stock_code = data.get("stock_code")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([stock_code, start_date, end_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        historical_data = icici_service.fetch_historical_data(stock_code, start_date, end_date)
        return jsonify({"data": historical_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500