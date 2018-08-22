import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}
class VideoInfo(object):
    def __init__(self):
        pass
    
    def getVideoInfo(self, code):
        resp = requests.get('https://www.javbus11.pw/search/ssni-251', headers=headers)
        print(resp.text)
        
    def test(self):    
        self.getVideoInfo(1234)
    
if __name__ == '__main__':
    video = VideoInfo()
    video.test()