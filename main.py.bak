'''
AUTHOR: 	 	principio
LAST EDITED:
DESCRIPTION: 	This is the main class of a simple collision detection demo 
			written in Python (Pyglet framework)
KNOWN ISSUES: 	Implementation imcomplete.
'''


import sys,pyglet
from pyglet.gl import *
from pyglet.window import key, mouse 

import constants as const

from rectangle import *

class MainWindow(pyglet.window.Window):
	def __init__(self):
		super().__init__(resizable=True)    # Seemingly no way to toggle resizability
                                            # without passing the flag to parent constructor
		self.maximize()		#Start maximized
		
		self.set_minimum_size(const.MAIN_MIN_SIZE[0], const.MAIN_MIN_SIZE[1])
		self.set_caption(const.MAIN_TITLE)
		self.fullscreen_flag = False
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)	#Enable alpha blending
		
		pyglet.clock.set_fps_limit(const.FPS)
        
		self.items = []     #Here be all items rendered within this window
		self.dragged_items = []	#Items being dragged by the user    
				
	def add_item(self, item):
		if(hasattr(item, "render")):
			self.items.append(item)
			return True
		return False
    
	def on_draw(self):
		self.clear()
		for item in self.items:
			item.render()
			
	def on_mouse_press(self, x, y, button, modifiers):
		if(button ==  mouse.LEFT):		
			for item in self.items:
				if(item.contains((x, y))):
					self.dragged_items.append(item)
					
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		for item in self.dragged_items:
			item.move((dx, dy))
			
	def on_mouse_release(self, x, y, button, modifiers):
		self.dragged_items.clear()
			
	def on_key_press(self, symbol, modifiers):
		if(modifiers and key.MOD_CTRL):
			if(symbol == key.F):
				self.fullscreen_flag = ~self.fullscreen_flag
				self.set_fullscreen(self.fullscreen_flag)
		if(symbol == key.ESCAPE):
			window.dispatch_event('on_close')
			
if (__name__=="__main__"):
	window = MainWindow()
	window.add_item(Rectangle((10, 10), 200, 300))
	window.add_item(Rectangle((20, 20), 100, 200))
	pyglet.app.run()