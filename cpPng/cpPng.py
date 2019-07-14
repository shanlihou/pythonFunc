import sys
import os
sys.path.append(r'..\Lib')
import ListPath


class CpPng(object):
    def __init__(self, dst):
        self.dst = dst
        
    def cpFile(self, filename: str):
        if not filename.endswith('.png'):
            return
        
        if 'gray' in filename:
            return
        
        dirname = os.path.basename(os.path.dirname(filename))
        basename = os.path.basename(filename)
        newname = dirname + '_' + basename
        print(newname)
        cmdstr = 'copy {} {}'.format(filename, os.path.join(self.dst, newname))
        print(cmdstr)
        os.system(cmdstr)
        
    def moveFile(self, filename: str):
        if 'gray' not in filename:
            return
        
        print(filename)
        dirname = os.path.dirname(filename)
        if 'grey' in dirname:
            return
    
        base = os.path.basename(filename)
        dirname += '_grey'
        ListPath.mkdir(dirname)
        cmdStr = 'move "{}" "{}"'.format(filename, os.path.join(dirname, base))
        print(cmdStr)
        os.system(cmdStr)
        
    def test(self):
        lp = ListPath.ListPath(r'G:\github\others\kaixinxiaoxiaole\my_resource_out\my_resource_out')
        for f in lp.getAllFile():
            self.moveFile(f)
    
if __name__ == '__main__':
    cp = CpPng(r'G:\github\others\kaixinxiaoxiaole\my_resource_out\whole')
    cp.test()