#coding=utf8
import os
class ListPath(object):
    def __init__(self, path):
        self.path = path
    
    def pathRec(self, path):
        for i in os.listdir(path):
            fileName = os.path.join(path, i)
            if os.path.isdir(fileName):
                self.pathRec(fileName)
                continue
            
            self.pathList.append(fileName)
                
    def getAllFile(self):
        self.pathList = []
        self.pathRec(self.path)
        return self.pathList
        
    def test(self):
        fileList = self.getAllFile()
        print(fileList)
    
if __name__ == '__main__':
    lp = ListPath(r'E:\889914\video')
    lp.test()