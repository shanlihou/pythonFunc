import cfscrape
from lxml import html
import os
import re
import pickle
import json
# get ss from web


def ping(ip):
    cmd = os.popen('ping %s' % ip)
    result = cmd.read()
    pat = re.compile(r'\((\d+)\%.*\)')
    print(result)
    find = pat.search(result)
    isLoss = True
    if find:
        ret = int(find.groups()[0])
        print(ret)
        if ret < 5:
            isLoss = False

    pat = re.compile(r'= (\d+)ms')
    find = pat.findall(result)
    if len(find) == 3:
        find = [int(x) for x in find]
        if not isLoss:
            return find[2]
        
    return -1


def getFreeSS():
    youneedSSUrl = "https://v2s.top/"
    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    # Or: scraper = cfscrape.CloudflareScraper() # CloudflareScraper inherits
    # from requests.Session
    rsponse = scraper.get(youneedSSUrl)
    # print(rsponse.text) # => "..."
    if (rsponse.status_code == 200):
        responseHtml = rsponse.text
        print(responseHtml)
        tree = html.fromstring(responseHtml)
        ssservers = tree.xpath("//section[@class='context']/table/tbody/tr")
        ssserversCount = len(ssservers)
        servers = []
        for s in range(ssserversCount):
            serverObjAttrs = tree.xpath(
                "//section[@class='context']/table/tbody/tr/td/text()")
            startIndex = 6 * s
            ip = serverObjAttrs[startIndex + 0]
            port = serverObjAttrs[startIndex + 1]
            passwd = serverObjAttrs[startIndex + 2]
            # serverObjAttrs[startIndex+3] #aes-256-cfb or
            method = 'aes-256-cfb'
            tm = serverObjAttrs[startIndex + 4]
            country = serverObjAttrs[startIndex + 5]
            sjson = {
                "server": ip,
                "server_port": int(port),
                "password": passwd,
                "method": method,
                "remarks": ip + "-" + country
            }
            servers.append(sjson)
        return servers
    else:
        return []


class SSR(object):
    def __init__(self):
        pass

    def save(self, result):
        data = pickle.dumps(result)
        with open('result.txt', 'wb') as fw:
            fw.write(data)

    def load(self):
        with open('result.txt', 'rb') as fr:
            result = fr.read()
            return pickle.loads(result)
        
    def loadFromJson(self):
        with open('electron.txt') as fr:
            jsonObj = json.loads(fr.read())
            return jsonObj

    def toJson(self, result):
        final = []
        for data in result:
            speed = ping(data['server'])
            if speed == -1:
                continue

            cfg = {
                "server": data['server'],
                "server_port": data['server_port'],
                "password": data['password'],
                "method": data['method'],
                "plugin": "",
                "plugin_opts": "",
                "plugin_args": "",
                "remarks": data["remarks"],
                "timeout": 5,
                'speed': speed,
            }
            final.append(cfg)
        final.sort(key=lambda cfg: cfg['speed'])    
        
        with open('couldUse.txt', 'wb') as fw:
            fw.write(pickle.dumps(final))

        final = json.dumps(final, indent=4, separators=(',', ':'))
        print(final)
        
    def google(self):
        pass

    def test(self):
        # self.save(getFreeSS())
        result = self.loadFromJson()
        self.toJson(result)


if __name__ == '__main__':
    if 1:
        ssr = SSR()
        ssr.test()
    else:
        ping('www.baidu.com')
