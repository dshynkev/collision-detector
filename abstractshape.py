'''
AUTHOR:          principio
LAST EDITED:
DESCRIPTION:     Shape parentclass. All shapes should subclass this.
KNOWN ISSUES:
'''

class AbstractShape:
    #These methods are invoked by the main window handlers.
    #Each shape should have at least these.
    def move(self, trans):  #Immediately move to given position
        raise NotImplementedError
    def accelerate(self, vector):   #Apply given acceleration vector
        raise NotImplementedError
    def contains(self, point):
        raise NotImplementedError
    def collidedItems(self, allItems):
        collided_items=[]
        for item in allItems:
            if(not item == self and self.check_collide(item)):
                collided_items.append(item)
        return collided_items
    def check_collide(self, item):
        raise NotImplementedError
    def setCollided(self, state=True):
        raise NotImplementedError
    def render(self):
        raise NotImplementedError