'''
AUTHOR:          principio
LAST EDITED:	2015-05-28 00:09:01
DESCRIPTION:     Circle item class.
KNOWN ISSUES:    *> Will crash if anything on OpenGL side fails.
'''

from helpers import getRandomColor, normalize, load_GLshaders
import constants as const

import pyglet, math
from pyglet.gl import *
from glhelper import *

from abstractshape import *

class Circle(AbstractShape):
    def __init__(self, center, radius):
        self.x = center[0]
        self.y = center[1]
        self.radius = radius

        self.fill_color = normalize(getRandomColor())
        self.color = self.fill_color
        
    #Load static shaders. Since we have no fallback option if this fails, ignore exceptions. 
    shaders=load_GLshaders()
    
    def contains(self, point):
        return (point[0]-self.x)*(point[0]-self.x)+(point[1]-self.y)*(point[1]-self.y) <= self.radius*self.radius

    def move(self, trans):
        self.x+=trans[0]
        self.y+=trans[1]
        
    def setCollided(self, state=True):
        self.colliding=state
    
    def render(self):
        self.shaders.bind()
        for window in pyglet.app.windows:
            pass
        scalex,scaley=window.get_size()        
        scalex = 2/scalex
        scaley = 2/scaley
        relative_scalex = scalex*(self.radius + const.BORDER_WIDTH + const.SMOOTH_WIDTH)
        relative_scaley = scaley*(self.radius + const.BORDER_WIDTH + const.SMOOTH_WIDTH)
        self.shaders.uniformf(b'center', (-1+self.x*scalex)/relative_scalex, (-1+self.y*scaley)/relative_scaley)
        self.shaders.uniformf(b'paintBorder', 2.0 if self.colliding else 0.0)
        self.shaders.uniformf(b'smoothWidth', const.SMOOTH_WIDTH)
        self.shaders.uniformf(b'borderWidth', const.BORDER_WIDTH)
        self.shaders.uniformf(b'circleColor',  *self.color)
        self.shaders.uniformf(b'borderColor', *normalize(const.COLOR_COLLIDING))        
        self.shaders.uniform_matrixf(b'scaleMatrix', [relative_scalex, 0, 0, 0,\
                                                     0, relative_scaley, 0, 0,\
                                                     0, 0, 1, 0,\
                                                     0, 0, 0, 1])

        tex=pyglet.image.Texture.create(2, 2)
        tex.blit(-1, -1)
        self.shaders.unbind()    

    def check_collide(self, item):
        if(type(self) is type(item)):
            return self._check_collide_circle(item)
        else:
            return False    #TODO: Implement
        
    def _check_collide_circle(self, item):
        dist = math.sqrt((self.x-item.x)*(self.x-item.x) + (self.y-item.y)*(self.y-item.y))
        return dist <= self.radius+item.radius
