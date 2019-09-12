import socket
import asyncio
import SSR


class GlobalData(object):
    CALL_BACK = None


class Opr(object):
    GetServer = 0
    UpIndex = 1
    DownIndex = 2
    SelectIndex = 3


def send(func, *args):
    GlobalData.CALL_BACK = func

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    port = 1080
    address = (host, port)

    s.sendto(bytes(args), address)
    s.close()
    
def afterDown(data):
    index = int(data)
    print(index)


def afterReset(*args):
    ret = SSR.SSR.google()
    print(ret)


async def start():
    send(afterReset, Opr.SelectIndex, 0)


class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if GlobalData.CALL_BACK:
            GlobalData.CALL_BACK(data)


def start_discovery():
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(
        DiscoveryProtocol, local_addr=('0.0.0.0', 9527))
    loop.run_until_complete(asyncio.wait([
        t,
        start()
    ]))
    loop.run_forever()


if __name__ == '__main__':
    start_discovery()
