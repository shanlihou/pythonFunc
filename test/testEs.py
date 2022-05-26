# coding=utf-8
import requests
import base64
import json

URI_BASE = 'http://{}:{}'.format('192.168.16.252', 9200)
ori = 'elastic:123456'
authB64 = base64.b64encode(bytes(ori, 'ascii'))
INDEX = '20308_friend_ik'
# INDEX = '20104_friend_ik'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic %s' % authB64.decode('ascii'),
}

INIT_STR = '''{
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "gbId": {
                "type": "long"
            }
        }
    }
}'''


class EsTest(object):
    headers = {
        'Authorization': 'Basic %s' % authB64.decode('ascii')
    }

    def __init__(self):
        pass

    def getPluginInfo(self):
        url = '{}/{}/{}'.format(URI_BASE, '_cat', 'plugins')
        ret = requests.get(url, headers=self.headers)
        print(ret.text)

    def del_index(self, index_name):
        url = '{}/{}'.format(URI_BASE, index_name)
        ret = requests.delete(url, headers=self.headers)
        print(ret.text)

    def set_block_not_read_only(self):
        data = {
            "index": {
                "blocks": {
                    "read_only_allow_delete": "false"
                }
            }
        }
        data = json.dumps(data)
        url = '{}/{}'.format(URI_BASE, '_settings')

        ret = requests.put(url, data=data, headers=HEADERS)
        print('set not read only', ret.text)

    def update_flood_stage(self):
        data = {
            "transient": {
                "cluster.routing.allocation.disk.watermark.low": "85%",
                "cluster.routing.allocation.disk.watermark.high": "90%",
                "cluster.routing.allocation.disk.watermark.flood_stage": "99%",
            }
        }

        data = json.dumps(data)
        url = f'{URI_BASE}/_cluster/settings'
        ret = requests.put(url, data=data, headers=HEADERS)
        print('update flood:', ret.text)

    def create_index(self, index_name):
        url = '{}/{}'.format(URI_BASE, index_name)
        data = json.loads(INIT_STR)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % authB64.decode('ascii'),
        }
        print(headers)
        ret = requests.put(url, data=INIT_STR, headers=headers)
        print(ret.text)

    def get_indexes(self):
        url = '{}/{}/{}'.format(URI_BASE, '_cat', 'indices?v')
        ret = requests.get(url, headers=self.headers)
        return ret.text

    def check_index_ok(self, index_name):
        url = '{}/{}'.format(URI_BASE, index_name)
        ret = requests.get(url, headers=self.headers)
        data = json.loads(ret.text)
        try:
            ret = data[index_name]['mappings']['properties']['name']['analyzer'] == 'ik_max_word'
            return ret
        except Exception as e:
            return False

    def error(self):
        err_str = {'error': {'root_cause': [{'type': 'index_not_found_exception', 'reason': 'no such index [20217_friend_ik]', 'resource.type': 'index_or_alias', 'resource.id': '20217_friend_ik', 'index_uuid': '_na_', 'index': '20217_friend_ik'}],
                             'type': 'index_not_found_exception', 'reason': 'no such index [20217_friend_ik]', 'resource.type': 'index_or_alias', 'resource.id': '20217_friend_ik', 'index_uuid': '_na_', 'index': '20217_friend_ik'}, 'status': 404}

    def ok(self):
        ok_dict = {'20217_friend_ik': {'aliases': {}, 'mappings': {'properties': {'gbId': {'type': 'long'}, 'name': {'type': 'text', 'analyzer': 'ik_max_word'}}}, 'settings': {'index': {
            'creation_date': '1605497657299', 'number_of_shards': '1', 'number_of_replicas': '1', 'uuid': 'UU7RhBbMTZ2RlGlorEwsbw', 'version': {'created': '7050199'}, 'provided_name': '20217_friend_ik'}}}}
        ret = ok_dict['20217_friend_ik']['mappings']['properties']['name']['analyzer']
        print(ret)

    def fix_index(self, index_name):
        #         self.del_index(index_name)
        self.create_index(index_name)

    def ana(self, name):
        url = '{}/{}/{}'.format(URI_BASE, INDEX, '_analyze')
        data = {'field': 'name',
                'text': name}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % authB64.decode('ascii'),
        }
        ret = requests.post(url, data=json.dumps(data), headers=headers)
        print(ret.text)

    @staticmethod
    def join(*args):
        return '/'.join(args)

    def search(self, name):
        data = {
            'query': {
                'bool': {
                    'should': [
                        {
                            'match': {
                                'name': {
                                    'query': name,
                                    'operator': 'and'
                                }
                            }
                        },
                        {
                            'match': {
                                'name.raw': {
                                    'query': name,
                                    'operator': 'and'
                                }
                            }
                        },
                    ]
                }
            },
            'size': 50
        }

        data = json.dumps(data)
        uri = self.join(URI_BASE, INDEX, '_doc', '_search')
        ret = requests.post(uri, data=data, headers=HEADERS)
        print(ret.text)
        jsonData = json.loads(ret.text)
        print(jsonData['hits'])

    def deal_all(self):
        indexes = self.get_indexes()
        for i in indexes.split('\n'):
            tup = i.split(' ')
            checks = [i for i in tup if i.endswith('_friend_ik')]
            print(checks)
            if checks:
                index_name = checks[0]
                self.del_index(index_name)
                self.check_and_create(index_name)

    def check_and_create(self, index_name):
        if not self.check_index_ok(index_name):
            self.del_index(index_name)
            self.create_index(index_name)

    def add_name(self, name, gbId, obId):
        data = {'name': name,
                'gbId': gbId}

        data = json.dumps(data)
        url = f'{URI_BASE}/{INDEX}/_doc/{obId}'

        ret = requests.post(url, data=data, headers=HEADERS)
        print(ret.text)

    def all_info(self):
        indexes = self.get_indexes()
        for i in indexes.split('\n'):
            tup = i.split(' ')
            checks = [i for i in tup if i.endswith('_friend_ik')]
            if checks:
                index_name = checks[0]
                print(index_name, self.get_info(index_name))

    def get_info(self, index_name):
        url = '{}/{}'.format(URI_BASE, index_name)
        headers = {
            'Authorization': 'Basic %s' % authB64.decode('ascii'),
        }
        ret = requests.get(url, headers=headers)
        try:
            jsonData = json.loads(ret.text)
            if jsonData[index_name]['mappings']['properties']['name']['analyzer'] == 'ik_max_word':
                return True
        except Exception as e:
            print(e)
            return False


def main():
    et = EsTest()
    #et.all_info()
    # et.check_and_create('20007_friend_ik')
    # et.del_index('20217_friend_ik')
    # et.ana('一二三四五六七')
    #et.update_flood_stage()
    #et.set_block_not_read_only()
    et.add_name('乔露凝', '5716224206216101890', 203081127261407233)
    et.search('乔露凝')
#    et.deal_all()


if __name__ == '__main__':
    main()
