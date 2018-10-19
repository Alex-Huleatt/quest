import ez, random
from pyglet.gl import *
import threading
from collections import defaultdict
from time import sleep

def generateRandomColor():
    r,g,b = random.random(), random.random(), random.random()
    m = (r*r+g*g+b*b)**.5
    return (.6*r/m,.6*g/m,.6*b/m, 1)

def neighbors(t,w,h):
    x,y = t
    return [((x+i)%w,(y+j)%h) for i in [-1,0,1] for j in [-1,0,1] if i or j]

born = [2,8]
survive = [2,3,4,6,8]
#211 generations at sz = 3 to finish-ish

import pyglet
from pyglet.window import mouse
frame = 0

def main2():
    window = pyglet.window.Window()
    sz = 3
    width,height = window.width, window.height

    def gen(t):
        batch = pyglet.graphics.Batch()
        glClear(GL_COLOR_BUFFER_BIT)
        global born
        global survive
        global frame
        if frame > 230:
            survive = [5,6,7,8]
            born = [3,5]

        s = (0, 0, 255, 0, 0, 255,0, 0, 255,0, 0, 255,)
        n_count = defaultdict(int)
        
        for o in gen.active: #O(n)
            for n in neighbors(o, width//sz, height//sz):
                n_count[n]+=1

        new_active = set()

        for k in n_count: #O(n)
            c = n_count[k]

            if (k in gen.active and c in survive) or (k not in gen.active and c in born):
                new_active.add(k)
                x,y,w,h=(k[0]+1)*sz,height - (k[1]+1)*sz,sz,sz
                
                batch.add(4, pyglet.gl.GL_QUADS, None, ('v2f', [x, y, x-w, y, x-w, y-h, x, y-h]), ('c3B', s))

        batch.draw()
        # pyglet.image.get_buffer_manager().get_color_buffer().save('out/'+str(frame)+'.png')
        frame += 1

        gen.active = new_active

    gen.active = set([(width//sz//2,height//sz//2), (width//sz//2+1,height//sz//2)])
    try:
        pyglet.clock.schedule_interval(gen, 0.05)

        pyglet.app.run()
    finally:
        pass



if __name__ == "__main__":
    main2()