'''
AUTHOR:          principio
LAST EDITED:	2015-05-28 23:42:44
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
        super().__init__(center[0]-radius, center[1]-radius, radius*2, radius*2)
        
        self.x, self.y = center        

        self.radius = radius

        # Normalization needed for OpenGL color model (vec4([0...1]))
        self.color = normalize(getRandomColor())
        
    #Load static shaders. Since we have no fallback option if this fails, ignore all exceptions. 
    shaders=load_GLshaders()
    
    def contains(self, point):
        return (point[0]-self.x)*(point[0]-self.x)+(point[1]-self.y)*(point[1]-self.y) <= self.radius*self.radius   # (x-m)^2+(y-n)^2 <= R^2
        
    def _moveBy(self, trans_vector):
        self.x+=trans_vector[0]
        self.y+=trans_vector[1]
    
    def render(self):
        self.colliding = (len(self.colliding_items) > 0)        
        
        self.shaders.bind()
             
        scalex = 2/self.SCENE_WIDTH    # Set scale factors to width/height reciprocals: this will map pixels to OpenGL coordinates
        scaley = 2/self.SCENE_HEIGHT
        
        relative_scalex = scalex*(self.radius + const.SMOOTH_WIDTH)     # Determine relative scale factors: scale with respect to radius
        relative_scaley = scaley*(self.radius + const.SMOOTH_WIDTH)     # We add smooth_width here because the transition ring is also part of the circle
        
        self.shaders.uniformi(b'paintBorder', self.colliding)   # Whether the border should be painted
        
        # Center is mapped to correct offset (coords start from center, so -1+coord is its translation to lower left corner, where Pyglet coords start)
        # We divide center coords by relative scale factors, because they are NOT to be scaled with respect to radius, only distances are.
        self.shaders.uniformf(b'center', (-1+self.x*scalex)/relative_scalex, (-1+self.y*scaley)/relative_scaley)
        
        self.shaders.uniformf(b'smoothWidth', const.SMOOTH_WIDTH)
        self.shaders.uniformf(b'borderWidth', const.BORDER_WIDTH)
        
        self.shaders.uniformf(b'circleColor',  *self.color)
        self.shaders.uniformf(b'borderColor', *normalize(const.COLOR_COLLIDING))
        
        # Now, all distances will be scaled with respect to the radius of the circle.
        self.shaders.uniform_matrixf(b'scaleMatrix', [relative_scalex, 0, 0, 0,\
                                                     0, relative_scaley, 0, 0,\
                                                     0, 0, 1, 0,\
                                                     0, 0, 0, 1])

        # Create a texture, that, when translated to (-1,-1), the Pyglet coord origin, will cover the entire scene (we will scale it later in shaders).
        tex=pyglet.image.Texture.create(2, 2)
        # ...and translate it as needed.        
        tex.blit(-1, -1)
        
        self.shaders.unbind()

    def collidingWith(self, item):
        if(type(self) is type(item)):
            return self._check_collide_circle(item)
        else:
            return False    #TODO: Implement
        
    def _check_collide_circle(self, item):
        dist = math.sqrt((self.x-item.x)*(self.x-item.x) + (self.y-item.y)*(self.y-item.y))
        return dist <= self.radius+item.radius
