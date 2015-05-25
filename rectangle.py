'''
AUTHOR: 	 	principio
LAST EDITED:
DESCRIPTION: 	Rectangle item class.
KNOWN ISSUES: 	
'''

import constants as const

from helpers import getRandomColor

from pyglet.graphics import draw
from pyglet.gl import GL_QUADS, glColor4f

class Rectangle:
	def __init__(self, origin, width, height):
		self.x, self.y = origin
		self.width = width
		self.height = height
		
		self.vertex = self._make_vertex_list()
				
				
		self.color = getRandomColor()
		
	
	def render(self):
		draw(4, GL_QUADS, ('v2f', self.vertex), ('c4B', self.color*4))	#4x 2D vertices
		
	def contains(self, point):
		return (self.x<point[0]) and (self.x+self.width>point[0])\
				and (self.y<point[1]) and (self.y+self.height>point[1])
	
	def move(self, trans):
		self.x+=trans[0]
		self.y+=trans[1]
		self.vertex=self._make_vertex_list()
		
	def _make_vertex_list(self):
		return (self.x, self.y,	#4 vertices clockwise
				self.x+self.width, self.y,
				self.x+self.width, self.y+self.height,
				self.x, self.y+self.height)