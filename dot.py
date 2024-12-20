from breeze_strategies import Strategies
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch configuration from .env
app_key = os.getenv('APP_KEY')
secret_key = os.getenv('SECRET_KEY')
api_session = os.getenv('API_SESSION')
max_profit = os.getenv('MAX_PROFIT', "10000")  # Default max profit
max_loss = os.getenv('MAX_LOSS', "5000")      # Default max loss

# Initialize the Strategies object
try:
    obj = Strategies(
        app_key=app_key,
        secret_key=secret_key,
        api_session=api_session,
        max_profit=max_profit,
        max_loss=max_loss
    )
    print("Strategy object initialized successfully.")
except Exception as e:
    print(f"Error initializing Strategies object: {e}")

# Define helper functions for various strategies
def execute_straddle():
    try:
        obj.straddle(
            strategy_type="long",
            stock_code="NIFTY",
            strike_price="18700",
            quantity="50",
            expiry_date="2023-06-29T06:00:00.000Z"
        )
        print("Straddle strategy executed successfully.")
    except Exception as e:
        print(f"Error executing straddle strategy: {e}")

def execute_strangle():
    try:
        obj.strangle(
            strike_price_call="18700",
            strike_price_put="18300",
            strategy_type="long",
            stock_code="NIFTY",
            quantity="50",
            expiry_date="2023-06-29T06:00:00.000Z"
        )
        print("Strangle strategy executed successfully.")
    except Exception as e:
        print(f"Error executing strangle strategy: {e}")

def execute_single_leg():
    try:
        obj.single_leg(
            right="Call",
            strategy_type="short",
            stock_code="NIFTY",
            strike_price="18700",
            quantity="50",
            expiry_date="2023-06-29T06:00:00.000Z"
        )
        print("Single leg strategy executed successfully.")
    except Exception as e:
        print(f"Error executing single leg strategy: {e}")

def execute_four_leg(stock_code, quantity, expiry_date, call_short_strike, put_short_strike, call_long_strike, put_long_strike):
    try:
        obj.four_leg(
            stock_code=stock_code,
            quantity=quantity,
            expiry_date=expiry_date,
            call_short_strike=call_short_strike,
            put_short_strike=put_short_strike,
            call_long_strike=call_long_strike,
            put_long_strike=put_long_strike
        )
        print(f"Four leg strategy for {stock_code} executed successfully.")
    except Exception as e:
        print(f"Error executing four leg strategy for {stock_code}: {e}")

# Execute strategies as examples
execute_straddle()
execute_strangle()
execute_single_leg()

# Execute four leg strategies
execute_four_leg("NIFTY", "25", "2024-08-14T06:00:00.000Z", "24900", "23000", "24850", "23050")
execute_four_leg("CNXBAN", "15", "2024-08-14T06:00:00.000Z", "52600", "47600", "52700", "47900")

# Stop all strategies
def stop_all_strategies():
    try:
        obj.stop()
        obj.stop_strategy(is_strangle=True)
        obj.stop_strategy(single_leg=True)
        obj.stop_strategy(is_FourLeg=True)
        print("All strategies stopped successfully.")
    except Exception as e:
        print(f"Error stopping strategies: {e}")

stop_all_strategies()

# Generate Profit & Loss report
def generate_pnl():
    try:
        pnl = obj.get_pnl()
        print("Profit & Loss report generated successfully:")
        print(pnl)
    except Exception as e:
        print(f"Error generating Profit & Loss report: {e}")

generate_pnl()
