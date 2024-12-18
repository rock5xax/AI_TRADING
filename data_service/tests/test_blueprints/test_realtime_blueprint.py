import pytest
from flask import Flask
from api.fetch_realtime_data import realtime_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(realtime_bp, url_prefix="/realtime")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_fetch_realtime_data_success(mocker, client):
    # Mock data
    mocker.patch(
        "api.fetch_realtime_data.session_service.generate_session_token",
        return_value=mocker.Mock(get_quotes=lambda stock_code, exchange_code: {"price": 100}),
    )

    payload = {"stock_symbol": "RELIANCE", "exchange_code": "NSE", "session_token": "dummy_token"}
    response = client.post("/realtime/fetch", json=payload)
    assert response.status_code == 200
    assert response.json["data"]["price"] == 100


def test_fetch_realtime_data_missing_symbol(client):
    payload = {"exchange_code": "NSE", "session_token": "dummy_token"}
    response = client.post("/realtime/fetch", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "Stock symbol is required"
