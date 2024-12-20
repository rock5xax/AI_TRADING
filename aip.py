import enum
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Breeze API BASE URL
API_URL = "https://api.icicidirect.com/breezeapi/api/v1/"

# Breeze New Endpoint
BREEZE_NEW_URL = "https://breezeapi.icicidirect.com/api/v2/"

# Live Feeds URL
LIVE_FEEDS_URL = "https://livefeeds.icicidirect.com"

# Live Streams URL
LIVE_STREAM_URL = "https://livestream.icicidirect.com"

# Live OHLC Stream URL
LIVE_OHLC_STREAM_URL = "https://breezeapi.icicidirect.com"

# Security Master Download Link 
SECURITY_MASTER_URL = "https://directlink.icicidirect.com/NewSecurityMaster/SecurityMaster.zip"

# Stock Script Code Download Link
STOCK_SCRIPT_CSV_URL = "https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv"

# API Methods
class APIRequestType(enum.Enum):

    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

    def __str__(self):
        return str(self.value)

# API Endpoints
class APIEndPoint(enum.Enum):

    CUST_DETAILS = "customerdetails"
    DEMAT_HOLDING = "dematholdings"
    FUND = "funds"
    HIST_CHART = "historicalcharts"
    MARGIN = "margin"
    ORDER = "order"
    PORTFOLIO_HOLDING = "portfolioholdings"
    PORTFOLIO_POSITION = "portfoliopositions"
    QUOTE = "quotes"
    TRADE = "trades"
    OPT_CHAIN = "optionchain"
    SQUARE_OFF = "squareoff"
    LIMIT_CALCULATOR = "fnolmtpriceandqtycal"
    MARGIN_CALCULATOR = "margincalculator"
    
    def __str__(self):
        return str(self.value)

# TUX Mapping
TUX_TO_USER_MAP = {
    "orderFlow": {
        "B": "Buy",
        "S": "Sell",
        "N": "NA"
    },
    "limitMarketFlag": {
        "L": "Limit",
        "M": "Market",
        "S": "StopLoss"
    },
    "orderType": {
        "T": "Day",
        "I": "IoC",
        "V": "VTC"
    },
    "productType": {
        "F": "Futures",
        "O": "Options",
        "P": "FuturePlus",
        "U": "FuturePlus_sltp",
        "I": "OptionPlus",
        "C": "Cash",
        "Y": "eATM",
        "B": "BTST",
        "M": "Margin",
        "T": "MarginPlus"
    },
    "orderStatus": {
        "A": "All",
        "R": "Requested",
        "Q": "Queued",
        "O": "Ordered",
        "P": "Partially Executed",
        "E": "Executed",
        "J": "Rejected",
        "X": "Expired",
        "B": "Partially Executed And Expired",
        "D": "Partially Executed And Cancelled",
        "F": "Freezed",
        "C": "Cancelled"
    },
    "optionType": {
        "C": "Call",
        "P": "Put",
        "*": "Others"
    },
}

