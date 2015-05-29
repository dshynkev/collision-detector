'''
AUTHOR:          principio
LAST EDITED:	2015-05-28 22:14:58
DESCRIPTION:     Shape parentclass. All shapes should subclass this.
KNOWN ISSUES:
'''

class AbstractShape:
    # This implements general collision-related abstractions and 'declares'
    # methods that will be invoked from the main module and, therefore, have to be implemented.
    
    # Every item is defined by at least a pair of coords.
    # Generally, all shape-independent stuff goes here.    
    def __init__(self, x, y):
        self.x=x
        self.y=y

        self.colliding_items=[]
        self.colliding = False
    
    def move(self, trans):
        self.x+=trans[0]
        self.y+=trans[1]
        
    def accelerate(self, vector):
        raise NotImplementedError
    def contains(self, point):
        raise NotImplementedError
    def collidingWith(self, item):
        raise NotImplementedError
    
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
    
    def render(self):
        raise NotImplementedError