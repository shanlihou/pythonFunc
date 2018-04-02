#coding=utf8
from gifHelper import gifHelper
from planeHelper import planeHelper
from throwGame import throwGame
gif = gifHelper()
#gif.parseGif('D:\\tmp\\test.gif')
#gif.parseGif('D:\\mie.gif')
if __name__ == '__main__':
    opt = 0
    if opt == 0:
        game = throwGame(16)
        img1 = game.createImg()
        gif.createGIF('box.gif', img1, 256, 256, 0, 0)
        
    else:
        planeGame = planeHelper()
        img, strPrint = planeGame.parse('飞行棋', '1')
        img, strPrint = planeGame.parse('飞行棋', '2')
        #img, strPrint = planeGame.parse('������', '2')
        img, strPrint = planeGame.parse('飞行棋开始', '1')
        print 'print:', strPrint
        count = 0
        player = 0
        while 1:
            #strRet = raw_input("Enter your input: ")
            #name = raw_input("name: ")
            #print strRet
            #print name
            img, strPrint = planeGame.parse('fly', str(player + 1))
            player = (player + 1)  % 2
            print strPrint
            if not img:
                continue
            print 'len:', len(img)
            for i in range(len(img)):
                if img[i]:
                    count += 1
                    print 'draw'
                    gif.createGIF('box%d.gif' % count, img[i], 256, 256, 0, 0)
                    exit()
                if strPrint[i]:
                    print strPrint[i]