#!/usr/bin/python 
#coding:utf-8 
from jpgHelper import jpgHelper
from display import display
jpg = jpgHelper('D:\\mie.jpg')
jpg.parser()
jpg.test()
display().display()
display().test()


'''
if event.type==KEYDOWN:
# �����������������ѵ�ظ���ԭʼ״̬
    if event.key == K_DOWN:
        #AngleYZ = (AngleYZ + 5) % 360
        camera.turnDown(5)
    elif event.key == K_RIGHT:
        camera.turnRight(5)
    elif event.key == K_UP:
        camera.turnUp(5)
    elif event.key == K_LEFT:
        camera.turnLeft(5)
        
    elif event.key == K_w:
        camera.moveForward()
        box.getRelCoor(camera)
    elif event.key == K_s:
        camera.moveBackward()
        box.getRelCoor(camera)
    elif event.key == K_a:
        camera.moveLeft()
        box.getRelCoor(camera)
    elif event.key == K_d:
        camera.moveRight()
        box.getRelCoor(camera)
if event.type == MOUSEMOTION:
    position = event.pos
#          print position
  '''