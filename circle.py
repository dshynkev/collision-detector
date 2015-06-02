'''
AUTHOR:          principio
LAST EDITED:	2015-06-02 01:45:00
DESCRIPTION:     Circle item class.
KNOWN ISSUES:    *> Will crash if anything on OpenGL side fails.
'''

from helpers import getRandomColor, normalized, load_GLshaders
import constants as const
import geometry

import pyglet
from pyglet.gl import *
from glhelper import *

from shape import *

class Circle(Shape, geometry.Circle):
    def __init__(self, center, radius):
        Shape.__init__(self, center-radius, radius*2, radius*2)
        geometry.Circle.__init__(self, center, radius)

        # Normalization needed for OpenGL color model (vec4([0...1]))
        self.color = normalized(getRandomColor())
        
    #Load static shaders. Since we have no fallback option if this fails, ignore all exceptions. 
    shaders=load_GLshaders()
    
    def render(self):
        self.set_colliding_flag()
        
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
        if(self.colliding):
            self.shaders.uniformf(b'borderColor', *normalized(const.COLOR_COLLIDING[self.colliding]))
        
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
        # Item is a circle
        if(type(self) is type(item)):
            return const.COLLISION_CIRCLE if geometry.check_collide_circles(self, item) else const.COLLISION_NONE
        # Item is a polygon
        elif(issubclass(type(item), geometry.Polygon)):
            return const.COLLISION_SAT if geometry.check_collide_polygon_circle(item.dots, self, item.normals) else const.COLLISION_NONE
        else:
            raise TypeError("Only shapes can be checked for collisions")
