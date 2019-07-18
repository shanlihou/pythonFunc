import cfscrape
from lxml import html
import os
# get ss from web


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
            sjson = {"server": ip, "server_port": int(
                port), "password": passwd, "method": method, "remarks": ip + "-" + country}
            servers.append(sjson)
        return servers
    else:
        return []


if __name__ == '__main__':
    #print(getFreeSS())
    ret = os.system('ping www.google.com')
    print('ret:', ret)
