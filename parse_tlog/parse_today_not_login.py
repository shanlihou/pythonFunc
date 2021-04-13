import const
import utils
import Filter
import parse_tlog


def parse_today_not_login():
    fname = Filter.Filter.filter_login_log()
    dm = parse_tlog.get_dm(fname)


if __name__ == '__main__':
    parse_today_not_login()