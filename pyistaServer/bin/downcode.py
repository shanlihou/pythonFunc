import requests
import urllib
import json
import os
from fileinput import filename


class github:
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo

    def downFile(self, filename):
        url = 'https://raw.githubusercontent.com/' + \
            self.user + '/' + self.repo + '/master/' + filename
        ret = requests.get(url)
        diskName = self.repo + '/' + filename
        with open(diskName, 'wb') as fw:
            fw.write(ret.content)

    def getDir(self, dir=''):
        dirName = self.repo + '/' + dir
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        url = 'https://api.github.com/repos/' + \
            self.user + '/' + self.repo + '/contents/' + dir
        ret = requests.get(url)
        jsonRet = json.loads(ret.text)
        for i in jsonRet:
            if i['type'] == 'dir':
                self.getDir(i['path'])
            else:
                print(i['path'])
                self.downFile(i['path'])


if __name__ == '__main__':
    git = github('junerain123', 'javsdt')
    git.getDir()
