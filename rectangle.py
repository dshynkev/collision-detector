'''
AUTHOR:         principio
LAST EDITED:	
DESCRIPTION:    Rectangle item class.
KNOWN ISSUES:
'''

import constants as const

from helpers import getRandomColor
import geometry

from pyglet.graphics import draw
from pyglet.gl import GL_QUADS, GL_LINE_LOOP, glLineWidth, glColor4f
from shape import Shape

class Rectangle(Shape, geometry.Rectangle):
    def __init__(self, origin, width, height):
        Shape.__init__(self, origin, width, height)
        geometry.Rectangle.__init__(self, origin, width, height)
        
        self.color = getRandomColor()

    def render(self):     
        self.set_colliding_flag()
        
        # Generate vertex list
        self.vertex=self._make_vertex_list()
        
        draw(4, GL_QUADS, ('v2f', self.vertex), ('c4B', self.color*4))  #4x 2D vertices with colors
        if(self.colliding):
            glLineWidth(const.BORDER_WIDTH)
            draw(4, GL_LINE_LOOP, ('v2f', self.vertex), ('c4B', const.COLOR_COLLIDING[self.colliding]*4))  #If colliding, draw a border
            
    def collidingWith(self, item):
        if(type(self) is type(item)):
            return const.COLLISION_RECT if geometry.check_collide_rectangles(self, item) else const.COLLISION_NONE
        else:
            return const.COLLISION_NONE
    
    # Return 4 vertices counterlockwise.
    def _make_vertex_list(self):
        return (self.x, self.y,
                self.x+self.width, self.y,
                self.x+self.width, self.y+self.height,
                self.x, self.y+self.height)
