from breeze_connect import BreezeConnect

class ICICIBrokerAPI:
    def __init__(self, api_key, session_token):
        self.client = BreezeConnect(api_key=api_key)
        self.client.generate_session(api_secret="your_api_secret", session_token=session_token)

    def get_historical_data(self, stock_code, start_date, end_date):
        response = self.client.get_historical_data(
            interval="1day",
            from_date=start_date,
            to_date=end_date,
            stock_code=stock_code,
            exchange_code="NSE"
        )
        return response

# Usage
api_key = "your_api_key"
session_token = "your_session_key"
broker_api = ICICIBrokerAPI(api_key, session_token)
data = broker_api.get_historical_data("RELIANCE", "2023-01-01", "2023-12-31")
