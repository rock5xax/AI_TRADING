import requests

def fetch_historical_data(start_date, end_date, symbol):
    url = "https://api.breeze.broker/historical"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "symbol": symbol
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()  # Assuming JSON response
