'''
AUTHOR:         principio
LAST EDITED:	2015-05-28 22:24:08
DESCRIPTION:    Polygon item class. Since rects use a different algorithm, they do not belong.
KNOWN ISSUES:
'''

from abstractshape import *

class Polygon(AbstractShape):
    def __init__(self, points):
        # Calculate bounds as minimum/maximum values of x and y for all dots
        max_x = max([x for x, y in points])
        min_x = min([x for x, y in points])
        max_y = max([y for x, y in points])
        min_y = min([y for x, y in points])
        
        # This will be the bounding box.
        super().__init__(min_x, min_y, max_x-min_x, max_y-min_y)
        
        