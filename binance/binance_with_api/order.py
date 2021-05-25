import attr



@attr.s
class Order(object):
    symbol = attr.ib()
    order_id = attr.ib()
    side = attr.ib()
    pos_side = attr.ib()
    price = attr.ib()
    qty = attr.ib()
    type = attr.ib()
    stop_price = attr.ib()
    close_position = attr.ib()

