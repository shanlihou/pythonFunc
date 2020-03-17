from xmlrpc.server import SimpleXMLRPCServer
import bin
import json
import os
import cmd

HANDLE_LIST = []


def add_handle(func):
    HANDLE_LIST.append(func.__name__)
    return func


class Command(object):
    def __init__(self):
        pass

    def __call__(self, cmd, args):
        bin_mod = getattr(bin, cmd)
        return bin_mod.main(args.split())


class IstaServer(object):

    def __init__(self, simple_server):
        self._cmd = Command()
        for func_name in HANDLE_LIST:
            simple_server.register_function(
                getattr(self, func_name), func_name)

    @add_handle
    def get_string(self, str_just_test):
        return "get is :%s" % str_just_test

    def pack_response(self, *args, **kwargs):
        ret_obj = {
            'isok': True
        }
        ret_obj.update(kwargs)
        return json.dumps(ret_obj)

    def unpack_request(self, req_str):
        return json.loads(req_str)

    @add_handle
    def cmd(self, request):
        req = self.unpack_request(request)
        cmd_str = req['cmd_str']
        cmd_list = cmd_str.split(' ', 1)
        command = cmd_list[0]
        args = cmd_list[1] if len(cmd_list) > 1 else ''
        resp_str = self._cmd(command, args)
        return self.pack_response(result=resp_str)


if __name__ == '__main__':
    s = SimpleXMLRPCServer(('0.0.0.0', 8080))
    _is = IstaServer(s)
    s.serve_forever()
