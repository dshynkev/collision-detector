'''
AUTHOR:          principio
LAST EDITED:	2015-06-04 21:33:47
DESCRIPTION:     Shape parentclass. All shapes should subclass this.
KNOWN ISSUES:   
'''
import constants as const
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
        
        self.collisions=[]
        self.colliding = 0        
    
    @classmethod
    def tellScreenBounds(this, width, height):
        this.SCENE_START_HEIGHT = height*const.BUTTON_HEIGHT_FACTOR
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
            adjust_vector.x = -self.bounds.x
        if(self.bounds.y<self.SCENE_START_HEIGHT):
            adjust_vector.y = self.SCENE_START_HEIGHT-self.bounds.y
        
        # Upper/right edges
        x_overflow = self.bounds.x+self.bounds.width - self.SCENE_WIDTH 
        y_overflow = self.bounds.y+self.bounds.height - self.SCENE_HEIGHT
        if(x_overflow>0):
            adjust_vector.x = -x_overflow
        if(y_overflow>0):
            adjust_vector.y = -y_overflow
        
        if(not adjust_vector.isNullVector()):   
            self.moveBy(adjust_vector)
        return True
    
    
    def getCollidingItems(self, items):
        collisions = []   
        for item in items:
            if item is not self:
                collision_type = self.collidingWith(item)
                if(collision_type != const.COLLISION_NONE):
                    collisions.append((item, collision_type))
        return collisions
    
    # item informs us that it is colliding with self. Record that.
    def adviseCollision(self, item, coltype):
        if (item, coltype) not in self.collisions:
            self.collisions.append((item, coltype))
        
    # Ditto, but this tells us that item is no longer colliding with self.
    def adviseNoCollision(self, item):
        # By iterating through all collision records,
        for collision in self.collisions:
            # Find the one where the items matches the advice sender
            if(collision[0] is item):
                self.collisions.remove(collision)
    
    # Get items currently colliding with self; update local item list accordingly;
    # inform other items about the collision state.    
    def updateCollisions(self, items):      
        new_collisions=self.getCollidingItems(items)
        
        for collision in self.collisions:
            if collision not in new_collisions:
                collision[0].adviseNoCollision(self)
                self.collisions.remove(collision)

        for collision in new_collisions:
            if collision not in self.collisions:
                collision[0].adviseCollision(self, collision[1])
                self.collisions.append(collision)
                
    # Before actually rendering anything, set the colliding flag appropriately.       
    def set_colliding_flag(self):
        self.colliding = const.COLLISION_NONE
        
        for item, coltype in self.collisions:
            self.colliding = coltype if coltype > self.colliding else self.colliding