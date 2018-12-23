class Coco(cocos.layer.Layer):
    def __init__(self):
        print('coco init')
        super(Coco, self).__init__()
        self.taskList = []
        self.resetState()
        self.schedule(self.update)