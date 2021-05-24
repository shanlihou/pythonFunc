import attr


@attr.s
class Position(object):
    symbol = attr.ib()
    enter_price = attr.ib()
    mark_price = attr.ib()
    profit = attr.ib()
    side = attr.ib()
    amt = attr.ib()