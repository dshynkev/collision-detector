'''
AUTHOR:         principio
LAST EDITED:	2016-02-11 19:12:20
DESCRIPTION:    This is the main class of a simple collision detection demo
                written in Python (Pyglet framework). 
KNOWN ISSUES:   *> Segfaults on the only Windows machine I have at my disposal. Appears to be a Python issue.
                *> On Linux/X11, going fullscreen will sometimes mess up the picture. Dragging any item helps.
'''

import pyglet
import pyglet.gl as gl
from pyglet.window import key, mouse

import constants as const
import helpers
import geometry

from shape import Shape
from circle import Circle
from polygon import Polygon

from button import Button

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(resizable=True)    # Seemingly no way to toggle resizability
                                            # without passing the flag to parent constructor
        self.maximize()             # Start maximized

        self.set_minimum_size(*const.MAIN_MIN_SIZE)
        self.set_caption(const.MAIN_TITLE)

        # Blend alpha so that the more shapes overlap, the less transparent the intersection area.
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        pyglet.clock.set_fps_limit(const.FPS)

        self.items = []             # All items rendered within this window
        self.dragged_items = []     # Items being dragged at the moment
        self.move_vectors = {}      # Vectors for random movement
        
        self.fullscreen_flag = False
        self.multidrag_flag = True  # Whether all overlapping items or only the uppermost one should be dragged.
        self.random_move_flag = False # Whether shapes should be automatically moved
        
        self.creation_flags = const.CREATE_NONE
        # This will be popped off when needed
        self.push_handlers(on_mouse_press = self.select_items,
                           on_mouse_drag = self.drag_items,
                           on_mouse_release = self.release_items)
        self.push_handlers(on_mouse_press = self.check_buttons)
        self.update_buttons()

    def add_item(self, item):
        if(issubclass(type(item), Shape)):
            self.items.append(item)
            self.check_collisions([item])
        else:
            raise NotImplementedError("Only Shape subclasses can be added to this scene.")
            
    def update_buttons(self):
        width = self.width*const.BUTTON_WIDTH_FACTOR
        height = self.height*const.BUTTON_HEIGHT_FACTOR
        self.buttons=[Button('Add rectangles', 0, 0, width, height, self.begin_creation, [const.CREATE_RECT], self.end_creation),
              Button('Add circles', width, 0, width, height, self.begin_creation, [const.CREATE_CIRCLE], self.end_creation),
              Button('Add polygons', 2*width, 0, width, height, self.begin_creation, [const.CREATE_POLY], self.end_creation),
              Button('Enable random motion', 3*width, 0, width, height, self.toggle_random, [], self.toggle_random, []),
              Button('Enable multidrag', 4*width, 0, width, height, self. toggle_multidrag, [], self.toggle_multidrag, [], True)]
    
    def check_collisions(self, items):
        for item in items:
            item.updateCollisions(self.items)
        
    def toggle_random(self):
        self.random_move_flag = not self.random_move_flag
        if(self.random_move_flag):
            pyglet.clock.schedule(self.random_move)
        else:
            pyglet.clock.unschedule(self.random_move)
            
    def toggle_multidrag(self): 
        self.multidrag_flag = not self.multidrag_flag
        
    # Move items randomly by pre-generated vectors.
    def random_move(self, dt):
        for item in self.items:
            try:
                vector = self.move_vectors[id(item)]
            except:
                # If the vector does not exist yet, create it
                vector = geometry.Vector.fromTuple(helpers.getRandomTranslation())
                self.move_vectors[id(item)] = vector
             
            # IF the vector has been shortened by too much, make a new one
            if(vector.length < const.AUTO_SPEED):
                vector = geometry.Vector.fromTuple(helpers.getRandomTranslation())
                self.move_vectors[id(item)] = vector
            
            # Current transition vector is computed from the direction of the 
            # principal transition vector and predefined speed
            current_trans = vector.normalized() * const.AUTO_SPEED
            item.moveBy(current_trans)
            # We decrement the translation vector by current vector
            vector.shortenBy(current_trans)
        
        self.check_collisions(self.items)
            
    def on_draw(self):
        self.clear()
        for button in self.buttons:
            button.render()
        for item in self.items:
            item.render()
            
    def on_resize(self, width, height):
        # Resize GL viewport
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW) 
        
        # Inform all items of the new dimensions and adjust their positions accordingly
        Shape.tellScreenBounds(width, height)
        for item in self.items:
            item.adjustBounds()
            
        # Update button positions: they are supposed to be dynamically sized
        self.update_buttons()
        
    def check_buttons(self, x, y, button, modifiers):
        status = False      
        if(button ==  mouse.LEFT):
            for button in self.buttons:
                status |= button.tellClicked(x, y)
            if(status):
                return True     # Don't let anyone else handle this event            

    # Builds a list of items that could be dragged after this mouse_press.
    # Caveat: only these items are deemed to be "selected", i.e. deletion etc
    # can only be invoked on them while they are being dragged.
    def select_items(self, x, y, button, modifiers):
        for item in self.items[::-1]:   #Start with the uppermost item
            if(item.contains(geometry.Point(x, y))):
                self.dragged_items.append(item)
                if(not self.multidrag_flag):    # If no multidrag, return when found the uppermost selected item
                    return True
    
    # Moves selected items with the cursor. Performance would benefit from moving the
    # collision detection to on_draw(), since no one cares about collisions unless
    # they are indicated during rendering, but there is a _miniscule_ chance
    # that the button will be realeased in between two on_draw()'s. Better play it safe.
    def drag_items(self, x, y, dx, dy, buttons, modifiers):
        for item in self.dragged_items:
            item.moveBy(geometry.Vector(dx, dy))
        self.check_collisions(self.dragged_items)

    # Clears the list of items
    def release_items(self, x, y, button, modifiers):
        if(button ==  mouse.LEFT):        
            self.dragged_items.clear()

    # Handle key presses.
    def on_key_press(self, symbol, modifiers):
        if(modifiers and key.MOD_CTRL):
            # On CTRL+F, toggle fullscreen
            if(symbol == key.F):
                self.fullscreen_flag = not self.fullscreen_flag
                self.set_fullscreen(self.fullscreen_flag)
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
            
    def begin_creation(self, shape):
        # Pop all handlers off and delete previous item reference  
        try:
            while 1:
                self.pop_handlers()
        except:
            pass
        try:
            del self.temp_item
        except:
            pass
        
        # Set the flag and push appropriate handlers
        self.creation_flags = shape
        if(self.creation_flags == const.CREATE_RECT):
            self.push_handlers(on_mouse_press = self.rect_on_click,
                                       on_mouse_drag = self.rect_on_drag,
                                       on_mouse_release = self.rect_on_release)
        elif(self.creation_flags == const.CREATE_CIRCLE):
            self.push_handlers(on_mouse_press = self.circle_on_click,
                                       on_mouse_drag = self.circle_on_drag,
                                       on_mouse_release = self.circle_on_release)
        elif(self.creation_flags == const.CREATE_POLY):
            self.push_handlers(on_mouse_press = self.polygon_on_click)
            
        # Push UI handlers on the top
        self.push_handlers(on_mouse_press = self.check_buttons)
    
    def end_creation(self):
        # Complete the polygon
        if(self.creation_flags == const.CREATE_POLY):
            if(len(self.temp_item.dots) <= 3):
                self.items.remove(self.temp_item)
                del self.temp_item
        # Pop all handlers
        try:
            while 1:
                self.pop_handlers()
        except:
            pass
        # Push itemdrag handlers
        self.push_handlers(on_mouse_press = self.select_items,
                   on_mouse_drag = self.drag_items,
                   on_mouse_release = self.release_items)
        # Push UI handler
        self.push_handlers(on_mouse_press = self.check_buttons)
        self.creation_flag = const.CREATE_NONE
            
    # ~~~~~~~~~~ CIRCLE creation subroutines ~~~~~~~~~~
    def circle_on_click(self, x, y, button, modifiers):
        if(button == mouse.LEFT):
            self.temp_item = Circle(geometry.Point(x, y), 0)
            self.add_item(self.temp_item)
        
    def circle_on_drag(self, x, y, dx, dy, buttons, modifiers):
        try:
            # Radius is the distance between the starting point and current point
            self.temp_item.radius = geometry.Vector(x-self.temp_item.x, y-self.temp_item.y).length
            self.temp_item.updateBounds()
            self.check_collisions([self.temp_item])
        except AttributeError:
            pass
        
    def circle_on_release(self, x, y, button, modifiers):
        try:
            if(button == mouse.LEFT):
                # Don't store zero-width circles
                if (self.temp_item.radius == 0):
                    self.items.remove(self.temp_item)
                del self.temp_item
        except AttributeError:
            pass
        
    # ~~~~~~~~~~ RECTANGLE creation subroutines ~~~~~~~~~~
    def rect_on_click(self, x, y, button, modifiers):
        if(button == mouse.LEFT):
            self.temp_item = Polygon.fromRectangle(geometry.Point(x, y), 0, 0)
            self.add_item(self.temp_item)
    
    def rect_on_drag(self, x, y, dx, dy, buttons, modifiers):
        try:
            self.temp_item.width += dx
            self.temp_item.height += dy
            self.temp_item.updateFromRectangle()
            self.temp_item.updateBounds()
            self.check_collisions([self.temp_item])
        except AttributeError:
            pass
        
    def rect_on_release(self, x, y, button, modifiers):
        try:            
            if(button == mouse.LEFT):
                # Don't store zero-width/height rectangles
                if (self.temp_item.width == 0 or self.temp_item.height == 0):
                    self.items.remove(self.temp_item)
                del self.temp_item
                return True
        except AttributeError:
            pass
        
    # ~~~~~~~~~~ POLYGON creation subroutines ~~~~~~~~~~
    def polygon_on_click(self, x, y, button, modifiers):
        if(button == mouse.LEFT):
            if(not hasattr(self, 'temp_item')):
                self.temp_item = Polygon([geometry.Point(x, y)])
                self.add_item(self.temp_item)
            else:
                self.temp_item.add_point(geometry.Point(x, y))
            self.check_collisions([self.temp_item])
        
if (__name__=="__main__"):
    window = MainWindow()
    pyglet.app.run()
