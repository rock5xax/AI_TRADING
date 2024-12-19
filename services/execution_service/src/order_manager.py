from .breeze_connector import initialize_breeze

def place_order(stock_code, quantity, order_type, price=None):
    breeze = initialize_breeze()
    order = breeze.place_order(
        stock_code=stock_code,
        quantity=quantity,
        order_type=order_type,
        price=price
    )
    return order
