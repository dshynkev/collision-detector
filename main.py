'''
AUTHOR:         principio
LAST EDITED:	2015-05-28 23:51:44
DESCRIPTION:    This is the main class of a simple collision detection demo
                written in Python (Pyglet framework). 
KNOWN ISSUES:   Implementation imcomplete.
'''


import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import constants as const

from rectangle import *
from circle import *

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(resizable=True)    # Seemingly no way to toggle resizability
                                            # without passing the flag to parent constructor
        self.maximize()             # Start maximized

        self.set_minimum_size(const.MAIN_MIN_SIZE[0], const.MAIN_MIN_SIZE[1])
        self.set_caption(const.MAIN_TITLE)
        self.fullscreen_flag = False

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)       # Blend alpha so that the more shapes overlap, the less transparent the intersection area.

        pyglet.clock.set_fps_limit(const.FPS)

        self.items = []     # Here be all items rendered within this window
        self.dragged_items = [] #I tems being dragged by the user

    def add_item(self, item):
        if(issubclass(type(item), AbstractShape)):
            self.items.append(item)
            self.check_collisions([item])
        else:
            raise NotImplementedError("Only Shape subclasses can be added to this scene.")
    
    def check_collisions(self, items):
        for item in items:
            item.updateCollisions(self.items)

    def on_draw(self):
        self.clear()
        for item in self.items:
            item.render()

    # Builds a list of items that could be dragged after this mouse_press.
    # Caveat: only these items are deemed to be "selected", i.e. deletion etc
    # can only be invoked on them while they are being dragged.
    def on_mouse_press(self, x, y, button, modifiers):
        if(button ==  mouse.LEFT):
            for item in self.items:
                if(item.contains((x, y))):
                    self.dragged_items.append(item)
    
    # Moves selected items with the cursor. Performance would benefit from, moving the
    # collision detection to on_draw(), since no one cares about collisions unless
    # they are indicated during rendering, but there is a _miniscule_ chance
    # that the button will be realeased in between two on_draw()'s. Better play it safe.
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for item in self.dragged_items:
            item.move((dx, dy))
        self.check_collisions(self.dragged_items)

    
    def on_mouse_release(self, x, y, button, modifiers):
        if(button ==  mouse.LEFT):        
            self.dragged_items.clear()

    def on_key_press(self, symbol, modifiers):
        #On CTRL+F, toggle fullscreen
        if(modifiers and key.MOD_CTRL):
            if(symbol == key.F):
                self.fullscreen_flag = ~self.fullscreen_flag
                self.set_fullscreen(self.fullscreen_flag)
        #On delete, remove all items that are currently being dragged
        if(symbol == key.DELETE):
            for item in self.dragged_items:
                self.items.remove(item)
        #Dispatch default closing event on escape.
        if(symbol == key.ESCAPE):
            window.dispatch_event('on_close')

if (__name__=="__main__"):
    window = MainWindow()
    window.add_item(Rectangle((10, 10), 200, 300))
    window.add_item(Rectangle((20, 20), 100, 120))
    window.add_item(Rectangle((50, 50), 400, 200))
    window.add_item(Circle((150, 150), 100))
    window.add_item(Circle((350, 350), 300))
    pyglet.app.run()