# Response Messages
class ResponseMessage(enum.Enum):

    # Currency not allowed
    CURRENCY_NOT_ALLOWED = "NDX as Exchange-Code not allowed"

    # Empty Details Errors
    BLANK_EXCHANGE_CODE = "Exchange-Code cannot be empty"
    BLANK_STOCK_CODE = "Stock-Code cannot be empty"
    BLANK_PRODUCT_TYPE = "Product cannot be empty"
    BLANK_PRODUCT_TYPE_NFO = "Product-type cannot be empty for Exchange-Code 'nfo'"
    BLANK_PRODUCT_TYPE_BFO = "Product-type cannot be empty for Exchange-Code 'bfo'"
    BLANK_PRODUCT_TYPE_NFO_BFO = "Product-type cannot be empty for Exchange-Code 'nfo' or 'bfo'"
    BLANK_PRODUCT_TYPE_HIST_V2 = "Product-type cannot be empty for Exchange-Code 'nfo','ndx', 'mcx' or 'bfo'"
    BLANK_ACTION = "Action cannot be empty"
    BLANK_ORDER_TYPE = "Order-type cannot be empty"
    BLANK_QUANTITY = "Quantity cannot be empty"
    BLANK_LOTS = "Lots cannot be empty"
    BLANK_VALIDITY = "Validity cannot be empty"
    BLANK_ORDER_ID = "Order-Id cannot be empty"
    BLANK_FROM_DATE = "From-Date cannot be empty"
    BLANK_TO_DATE = "To-Date cannot be empty"
    BLANK_TRANSACTION_TYPE = "Transaction-Type cannot be empty"
    BLANK_AMOUNT = "Amount cannot be empty"
    BLANK_SEGMENT = "Segment cannot be empty"
    BLANK_INTERVAL = "Interval cannot be empty"
    BLANK_STRIKE_PRICE = "Strike-Price cannot be empty for Product-Type 'options'"
    BLANK_EXPIRY_DATE = "Expiry-Date cannot be empty for exchange-code 'nfo'"
    BLANK_RIGHT_STRIKE_PRICE = "Either Right or Strike-Price cannot be empty."
    BLANK_RIGHT_EXPIRY_DATE = "Either Expiry-Date or Right cannot be empty."
    BLANK_EXPIRY_DATE_STRIKE_PRICE = "Either Expiry-Date or Strike-Price cannot be empty."

    # Validation Errors
    EXCHANGE_CODE_ERROR = "Exchange-Code should be either 'nse', or 'nfo' or 'ndx' or 'mcx'"
    EXCHANGE_CODE_HIST_V2_ERROR = "Exchange-Code should be either 'nse', 'bse' ,'nfo', 'ndx', 'mcx' or 'bfo'"
    PRODUCT_TYPE_ERROR = "Product should be either 'futures', 'options', 'futureplus', 'optionplus', 'cash', 'eatm','btst','mtf' or 'margin'"
    PRODUCT_TYPE_ERROR_NFO_BFO = "Product-type should be either 'futures', 'options', 'futureplus', or 'optionplus' for Exchange-Code 'NFO' or 'BFO'"
    PRODUCT_TYPE_ERROR_HIST_V2 = "Product-type should be either 'futures', 'options' for Exchange-Code 'NFO','NDX', 'MCX' or 'BFO'"
    ACTION_TYPE_ERROR = "Action should be either 'buy', or 'sell'"
    ORDER_TYPE_ERROR = "Order-type should be either 'limit', 'market', or 'stoploss'"
    VALIDITY_TYPE_ERROR = "Validity should be either 'day', 'ioc', or 'vtc'"
    RIGHT_TYPE_ERROR = "Right should be either 'call', 'put', or 'others'"
    TRANSACTION_TYPE_ERROR = "Transaction-Type should be either 'debit' or 'credit'"
    ZERO_AMOUNT_ERROR = "Amount should be more than 0"
    AMOUNT_DIGIT_ERROR = "Amount should only contain digits"
    INTERVAL_TYPE_ERROR = "Interval should be either '1minute', '5minute', '30minute', or '1day'"
    INTERVAL_TYPE_ERROR_HIST_V2 = "Interval should be either '1second','1minute', '5minute', '30minute', or '1day'"
    API_SESSION_ERROR = "API Session cannot be empty"
    OPT_CHAIN_EXCH_CODE_ERROR = "Exchange code should be nfo or bfo"
    NFO_FIELDS_MISSING_ERROR = "At least two inputs are required out of Expiry-Date, Right & Strike-Price. All three cannot be empty."
    UNDER_LYING_ERROR = "Underlying cannot be empty"
    ORDER_FLOW = "Order flow cannot be empty"
    STOP_LOSS_TRIGGER = "Stop loss trigger cannot be empty"
    OPTION_TYPE = "Option type cannot be empty, it's either CALL or PUT"
    SOURCE_FLAG = "Source flag cannot be empty, it should be either P or M"
    MARKET_TYPE = "Market type cannot be empty"
    FRESH_ORDER_LIMIT = "Fresh order limit cannot be empty"

    # Socket Connectivity Response
    RATE_REFRESH_NOT_CONNECTED = "Socket server is not connected to rate refresh."
    RATE_REFRESH_DISCONNECTED = "Socket server for rate refresh has been disconnected."
    ORDER_REFRESH_NOT_CONNECTED = "Socket server is not connected to order refresh."
    ORDER_REFRESH_DISCONNECTED = "Socket server for order streaming has been disconnected."
    ORDER_NOTIFICATION_SUBSCRIBED = "Order Notification subscribed successfully"
    OHLCV_STREAM_NOT_CONNECTED = "Socket server is not connected to OHLCV Stream."
    OHLCV_STREAM_DISCONNECTED = "Socket server for OHLCV Streaming has been disconnected."
    STRATEGY_STREAM_SUBSCRIBED = "{0} streaming subscribed successfully."
    STRATEGY_STREAM_DISCONNECTED = "Strategy stream disconnected."
    STRATEGY_STREAM_NOT_CONNECTED = "Socket server is not connected to strategy streaming."
    STRATEGY_STREAM_UNSUBSCRIBED = "{0} streaming unsubscribed successfully."

    # Stock Subscription Message
    STOCK_SUBSCRIBE_MESSAGE = "Stock {0} subscribed successfully"
    STOCK_UNSUBSCRIBE_MESSAGE = "Stock {0} unsubscribed successfully"

    def __str__(self):
        return str(self.value)

# Exception Messages
class ExceptionMessage(enum.Enum):
    AUTHENICATION_EXCEPTION = "Could not authenticate credentials. Please check token and keys"
    STOCK_CODE_EXCEPTION = "Stock-Code cannot be empty."
    PRODUCT_TYPE_EXCEPTION = "Product-Type should either be Futures or Options for given Exchange-Code."

    def __str__(self):
        return str(self.value)

# Type Lists for Validation
INTERVAL_TYPES = ["1minute", "5minute", "30minute", "1day"]
PRODUCT_TYPES = ["futures", "options", "futureplus", "optionplus", "cash", "eatm", "margin", "mtf", "btst"]
ACTION_TYPES = ["buy", "sell"]
ORDER_TYPES = ["limit", "market", "stoploss"]
VALIDITY_TYPES = ["day", "ioc", "vtc"]

# Utility Functions
class APIUtils:
    @staticmethod
    def validate_request_params(params, required_fields):
        """
        Validate if all required fields are present in the parameters.
        """
        missing_fields = [field for field in required_fields if field not in params or not params[field]]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    @staticmethod
    def map_tux_to_user(response, mapping):
        """
        Map TUX-specific response fields to user-friendly formats.
        """
        return {key: mapping[key].get(value, value) for key, value in response.items() if key in mapping}

# Example Usage
if __name__ == "__main__":
    try:
        # Example: Validate API parameters
        request_params = {"exchangeCode": "nse", "stockCode": "RELIANCE"}
        required_fields = ["exchangeCode", "stockCode", "productType"]
        APIUtils.validate_request_params(request_params, required_fields)
    except ValueError as e:
        logger.error(f"Validation Error: {e}")

    try:
        # Example: Map TUX response
        tux_response = {"orderFlow": "B", "limitMarketFlag": "L"}
        mapped_response = APIUtils.map_tux_to_user(tux_response, TUX_TO_USER_MAP)
        logger.info(f"Mapped Response: {mapped_response}")
    except Exception as e:
        logger.error(f"Error in mapping response: {e}")
