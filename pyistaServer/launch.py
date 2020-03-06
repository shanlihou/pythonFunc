from xmlrpc.server import SimpleXMLRPCServer
from FetchFtp import tunnel
import json

HANDLE_LIST = []


def add_handle(func):
    HANDLE_LIST.append(func.__name__)
    return func


class IstaServer(object):

    def __init__(self, simple_server):
        for func_name in HANDLE_LIST:
            simple_server.register_function(
                getattr(self, func_name), func_name)

    @add_handle
    def get_string(self, str):
        return "get is :%s" % str

    def pack_response(self, *args, **kwargs):
        return 'ok'

    def unpack_request(self, str):
        return json.loads(str)

    @add_handle
    def fetch_remote_path(self, request):
        t = tunnel.Tunnel('192.168.16.123')
        req = self.unpack_request(request)
        t.down_path(req['remote_path'])
        return self.pack_response()


if __name__ == '__main__':
    s = SimpleXMLRPCServer(('0.0.0.0', 8080))
    _is = IstaServer(s)
    s.serve_forever()
