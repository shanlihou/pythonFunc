import os
import LogOne


class Filter(object):
    def __init__(self, filename, inner_file_name, outer_file_name):
        self.filename = filename
        self.inner_openid_set = self.get_openid_info(inner_file_name)
        self.outer_openid_set = self.get_openid_info(outer_file_name)
        self.basename = os.path.basename(filename)
        self.dirname = os.path.dirname(filename)
        self.newdir = os.path.join(self.dirname, 'tmp')
        try:
            os.mkdir(self.newdir)
        except Exception as e:
            pass

    @staticmethod
    def filter_tlog(filename, filter_str):
        fw = open(filename + '.{}.log'.format(filter_str), 'w')
        with open(filename, encoding='utf-8') as fr:
            for line in fr:
                if line.startswith(filter_str):
                    fw.write(line)

    def get_openid_info(self, filename):
        openid_set = set()
        with open(filename, encoding='utf-8') as fr:
            for line in fr:
                if ' ' in line:
                    tup = line.strip().split(' ')
                else:
                    tup = line.strip().split('\t')

#                 print(tup)
                if len(tup) > 2:
                    openid_set.add(tup[2])

        return openid_set

    def filter_inner(self):
        fw_name = '{}\\{}.{}.log'.format(self.newdir, self.basename, 'inner')

        fw = open(fw_name, 'w')
        with open(self.filename) as fr:
            for line in fr:
                lo = LogOne.LogOne.get_log_obj_from_line(line)
                if lo.account not in self.inner_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_out_first(self):
        fw_name = '{}\\{}.{}.log'.format(
            self.newdir, self.basename, 'out_first')
        fw = open(fw_name, 'w')
        with open(self.filename) as fr:
            for line in fr:
                lo = LogOne.LogOne.get_log_obj_from_line(line)
                if lo.account not in self.outer_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_out_second(self):
        fw_name = '{}\\{}.{}.log'.format(
            self.newdir, self.basename, 'out_second')
        fw = open(fw_name, 'w')
        with open(self.filename) as fr:
            for line in fr:
                lo = LogOne.LogOne.get_log_obj_from_line(line)
                if lo.account in self.outer_openid_set or lo.account in self.inner_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_guild_bandit(self)

