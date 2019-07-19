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
    find = pat.search(result)
    if find:
        result = int(find.groups()[0])
        print(result)
        if result < 5:
            return True

    return False


def getFreeSS():
    youneedSSUrl = "https://www.youneed.win/free-ss"
    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    # Or: scraper = cfscrape.CloudflareScraper() # CloudflareScraper inherits
    # from requests.Session
    rsponse = scraper.get(youneedSSUrl)
    # print(rsponse.text) # => "..."
    if (rsponse.status_code == 200):
        responseHtml = rsponse.text
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

    def toJson(self, result):
        final = []
        for data in result:
            if not ping(data['server']):
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
                "timeout": 5
            }
            final.append(cfg)
        with open('couldUse.txt', 'wb') as fw:
            fw.write(pickle.dumps(final))

        final = json.dumps(final, indent=4, separators=(',', ':'))
        print(final)

    def test(self):
        result = self.load()
        self.toJson(result)


if __name__ == '__main__':
    ssr = SSR()
    ssr.test()
