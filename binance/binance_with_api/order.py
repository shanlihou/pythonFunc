from os import stat
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

    @classmethod
    def from_order(cls, oriOrder):
        return cls(
            oriOrder.symbol,
            oriOrder.orderId,
            oriOrder.side,
            oriOrder.positionSide,
            oriOrder.price,
            oriOrder.origQty,
            oriOrder.type,
            oriOrder.stopPrice,
            oriOrder.closePosition,
        )
