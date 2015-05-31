'''
AUTHOR:          principio
LAST EDITED:	2015-05-28 22:14:58
DESCRIPTION:     Shape parentclass. All shapes should subclass this.
KNOWN ISSUES:
'''

import pyglet.app


class AbstractShape:
    # This implements general collision-related abstractions and 'declares'
    # methods that will be invoked from the main module and, therefore, have to be implemented.
    
    # Every item is defined by at least a pair of coords.
    # These coords and width and height, as far as this class is concerned,
    # delimit a bounding rect for this shape.
    # Generally, all shape-independent stuff goes here.    
    def __init__(self, x, y, width, height):
        self.bounding_x=x
        self.bounding_y=y
        self.bounding_width = width
        self.bounding_height = height

        self.colliding_items=[]
        self.colliding = False
        
    
    @classmethod
    def newScreenBounds(this, width, height):
        this.SCENE_WIDTH=width
        this.SCENE_HEIGHT=height
        
    # For an arbitrary 2D shape, parallel translation by a vector is well-defined.
    # moveTo(point), however, is not (what is the anchor point of a pentagon, for instance?)
    # Therefore, external code can only use this subroutine for shape translation.
    def moveBy(self, trans_vector):
        self._moveBy(trans_vector)      # Move the item itself
        self.moveBoundsBy(trans_vector) # Move bounding rect accordingly
        self.adjustBounds()             # Make sure the shape stays in current window
        
    def moveBoundsBy(self, trans_vector):
        self.bounding_x+=trans_vector[0]
        self.bounding_y+=trans_vector[1]
    
    # Returns whether 
    def adjustBounds(self):
        # If the item cannot fit in given bounds, give up ()
        if(self.bounding_width > self.SCENE_WIDTH
            or self.bounding_height > self.SCENE_HEIGHT):
            return False
        
        adjust_vector = [0, 0]        
        
        if(self.bounding_x<0):
            adjust_vector[0] += -self.bounding_x
        if(self.bounding_y<0):
            adjust_vector[1] += -self.bounding_y
            
        x_overflow = self.bounding_x+self.bounding_width - self.SCENE_WIDTH 
        y_overflow = self.bounding_y+self.bounding_height - self.SCENE_HEIGHT
        if(x_overflow>0):
            adjust_vector[0] += -x_overflow
        if(y_overflow>0):
            adjust_vector[1] += -y_overflow
        if(adjust_vector != [0,0]):   
            self.moveBy(adjust_vector)
        return True
    
    def getCollidingItems(self, items):
        colliding_items = []        
        for item in items:
            if item is not self and self.collidingWith(item):
                colliding_items.append(item)
        return colliding_items
    
    # item informs us that it is colliding with self. Record that.
    def adviseCollision(self, item):
        if item not in self.colliding_items:
            self.colliding_items.append(item)
        
    # Ditto, but this tells us that item is no longer colliding with self.
    def adviseNoCollision(self, item):
        if item in self.colliding_items:
            self.colliding_items.remove(item)
    
    # Get items currently colliding with self; update local item list accordingly;
    # inform other items about the collision state.    
    def updateCollisions(self, items):
        new_items=self.getCollidingItems(items)
        
        for item in self.colliding_items:
            if item not in new_items:
                item.adviseNoCollision(self)
                self.colliding_items.remove(item)
        
        for item in new_items:
            if item not in self.colliding_items:
                item.adviseCollision(self)
                self.colliding_items.append(item)