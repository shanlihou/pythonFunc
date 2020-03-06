from xmlrpc.client import ServerProxy
if __name__ == '__main__':
    s = ServerProxy("http://192.168.16.123:8080")
    print(s.fetch_remote_path('{"remote_path": "pyistaServer"}')) 