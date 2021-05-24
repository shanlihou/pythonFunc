import sys
from common import sh_log

from binance_with_api import auto_trader


def main():
    at = auto_trader.AutoTrader()
    at.run()

if __name__ == '__main__':
    main()