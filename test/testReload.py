import zoom

def HotFix():
    # 此时程序中断, 将Zoom模块的Eat进行修改, 然后控制台按回车,程序继续
    # =====中断=====
    input()
    # =====中断=====
    import importlib
    importlib.reload(zoom)

print ("热更新前")
_cat = zoom.cat
_cat.Eat()
HotFix()
print ("热更新后")
print ("cat还是Zoom的cat吗", zoom.cat is _cat)
zoom.cat.Eat()
_cat.Eat()