from server import serverThread
from coco import start as cocoStart
from log import logger

if __name__ == '__main__':
    serverThread()
    cocoStart()
