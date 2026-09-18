allowed_orders = ("id", "date", "amount", "category", "description")


def validate_order_field(order_field):
    if order_field in allowed_orders:
        return order_field

    raise ValueError("Invalid order criteria")