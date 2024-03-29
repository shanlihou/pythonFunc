import os
import LogOne
import const
import utils
import functools
import pickle


class Filter(object):

    def __init__(self, filename, log_class):
        self.filename = filename
        self.inner_openid_set = utils.get_openid_info(const.INNER_FILTER_NAME)
        # self.outer_openid_set = utils.get_openid_info(const.OUT_FILTER_NAME)
        self.basename = os.path.basename(filename)
        self.newdir = os.path.join(const.ROOT_NAME, 'tmp')
        try:
            os.mkdir(self.newdir)
        except Exception as e:
            pass

    @staticmethod
    def filter_guild_train():
        tmp_dir = utils.get_dir('tmp')
        fw_name = os.path.join(tmp_dir, 'guild_train_tlog.log')
        if os.path.exists(fw_name):
            return fw_name

        fw = utils.utf8_open(fw_name, 'w')
        for line in utils.get_origin_line_stream():
            if 'guild train upgrade' in line and line.startswith('LOG_GUILD_CONTRIBUTION'):
                fw.write(line)

        fw.close()
        return fw_name

    @staticmethod
    def filter_login_log():
        dirname = utils.get_dir('tmp')
        fw_name = utils.get_out_name('tmp', 'log_in_and_out.log')
        if os.path.exists(fw_name):
            return fw_name

        fw = utils.utf8_open(fw_name, 'w', encoding='utf-8')
        for line in utils.get_origin_line_stream():
            if not (line.startswith('SecLogin') or line.startswith('SecLogout')):
                continue

            fw.write(line)

        fw.close()
        return fw_name

    def filter_inner(self):
        fw_name = '{}\\{}.{}.log'.format(self.newdir, self.basename, 'inner')

        fw = utils.utf8_open(fw_name, 'w', encoding='utf-8')
        with utils.utf8_open(self.filename, encoding='utf-8') as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                if not lo:
                    continue

                if lo.account not in self.inner_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_out_first(self):
        fw_name = '{}\\{}.{}.log'.format(
            self.newdir, self.basename, 'out_first')
        fw = utils.utf8_open(fw_name, 'w')
        with utils.utf8_open(self.filename) as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                if not lo:
                    continue

                if lo.account not in self.outer_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_out(self):
        fw_name = '{}\\{}.{}.log'.format(
            self.newdir, self.basename, 'outter')
        fw = utils.utf8_open(fw_name, 'w', encoding='utf-8')
        with utils.utf8_open(self.filename, encoding='utf-8') as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                if not lo:
                    continue

                if lo.account in self.inner_openid_set:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    def filter_by_act(self, battle_type):
        battle_type = str(battle_type)
        fw_name = os.path.join(self.newdir, '{}.{}.log'.format(self.basename, battle_type))
        if os.path.exists(fw_name):
            return fw_name

        fw = utils.utf8_open(fw_name, 'w')
        with utils.utf8_open(self.filename, encoding='utf-8') as fr:
            for line in fr:
                lo = LogOne.RoundFlow.get_log_obj_from_line(line)
                if not lo:
                    print('error1:', line)
                    continue

                if lo.battle_type != battle_type:
                    continue

                fw.write(line)

        fw.close()
        return fw_name

    @staticmethod
    def filter_sys_log(tag_name):
        new_dir = utils.get_dir('tmp')
        basename = os.path.basename(const.SYS_LOG_NAME)
        fw_name = os.path.join(new_dir, '{}.{}.log'.format(basename, tag_name))
        fw = utils.utf8_open(fw_name, 'w')
        with utils.utf8_open(const.SYS_LOG_NAME, encoding='utf-8') as fr:
            for line in fr:
                if tag_name in line:
                    fw.write(line)

        fw.close()
        return fw_name


if __name__ == '__main__':
    print(utils.get_gbid_2_account_dic())
