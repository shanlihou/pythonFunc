import json
from common import const

import sys
LIB_PATH = r'E:\shgithub\python\pythonFunc\Lib'
if LIB_PATH not in sys.path:
    sys.path.append(LIB_PATH)
import bmob_config


class ConfigManager(bmob_config.BmobConfig):
    def __init__(self):
        super().__init__('binance', 'config/.bmob_user_info.json', const.PRI_FILE, const.PUB_FILE)

    def get_default_config(self):
        return json.load(open(const.DEFAULT_CONFIG))

    def load_config_and_check(self):
        obj_id, config = self.get_from_remote()
        ret = self._check_config_same(config)
        self.config = config
        return ret

    def _check_config_same(self, config):
        st1 = self.config['notify_strategy']
        st2 = config['notify_strategy']
        if len(st1) != len(st2):
            return False

        for k in st1:
            dic1 = st1[k]
            if k not in st2:
                return False

            dic2 = st2[k]
            if not self._check_cmp_dic_same(dic1, dic2):
                return False

        return True

    def _check_cmp_dic_same(self, dic1, dic2):
        return dic1['init_val'] == dic2['init_val'] and\
                dic1['rate'] == dic2['rate'] and\
                dic1['degree'] == dic2['degree']
