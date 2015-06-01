'''
AUTHOR:          principio
LAST EDITED:	2015-05-31 22:36:37
DESCRIPTION:     Shape parentclass. All shapes should subclass this.
KNOWN ISSUES:
'''

import geometry

class Shape:
    # This implements general collision-related abstractions and 'declares'
    # methods that will be invoked from the main module and, therefore, have to be implemented.
    
    #These are specific to a particular shape and are implemeted in subclasses.
    '''
    def contains(self, point)               #[V] Will be pulled in from geometry.*
    def render(self)
    def collidingWith(self, item)
    '''   
    
    # Every item is defined by at least a pair of coords.
    # These coords and width and height, as far as this class is concerned,
    # delimit a bounding rect for this shape.
    # Generally, all shape-independent stuff goes here.    
    def __init__(self, origin, width, height):
        self.bounds = geometry.Rectangle(origin, width, height)
        
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
        # If the item cannot fit in given bounds, restrict movement.
        if(self.bounds.width > self.SCENE_WIDTH
            or self.bounds.height > self.SCENE_HEIGHT):
            return False
        
        self += trans_vector      # Move the item itself
        self.bounds += trans_vector # Move bounding rect accordingly
        self.adjustBounds()             # Make sure the shape stays in current window
        
    
    # Returns whether 
    def adjustBounds(self):
        adjust_vector = geometry.Vector(0, 0)    
        
        # Lower/left edges
        if(self.bounds.x<0):
            adjust_vector.x += -self.bounds.x
        if(self.bounds.y<0):
            adjust_vector.y += -self.bounds.y
        
        # Upper/right edges
        x_overflow = self.bounds.x+self.bounds.width - self.SCENE_WIDTH 
        y_overflow = self.bounds.y+self.bounds.height - self.SCENE_HEIGHT
        if(x_overflow>0):
            adjust_vector.x += -x_overflow
        if(y_overflow>0):
            adjust_vector.y += -y_overflow
        
        if(not adjust_vector.isNullVector()):   
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
        # If more than one colliding item, set the respective flag
        self.colliding = (len(self.colliding_items) > 0)
        
    # Ditto, but this tells us that item is no longer colliding with self.
    def adviseNoCollision(self, item):
        if item in self.colliding_items:
            self.colliding_items.remove(item)
        # If more than one colliding item, set the respective flag
        self.colliding = (len(self.colliding_items) > 0)
    
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
                
        # If more than one colliding item, set the respective flag
        self.colliding = (len(self.colliding_items) > 0)