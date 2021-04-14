import utils
import LogOne


def parse_guild():
    fname = utils.filter_from_origin(LogOne.GuildFlow.FILTER_STR)
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if not lo:
                continue

            if lo.gbid == '8444553112797262642':
                print(lo.act_type)
                print(line)


if __name__ == '__main__':
    parse_guild()