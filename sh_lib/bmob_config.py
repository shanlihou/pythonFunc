from bmob import BMOB
import json


class BmobConfig(object):
    def __init__(self, config_name, bmob_user_info_file, pri_file, pub_file):
        BMOB(bmob_user_info_file, pri_file, pub_file)
        self.config_name = config_name
        self.object_id = ''
        obj_id, config = self.get_from_remote()
        if not obj_id:
            self.set_default_config()
        else:
            self.object_id = obj_id
            self.config =config

    def get_from_remote(self):
        ret = BMOB().get('config')
        json_data = json.loads(ret)
        if 'error' in json_data:
            return None, None

        for config in json_data['results']:
            if config['name'] == self.config_name:
                object_id = config['objectId']
                config = json.loads(BMOB().big_dec(config['content']))
                return object_id, config

        return None, None

    def get_default_config(self):
        return {}

    def set_default_config(self):
        self.config = self.get_default_config()
        self.save_config_to_remote()

    def save_config_to_remote(self):
        enc_data = BMOB().big_enc(self.config)
        json_str = json.dumps({
            'name': self.config_name,
            'content': enc_data
        })

        if self.object_id:
            BMOB().putData(self.object_id, 'config', json_str)
        else:
            ret = BMOB().addData('config', json_str)
            json_data = json.loads(ret)
            self.object_id = json_data['objectId']

    def test(self):
        pass