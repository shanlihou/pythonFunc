import re
import utils


class GuildBattle(object):
    def __init__(self, filename):
        self.gbid_set = set()
        self.account_set = set()
        self.day = 0
        self.init_data(filename)

    def parse_day(self, line):
        pat = re.compile(r'\[\d+\-\d+\-(\d+)')
        find = pat.search(line)
        if find:
            day = int(find.group(1))
            self.day = day

    def init_data(self, filename):
        pat = re.compile(r'gbId\:([^,]+), kill\:')
        with open(filename, encoding='utf-8') as fr:
            for line in fr:
                find = pat.search(line)
                if find:
                    gbid = int(find.group(1))
                    if utils.is_gbid_inter(gbid):
                        continue

                    self.gbid_set.add(gbid)

                    account = utils.get_account(gbid)
                    self.account_set.add(account)
                else:
                    self.parse_day(line)

    def generate_col(self, day_dict):
        login_account_num = day_dict.get(self.day)
        col = []
        col.append(self.day)
        col.append(len(self.gbid_set))

        account_num = len(self.account_set)
        col.append(account_num)
        col.append(account_num / login_account_num)
        return col


def deal_guild_battle(filename, day_dict):
    gb = GuildBattle(filename)
    return gb.generate_col(day_dict)


if __name__ == '__main__':
    deal_guild_battle()
