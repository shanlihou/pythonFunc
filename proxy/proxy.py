#!/usr/bin/python
#-*- coding:utf-8 -*-
 
import socket, logging
import select, errno
import os
import sys
import traceback
import gzip
from StringIO import StringIO
import Queue
import threading
import time
import thread
import cgi
from cgi import parse_qs
import json
import imp
from os.path import join, getsize
import re
import ssl
 
##################user config ##################
logger = logging.getLogger("network-server")
#############################################
 
def getTraceStackMsg():
    tb = sys.exc_info()[2]
    msg = ''
    for i in traceback.format_tb(tb):
        msg += i
    return msg
 
def InitLog():
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("network-server.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
 
def clearfdpro(epoll_fd, params, fd):
    try:
        fd_check = int(fd)
    except Exception, e:
        print "fd error"
        sys.exit(1)
    try:
        #print "pid:%s, close fd:%s" % (os.getpid(), fd)
        epoll_fd.unregister(fd)
    except Exception, e:
        #print str(e)+getTraceStackMsg()
        pass
 
    try:
        param = params[fd]
        try:
            addr = param["addr"]
            if "next" in param:
                print "close sock, %s:%s" % (addr[0], addr[1])
        except Exception, e:
            pass
        param["connections"].shutdown(socket.SHUT_RDWR)
        param["connections"].close()
        f = param.get("f", None)
        if f != None:
            f.close()
        rc = param.get("rc", None)
        if rc != None:
            rc.close()
        if "read_cache_name" in param:
            os.remove(param["read_cache_name"])
    except Exception, e:
        #print str(e)+getTraceStackMsg()
        pass
 
    try:
        del params[fd]
        #logger.error(getTraceStackMsg())
        #logger.error("clear fd:%s" % fd)
    except Exception, e:
        #print str(e)+getTraceStackMsg()
        pass
 
def clearfd(epoll_fd, params, fd):
    try:
        param = params[fd]
        if "nextfd" in param:
            nextfd = param["nextfd"]
            next_param = params[nextfd]
            del param["nextfd"]
            del next_param["nextfd"]
            if not "next" in param: #masterfd
                clearfdpro(epoll_fd, params, nextfd)
            else: # nextfd
                if not "writedata" in next_param or len(next_param["writedata"]) == 0:
                    clearfdpro(epoll_fd, params, nextfd)
                else:
                    next_param["sendandclose"] = "true"
        clearfdpro(epoll_fd, params, fd)
    except Exception, e:
        #print str(e)+getTraceStackMsg()
        pass
 
def FindHostPort(datas):
    host_s = -1
    host_e = -1
    host_str = None
    host = ""
    port = ""
    if not datas.startswith("CONNECT"):
        host_s = datas.find("Host:")
        if host_s < 0:
            host_s = datas.find("host:")
        if host_s > 0:
            host_e = datas.find("\r\n", host_s)
        if host_s > 0 and host_e > 0:
            host_str = datas[host_s+5:host_e].strip()
            add_list = host_str.split(":")
            if len(add_list) == 2:
                host = add_list[0]
                port = add_list[1]
            else:
                host = add_list[0]
                port = 80
            first_seg = datas.find("\r\n")
            first_line = datas[0:first_seg]
            print("\nfirst line chaged:")
            print(first_line)
            first_line = first_line.replace(" http://%s" % host_str, " ")
            print(first_line)
            datas = first_line + datas[first_seg:]
    else:
        first_seg = datas.find("\r\n")
        head_e = datas.find("\r\n\r\n")
        if first_seg > 0 and head_e > 0:
            first_line = datas[0:first_seg]
            com,host_str,http_version = re.split('\s+', first_line)
            add_list = host_str.split(":")
            if len(add_list) == 2:
                host = add_list[0]
                port = add_list[1]
            else:
                host = add_list[0]
                port = 443
            host_s = 1
            host_e = 1
    return host_str,host_s,host_e,host,port,datas
 
def connect_pro(params, param, epoll_fd, datas, fd, cur_time, host, port):
    try:
        nextfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        nextfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        nextfd.settimeout(5)
        try:
            nextfd.connect((host, int(port)))
        except Exception, e:
            print "########%s,%s connect fail" % (host,port)
        nextfd.setblocking(0)
        next_fileno = nextfd.fileno()
        print "pid:%s, connect %s:%s fd:%s" % (os.getpid(), host, port, next_fileno)
        if next_fileno in params:
            print "fileno exist"
            sys.exit(1)
        if not datas.startswith("CONNECT"):
            next_param = {"addr":[host,port],"writelen":0, "connections":nextfd, "time":cur_time, "nextfd":fd}
            param["nextfd"] = next_fileno
            next_param["writedata"] = datas
            next_param["writelen"] = 0
            next_param["next"] = "true"
            param["read_len"] = 0
            param["readdata"] = ""
            params[next_fileno] = next_param
            epoll_fd.register(next_fileno, select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)
            epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
        else:
            next_param = {"addr":[host,port],"writelen":0, "connections":nextfd, "time":cur_time, "nextfd":fd}
            param["nextfd"] = next_fileno
            next_param["next"] = "true"
            params[next_fileno] = next_param
            epoll_fd.register(next_fileno, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
            param["read_len"] = 0
            param["readdata"] = ""
            param["writedata"] = "HTTP/1.1 200 Connection Established\r\nConnection: close\r\n\r\n"
            param["writelen"] = 0
            param["reuse"] = "true"
            epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)
    except socket.error, msg:
        clearfd(epoll_fd,params,fd)
 
def process_datas(process_status, params, param, epoll_fd, datas, read_len, fd, cur_time):
    if process_status == "close":
        clearfd(epoll_fd,params,fd)
    else:
        need_connect = False
        host_str = None
        host_s = -1
        host_e = -1
        if "reuse" in param and "next" not in param:
            if not datas.startswith("CONNECT") and \
                    not datas.startswith("GET") and \
                    not datas.startswith("POST") and \
                    not datas.startswith("PUT"):
                del param["reuse"]
            else:
                host_str,host_s,host_e,host,port,datas = FindHostPort(datas)
                host_s = int(host_s)
                host_e = int(host_e)
                next_fileno = param["nextfd"]
                next_param = params[next_fileno]
                addr = next_param["addr"]
                if host_s > 0 and host_e > 0:
                    if host != addr[0] or str(port) != str(addr[1]):
                        print "%s,%s neq %s,%s" % (host,port,addr[0],addr[1])
                        need_connect = True
                        del param["nextfd"]
                        del next_param["nextfd"]
                        clearfd(epoll_fd,params,next_fileno)
                    del param["reuse"]
                else:
                    param["read_len"] = read_len
                    param["readdata"] = datas
                    return None
        if need_connect or not "nextfd" in param:
            if host_str == None or not host_s > 0 or not host_e > 0:
                host_str,host_s,host_e,host,port,datas = FindHostPort(datas)
                host_s = int(host_s)
                host_e = int(host_e)
            if host_s > 0 and host_e > 0:
                if not datas.startswith("CONNECT"):
                    epoll_fd.modify(fd, select.EPOLLERR | select.EPOLLHUP) # 简单处理，http连接时把读去掉，避免内存攻击
                thread.start_new_thread(connect_pro,(params, param, epoll_fd, datas, fd, cur_time, host, port))
            else:
                param["read_len"] = read_len
                param["readdata"] = datas
        else:
            next_fileno = param["nextfd"]
            next_param = params[next_fileno]
            if "next" in param:
                next_param["reuse"] = "true"
            write_data = next_param.get("writedata", "")
            write_data += datas
            next_param["writedata"] = write_data
            param["read_len"] = 0
            param["readdata"] = ""
            epoll_fd.modify(next_fileno, select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)
        if process_status == "close_after_process":
            print "close after process"
            clearfd(epoll_fd,params,fd)
 
def run_main(listen_fd):
    try:
        epoll_fd = select.epoll()
        epoll_fd.register(listen_fd.fileno(), select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
        print "listen_fd:%s" % listen_fd.fileno()
    except select.error, msg:
        logger.error(msg)
 
 
    params = {}
 
    last_min_time = -1
    while True:
        epoll_list = epoll_fd.poll()
 
        cur_time = time.time()
        for fd, events in epoll_list:
            if fd == listen_fd.fileno():
                while True:
                    try:
                        conn, addr = listen_fd.accept()
                        conn.setblocking(0)
                        epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
                        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        #conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
                        params[conn.fileno()] = {"addr":addr,"writelen":0, "connections":conn, "time":cur_time}
                    except socket.error, msg:
                        break
            elif select.EPOLLIN & events:
                param = params.get(fd,None)
                if param == None:
                    continue
                param["time"] = cur_time
                datas = param.get("readdata","")
                cur_sock = params[fd]["connections"]
                read_len = param.get("read_len", 0)
                process_status = "close"
                while True:
                    try:
                        data = cur_sock.recv(102400)
                        if not data:
                            if datas == "":
                                break
                            else:
                                raise Exception("close after process")
                        else:
                            datas += data
                            read_len += len(data)
                    except socket.error, msg:
                        if msg.errno == errno.EAGAIN:
                            process_status = "process"
                            break
                        else:
                            break
                    except Exception, e:
                        process_status = "close_after_process"
                        break
                process_datas(process_status, params, param, epoll_fd, datas, read_len, fd, cur_time)
            elif select.EPOLLHUP & events or select.EPOLLERR & events:
                clearfd(epoll_fd,params,fd)
                logger.error("sock: %s error" % fd)
            elif select.EPOLLOUT & events:
                param = params.get(fd,None)
                if param == None:
                    continue
                param["time"] = cur_time
                sendLen = param.get("writelen",0)
                writedata = param.get("writedata", "")
                total_write_len = len(writedata)
                cur_sock = param["connections"]
                f = param.get("f", None)
                totalsenlen = param.get("totalsenlen", None)
                if writedata == "":
                    clearfd(epoll_fd,params,fd)
                    continue
                while True:
                    try:
                        sendLen += cur_sock.send(writedata[sendLen:])
                        if sendLen == total_write_len:
                            if f != None and totalsenlen != None:
                                readmorelen = 102400
                                if readmorelen > totalsenlen:
                                    readmorelen = totalsenlen
                                morefiledata = ""
                                if readmorelen > 0:
                                    morefiledata = f.read(readmorelen)
                                if morefiledata != "":
                                    writedata = morefiledata
                                    sendLen = 0
                                    total_write_len = len(writedata)
                                    totalsenlen -= total_write_len
                                    param["writedata"] = writedata
                                    param["totalsenlen"] = totalsenlen
                                    continue
                                else:
                                    f.close()
                                    del param["f"]
                                    del param["totalsenlen"]
                            if not "sendandclose" in param:
                                param["writedata"] = ""
                                param["writelen"] = 0
                                epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
                            else:
                                clearfd(epoll_fd,params,fd)
                            break
                    except socket.error, msg:
                        if msg.errno == errno.EAGAIN:
                            param["writelen"] = sendLen
                            break
                        clearfd(epoll_fd,params,fd)
                        break
            else:
                continue
        #check time out
        if cur_time - last_min_time > 20:
            last_min_time = cur_time
            objs = params.items()
            for (key_fd,value) in objs:
                fd_time = value.get("time", 0)
                del_time = cur_time - fd_time
                if del_time > 20:
                    clearfd(epoll_fd,params,key_fd)
                elif fd_time < last_min_time:
                    last_min_time = fd_time
 
 
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    InitLog()
    port = int(sys.argv[1])
    try:
        listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error, msg:
        logger.error("create socket failed")
    try:
        listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error, msg:
        logger.error("setsocketopt SO_REUSEADDR failed")
    try:
        listen_fd.bind(('', port))
    except socket.error, msg:
        logger.error("bind failed")
    try:
        listen_fd.listen(10240)
        listen_fd.setblocking(0)
    except socket.error, msg:
        logger.error(msg)
 
 
    child_num = 19
    c = 0
    while c < child_num:
        c = c + 1
        newpid = os.fork()
        if newpid == 0:
            run_main(listen_fd)
    run_main(listen_fd)