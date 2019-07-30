import telnetlib
import time
import pexpect


class KbeNode(object):
    def __init__(self, host, port):
        self.tn = telnetlib.Telnet(host, port=port, timeout=10)
        self.tn.set_debuglevel(1000)
        
    def write(self, data):
        self.tn.write(data.encode('ascii'))
        
    def read_until(self, data):
        self.tn.read_until(data.encode('ascii'))

    def test(self):
        self.read_until('password:')
        self.write('pwd123456' + '\r\n')
        print(self.tn.read_very_eager())
        self.write('print(1)\n')
        print(self.tn.read_very_eager())
        self.write('\n')
        self.write('\n')
        self.write('\n')
        print(self.tn.read_lazy())
        self.tn.mt_interact()
        time.sleep(5)
        
        print('end')


if __name__ == '__main__':
    kn = KbeNode('192.168.10.173', 40000)
    kn.test()
