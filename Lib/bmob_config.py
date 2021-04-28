from bmob import BMOB
import json


class BmobConfig(object):
    def __init__(self, config_name, pri_file, pub_file):
        BMOB(pri_file, pub_file)
        self.config_name = config_name
        self.object_id = ''
        if not self.load_from_remote():
            self.set_default_config()

    def _parse_config(self, json_data):
        for config in json_data['results']:
            if config['name'] == self.config_name:
                self.object_id = config['objectId']
                self.load_config(config['content'])
                return True

        return False

    def load_from_remote(self):
        ret = BMOB().get('config')
        json_data = json.loads(ret)
        if 'error' in json_data:
            return False
        elif not self._parse_config(json_data):
            return False

        return True

    def load_config(self, enc_data):
        self.config = json.loads(BMOB().decrypt(enc_data))

    def set_default_config(self):
        self.config = {}
        self.save_config_to_remote()

    def save_config_to_remote(self):
        enc_data = BMOB().encrypt(json.dumps(self.config))
        json_str = json.dumps({
            'name': self.config_name,
            'content': enc_data
        })

        if self.object_id:
            BMOB().putData(self.object_id, 'config', json_str)
        else:
            BMOB().addData('config', json_str)

    def test(self):
        pass