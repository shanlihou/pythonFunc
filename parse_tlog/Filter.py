import os
import LogOne
import const
import utils
import functools
import pickle


class Filter(object):
    def __init__(self, filename, log_class):
        self.filename = filename
        self.inner_openid_set = self.get_openid_info(const.INNER_FILTER_NAME)
        self.outer_openid_set = self.get_openid_info(const.OUT_FILTER_NAME)
        self.basename = os.path.basename(filename)
        self.newdir = os.path.join(const.ROOT_NAME, 'tmp')
        self.log_class = log_class
        try:
            os.mkdir(self.newdir)
        except Exception as e:
            pass

    @classmethod
    @functools.lru_cache(1)
    def get_gbid_2_account_dic(cls):
        tmp_dir = utils.get_dir('tmp')
        save_path = os.path.join(tmp_dir, 'gbid_2_account')
        if os.path.exists(save_path):
            return pickle.load(open(save_path, 'rb'))

        ret_dic = {}

        sec_name = cls.filter_tlog(const.ORI_FILE_NAME, 'SecLogin')
        with open(sec_name) as fr:
            for line in fr:
                lo = LogOne.LogOne.get_log_obj_from_line(line)
                ret_dic[lo.gbid] = lo.account

        pickle.dump(ret_dic, open(save_path, 'wb'))

        return ret_dic

    @staticmethod
    def filter_tlog(filename, filter_str):
        basename = os.path.basename(filename)
        dirname = utils.get_dir('tmp')
        fw_name = os.path.join(dirname, '{}.{}.log'.format(basename, filter_str))
        if os.path.exists(fw_name):
            return fw_name

        fw = open(fw_name, 'w')
        with open(filename, encoding='utf-8') as fr:
            for line in fr:
                if line.startswith(filter_str):
                    fw.write(line)

        fw.close()
        return fw_name

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
                lo = self.log_class.get_log_obj_from_line(line)
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
                lo = self.log_class.get_log_obj_from_line(line)
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
                lo = self.log_class.get_log_obj_from_line(line)
                if lo.account in self.outer_openid_set or lo.account in self.inner_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_by_act(self, actId):
        actId = str(actId)
        fw_name = os.path.join(self.newdir, '{}.{}.log'.format(self.basename, actId))
        fw = open(fw_name, 'w')
        with open(self.filename) as fr:
            for line in fr:
                lo = LogOne.LogVitality.get_log_obj_from_line(line)
                if lo.act != actId:
                    continue

                fw.write(line)

        fw.close()
        return fw_name


if __name__ == '__main__':
    print(Filter.get_gbid_2_account_dic())