import sys
from common import sh_log

from binance_with_api import auto_trader


def main():
    at = auto_trader.AutoTrader()
    if len(sys.argv) == 2:
        if sys.argv[1] == 'test':
            at.test()
        else:
            at.run()

if __name__ == '__main__':
    main()