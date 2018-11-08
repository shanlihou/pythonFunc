class TLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        cocos.layer.Layer.__init__(self)
        world_width, world_height = director.get_window_size()
        rand_color = [255, 0, 0]
        icolor = 0
        for i in range(qty_balls):
            ball = Ball((world_width*random.random(), world_height*random.random()), color=rand_color)
            rand_color[icolor] = random.randint(50, 255)
            icolor = (icolor + 1)%len(rand_color)
            self.add(ball)
self.time = 0.0
self.schedule(self.update)