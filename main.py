'''
AUTHOR:         principio
LAST EDITED:	2015-05-31 23:37:09
DESCRIPTION:    This is the main class of a simple collision detection demo
                written in Python (Pyglet framework). 
KNOWN ISSUES:   *> Segfaults on the only Windows machine I have at my disposal. Appears to be a Python issue.
                *> On Linux/X11, going fullscreen will sometimes mess up the picture. Dragging any item helps.
'''

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import constants as const

from rectangle import *
from circle import *
from polygon import *

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(resizable=True)    # Seemingly no way to toggle resizability
                                            # without passing the flag to parent constructor
        self.maximize()             # Start maximized

        self.set_minimum_size(*const.MAIN_MIN_SIZE)
        self.set_caption(const.MAIN_TITLE)
        self.fullscreen_flag = False

        # Blend alpha so that the more shapes overlap, the less transparent the intersection area.
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        pyglet.clock.set_fps_limit(const.FPS)

        self.items = []             # All items rendered within this window
        self.dragged_items = []     # Items being dragged at the moment
        self.multidrag_flag=True    # Whether all overlapping items or only the uppermost one shoulds be dragged.

    def add_item(self, item):
        if(issubclass(type(item), Shape)):
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
            for item in self.items[::-1]:   #Start with the uppermost item
                if(item.contains(geometry.Point(x, y))):
                    self.dragged_items.append(item)
                    if(not self.multidrag_flag):    # If no multidrag, return when found the uppermost selected item
                        return True
    
    # Moves selected items with the cursor. Performance would benefit from, moving the
    # collision detection to on_draw(), since no one cares about collisions unless
    # they are indicated during rendering, but there is a _miniscule_ chance
    # that the button will be realeased in between two on_draw()'s. Better play it safe.
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for item in self.dragged_items:
            item.moveBy(geometry.Vector(dx, dy))
        self.check_collisions(self.dragged_items)

    def on_mouse_release(self, x, y, button, modifiers):
        if(button ==  mouse.LEFT):        
            self.dragged_items.clear()

    def on_key_press(self, symbol, modifiers):
        if(modifiers and key.MOD_CTRL):
            # On CTRL+F, toggle fullscreen
            if(symbol == key.F):
                self.fullscreen_flag = not self.fullscreen_flag
                self.set_fullscreen(self.fullscreen_flag)
            # On CTRL+M, toggle multidrag
            if(symbol == key.M):
                self.multidrag_flag = not self.multidrag_flag
            # On CTRL+Q, exit
            if(symbol == key.Q):
                window.dispatch_event('on_close')
        # On Delete, remove all items that are currently being dragged
        if(symbol == key.DELETE):
            for item in self.dragged_items:
                self.items.remove(item)
            self.check_collisions(self.items)
        # Dispatch default closing event on Escape.
        if(symbol == key.ESCAPE):
            window.dispatch_event('on_close')
            
    def on_resize(self, width, height):
        # Resize GL viewport
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW) 
        
        # Inform all items of the new dimensions and adjust their positions accordingly
        Shape.newScreenBounds(width, height)
        for item in self.items:
            item.adjustBounds()
        

if (__name__=="__main__"):
    window = MainWindow()
    window.add_item(Rectangle(geometry.Point(10, 10), 200, 300))
    window.add_item(Rectangle(geometry.Point(20, 20), 100, 120))
    window.add_item(Rectangle(geometry.Point(50, 50), 400, 200))
    window.add_item(Circle(geometry.Point(150, 150), 100))
    window.add_item(Circle(geometry.Point(250, 250), 300))
    #window.add_item(Polygon(list(map(geometry.Point.fromTuple, [[250, 250], [200, 300], [150, 200], [200, 50], [250, 0]]))))
    window.add_item(Polygon(list(map(geometry.Point.fromTuple, [[400, 300], [300, 300], [350, 400]]))))
    window.add_item(Polygon(list(map(geometry.Point.fromTuple, [[400, 200], [400, 400], [600, 400], [600, 200]]))))
    pyglet.app.run()
