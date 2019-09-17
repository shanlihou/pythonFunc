import socket
import asyncio
import SSR
import functools
import json


class GlobalData(object):
    CALL_BACK = None
    GOOD_DATA = {}


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


def printFinal():
    p = [data for data in GlobalData.GOOD_DATA.values() if data is not None]
    final = json.dumps(p, indent=4, separators=(',', ':'))
    print(final)


def getIndexInfo(index, data):
    print(index, data)
    dataList = data.decode('ascii').split('&')
    if index in GlobalData.GOOD_DATA:
        printFinal()
        return

    GlobalData.GOOD_DATA[index] = {
        "server": dataList[0],
        "server_port": int(dataList[1]),
        "password": dataList[2],
        "method": dataList[3],
        "plugin": "",
        "plugin_opts": "",
        "plugin_args": "",
        "remarks": dataList[4],
        "timeout": 5,
    }
    send(afterDown, Opr.DownIndex)


def afterDown(data):
    index = int(data)
    if index in GlobalData.GOOD_DATA:
        printFinal()
        return

    print(index)
    ret = SSR.SSR.google()
    print(ret)
    if ret:
        send(functools.partial(getIndexInfo, index), Opr.GetServer)
    else:
        GlobalData.GOOD_DATA[index] = None
        send(afterDown, Opr.DownIndex)


def afterReset(*args):
    ret = SSR.SSR.google()
    print(ret)
    if ret:
        send(functools.partial(getIndexInfo, 0), Opr.GetServer)
    else:
        send(afterDown, Opr.DownIndex)


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
