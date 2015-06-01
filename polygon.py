'''
AUTHOR:         principio
LAST EDITED:	2015-05-31 23:36:42
DESCRIPTION:    Polygon item class. Since rects use a different algorithm, they do not belong.
KNOWN ISSUES:
'''
from helpers import getRandomColor
import constants as const
import geometry

from pyglet.gl import *
from pyglet.graphics import draw
from shape import *

class Polygon(Shape, geometry.Polygon):
    # The respresentation of a polygon is a list of dots (vertices)
    def __init__(self, dots):
        # Calculate bounds as minimum/maximum values of x and y for all dots
        max_x = max([x for x, y in dots])
        min_x = min([x for x, y in dots])
        max_y = max([y for x, y in dots])
        min_y = min([y for x, y in dots])
        
        # This will be the bounding box.
        Shape.__init__(self, geometry.Point(min_x, min_y), max_x-min_x, max_y-min_y)
        
        geometry.Polygon.__init__(self, dots)
        
        self._set_gl_vertices()
        
        self.color=getRandomColor()
    
        
    def render(self):
        self._set_gl_vertices()
        
        # Without this, number of points in polygon is undefined to pyglet.
        glEnable(GL_PRIMITIVE_RESTART)
        glPrimitiveRestartIndex(-1)
        
        glEnable(GL_LINE_SMOOTH)
        
        vertices = round(len(self.gl_vertices)/2)   
        
        draw(vertices, GL_POLYGON, ('v2f', self.gl_vertices), ('c4B', self.color*vertices))
        if(self.colliding):
            draw(vertices, GL_LINE_LOOP, ('v2f', self.gl_vertices), ('c4B', const.COLOR_COLLIDING*vertices))
        
        glDisable(GL_LINE_SMOOTH)

    
    def collidingWith(self, item):
        # First, check if bounding rects collide. If not, there is no collision.        
        #if(not geometry.check_collide_rectangles(self.bounds, item.bounds)):
        #    return False
        
        if(type(self) is type(item)):
            return geometry.check_collide_polygons(self, item)
            
    def _set_gl_vertices(self):
        self.gl_vertices = [coord for dot in self.dots for coord in dot]    # Transform list of yuples into a flat list
        self.gl_vertices += [-1, -1]     # Restart trigger for OpenGL. Repeated twice because vertex data has to be 2-aligned