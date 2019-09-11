import socket
import asyncio


async def send():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    port = 1080
    address = (host, port)

    s.sendto(b'1', address)
    print(1)
    s.close()


class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(data)


def start_discovery():
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(
        DiscoveryProtocol, local_addr=('0.0.0.0', 9527))
    loop.run_until_complete(asyncio.wait([
        t,
        send()
    ]))
    loop.run_forever()


if __name__ == '__main__':
    start_discovery()
