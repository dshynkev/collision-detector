'''
AUTHOR: 	 	principio
LAST EDITED: 	
DESCRIPTION: 	
KNOWN ISSUES: 	
'''

'''
AUTHOR:          principio
LAST EDITED:
DESCRIPTION:     Circle item class.
KNOWN ISSUES:     Not implemented.
'''

from helpers import getRandomNormalizedColor, load_GLshaders

import pyglet
from pyglet.gl import *

from glhelper import *

class Circle:
    def __init__(self, center, radius):
        self.x = center[0]
        self.y = center[1]
        self.radius = radius

        self.color = getRandomNormalizedColor()
        
        
    shaders=load_GLshaders()

    def render(self):
        self.shaders.bind()
        for window in pyglet.app.windows:
            pass
        scalex,scaley=window.get_size()        
        scalex = 2/scalex
        scaley = 2/scaley        
        print(self.radius*scalex)
        self.shaders.uniformf(b'center', (-1+self.x*scalex)/(self.radius*scalex), (-1+self.y*scaley)/(self.radius*scaley))
        self.shaders.uniformf(b'circleColor',  *self.color)

        self.shaders.uniform_matrixf(b'scaleMatrix', [(self.radius*scalex), 0, 0, 0,\
                                                     0, (self.radius*scaley), 0, 0,\
                                                     0, 0, 1, 0,\
                                                     0, 0, 0, 1])

        tex=pyglet.image.Texture.create(2, 2)
        tex.blit(-1, -1)
        self.shaders.unbind()
        