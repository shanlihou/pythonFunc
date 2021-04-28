import json
from common import const

import sys
LIB_PATH = r'E:\shgithub\python\pythonFunc\Lib'
if LIB_PATH not in sys.path:
    sys.path.append(LIB_PATH)
import bmob_config


class ConfigManager(bmob_config.BmobConfig):
    def __init__(self):
        super().__init__('binance', const.PRI_FILE, const.PUB_FILE)
        print(self.config)
        if not self.config:
            self.config = json.load(open(const.DEFAULT_CONFIG))
            self.save_config_to_remote()

