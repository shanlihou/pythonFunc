import attr
import time


class KLines(object):

    def __init__(self, open_time, open_rice, max_rice, min_rice, end_rice, deal_amount, end_time, deal_rice, deal_num, active_buy_amount, active_buy_rice, ignore):
        self.open_time = open_time // 1000
        self.open_rice = float(open_rice)
        self.max_rice = float(max_rice)
        self.min_rice = float(min_rice)
        self.end_rice = float(end_rice)
        self.deal_amount = float(deal_amount)
        self.end_time = end_time // 1000
        self.deal_rice = float(deal_rice)
        self.deal_num = int(deal_num)
        self.active_buy_amount = float(active_buy_amount)
        self.active_buy_rice = float(active_buy_rice)

    def __str__(self):
        t_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.open_time))
        return f'start:{t_start}, max:{self.max_rice}, min:{self.min_rice}, end:{self.end_rice}, diff:{self.end_rice - self.open_rice}, open:{self.open_rice}'
