'''
AUTHOR:         principio
LAST EDITED:
DESCRIPTION:    Rectangle item class.
KNOWN ISSUES:
'''

import constants as const

from helpers import getRandomColor

from pyglet.graphics import draw
from pyglet.gl import GL_QUADS, glColor4f
from circle import *

class Rectangle:
    def __init__(self, origin, width, height):
        self.x, self.y = origin
        self.width = width
        self.height = height

        self.vertex = self._make_vertex_list()

        self.color = getRandomColor()
        self.colliding = False

    def render(self):
        draw(4, GL_QUADS, ('v2f', self.vertex), ('c4B', self.color*4))  #4x 2D vertices
        if(self.colliding):
            draw(4, GL_LINE_LOOP, ('v2f', self.vertex), ('c4B', const.COLOR_COLLIDING*4))  #If colliding, draw a border

    def contains(self, point):
        return (self.x<=point[0]) and (self.x+self.width>=point[0])\
                        and (self.y<=point[1]) and (self.y+self.height>=point[1]) #If X1...x...X2 and Y1...y...Y2.

    def move(self, trans):
        self.x+=trans[0]
        self.y+=trans[1]
        self.vertex=self._make_vertex_list()
        
    def collidedItems(self, items):
        collided_items=[]
        for item in items:
            if(not item == self and self._check_collide(item)):
                collided_items.append(item)
        return collided_items
            
    def setCollided(self, state=True):
        self.colliding=state
            
    def _check_collide(self, item):
        if(isinstance(item, Rectangle)):
            return self._check_collide_rect(item)
        elif(isinstance(item, Circle)):
            return False    #TODO: Implement
        else:
            raise NotImplementedError("Only rectangle and circle collisions are supported.")
        
    def _check_collide_rect(self, item):
        return  (((self.x>=item.x and self.x<=item.x+item.width) or    #X1...x3...X2
                (item.x>=self.x and item.x<=self.x+self.width)) and    #x3...X1...x4
                ((self.y>=item.y and self.y<=item.y+item.height) or    #Y1...y3...Y2
                (item.y>=self.y and item.y<=self.y+self.height)))      #y3...Y1...y4

    def _make_vertex_list(self):
        return (self.x, self.y, # 4 vertices clockwise
                        self.x+self.width, self.y,
                        self.x+self.width, self.y+self.height,
                        self.x, self.y+self.height)
