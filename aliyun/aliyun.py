#!/usr/bin/python
# coding=utf-8

import paramiko
import os

def sftp_upload(host,port,username,password,local,remote):
    sf = paramiko.Transport((host,port))
    sf.connect(username = username,password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    print('123')
    try:
        if os.path.isdir(local):#�жϱ��ز�����Ŀ¼�����ļ�
            for f in os.listdir(local):#��������Ŀ¼
                print('123')
                sftp.put(os.path.join(local+f),os.path.join(remote+f))#�ϴ�Ŀ¼�е��ļ�
        else:
            sftp.put(local,remote)#�ϴ��ļ�
    except Exception as e:
        print('upload exception:',e)
    sf.close()

def sftp_download(host,port,username,password,local,remote):
    sf = paramiko.Transport((host,port))
    sf.connect(username = username,password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        if os.path.isdir(local):#�жϱ��ز�����Ŀ¼�����ļ�
            for f in sftp.listdir(remote):#����Զ��Ŀ¼
                sftp.get(os.path.join(remote+f),os.path.join(local+f))#����Ŀ¼���ļ�
        else:
            sftp.get(remote,local)#�����ļ�
    except Exception as e:
        print('download exception:',e)
    sf.close()

class aliyun(object):
    def __init__(self, host, port, name, pwd, local, remote):
        self.host = host
        self.port = port
        sf = paramiko.Transport((host, port))
        sf.connect(username=name, password=pwd)
        sftp = paramiko.SFTPClient.from_transport(sf)
        self.sf = sf
        self.sftp = sftp
        self.local = local
        self.remote = remote
        
    def upload(self, path):
        absPath = os.path.join(self.local, path)
        absRemote = os.path.join(self.remote, path).replace('\\', '/')
        if os.path.isdir(absPath):
            try:
                self.sftp.mkdir(absRemote)
            except Exception as e:
                print(e)
            for f in os.listdir(absPath):
                newName = os.path.join(path, f)
                self.upload(newName)
        else:
            print(absPath,'----', absRemote)
            self.sftp.put(absPath, absRemote)
        
    
    def test(self):
        self.upload('res')
        self.sf.close()
        
        

if __name__ == '__main__':
    host = '106.14.182.206'#主机
    port = 22 #端口
    username = '' #用户名
    password = '' #密码
    #local = r'G:\github\cocos\stone_war\cocoscreator_assets\build\wechatgame\res' + '\\'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
    #local = r'G:\github\cocos\stone_war\cocoscreator_assets\build' + '\\'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
    local = r'G:\github\others\kaixinxiaoxiaole\build\wechatgame' + '\\'
    remote = '/home/shanlihou/'#远程文件或目录，与本地一致，当前为linux目录格式
    ali = aliyun(host, port, username, password, local, remote)
    ali.test()