'''
AUTHOR:         principio
LAST EDITED:	2016-02-11 19:12:20
DESCRIPTION:    Geometrical classes and algorithms
KNOWN ISSUES:   Names will collide, import by name only.
'''

import math
from copy import copy

# Get normals to a polygon's sides
def get_polygon_normals(polygon):
    normals = []
    prevertex=polygon[0]
    for vertex in polygon[1:]:
        normal = Vector.fromTuple(prevertex-vertex).normal()
        normal.normalize()
        normals.append(normal)
        prevertex=vertex
    return normals

# Get the only normal for circle-polygon collision (from centre to the nearest point)
def _get_circle_to_polygon_normal(polygon, circle):
    min_dist = polygon[0].dist(circle)
    closest = polygon[0]
    for dot in polygon[1:]:
        dist = dot.dist(circle)
        if(dist<min_dist):
            closest=dot
            min_dist=dist
    
    normal = Vector.fromTuple(circle-closest)
    normal.normalize()
    return [normal]

# Dot product of two 2D vectors
def dot(vector, other):
    return (vector.x*other.x+vector.y*other.y)

# Vector product (multiplied as 2x1 matrices)
def vec(vector, other):
    return Vector(vector.x*other.x, vector.y*other.y)

# Cross product of vectors OA and OB.
def cross(o, a, b):
    return (a.x-o.x)*(b.y-o.y) - (a.y-o.y)*(b.x-o.x)
    
# Project a polygon onto an axis
def _project_polygon(polygon, axis):
    min_point = dot(polygon[0], axis)
    max_point = min_point
    
    for vertex in polygon:
        current_point = dot(vertex, axis)
        min_point = min(min_point, current_point)
        max_point = max(max_point, current_point)
        
    return (min_point, max_point)

def _project_circle(circle, axis):
    center_point = dot(circle, axis)
    min_point = center_point-circle.radius
    max_point = center_point+circle.radius
    return (min_point, max_point)

# Check if two projections overlap
def _overlap(proj1, proj2):
    # ...1[0]....2[0]....1[1].....2[1] is when polygons overlap.
    # Then, the signs of difference between each .[0] and .[1] are the same
    d1 = proj1[0]-proj2[1]
    d2 = proj2[0]-proj1[1]
    return (d1*d2>0)
            


def check_collide_polygons(first, second, first_normals, second_normals):
    normals = first_normals + second_normals
    
    for normal in normals:
        first_p = _project_polygon(first, normal)
        second_p = _project_polygon(second, normal)
        
        if(not _overlap(first_p, second_p)):
            return False
    
    return True

def check_collide_polygon_circle(polygon, circle, polygon_normals):
    normals = polygon_normals + _get_circle_to_polygon_normal(polygon, circle)
    
    for normal in normals:
        polygon_p = _project_polygon(polygon, normal)
        circle_p = _project_circle(circle, normal)
        
        if(not _overlap(polygon_p, circle_p)):
            return False
        
    return True

# Non-SAT stuff starts here

# Convex hull of a set of points, stolen from Wikibooks ftw
def convex_hull(dots):
    # Do nothing for non-polygons
    if(len(dots)<3):
        return dots

    # Remove duplicates and sort as tuples
    dots = sorted(set(dots), key=lambda a: (a.x, a.y))
    
    upper_hull = []
    lower_hull=[]
    
    for dot in dots:
        # If the angle is counter-clockwise, pop the outliers off
        while(len(upper_hull) >=2 and cross(upper_hull[-2], upper_hull[-1], dot) <= 0):
            upper_hull.pop()
        upper_hull.append(dot)
        
    for dot in reversed(dots):
        # Ditto, but in opposite direction
        while(len(lower_hull) >=2 and cross(lower_hull[-2], lower_hull[-1], dot) <= 0):
            lower_hull.pop()
        lower_hull.append(dot)
    
    return lower_hull[:-1] + upper_hull[:-1]

def check_collide_rectangles(first, second):
        return  (((first.x>=second.x and first.x<=second.x+second.width) or    #X1...x3...X2
                    (second.x>=first.x and second.x<=first.x+first.width)) and    #x3...X1...x4
                    ((first.y>=second.y and first.y<=second.y+second.height) or    #Y1...y3...Y2
                    (second.y>=first.y and second.y<=first.y+first.height)))      #y3...Y1...y4
                
def check_collide_circles(first, second):
    return first.dist(second) <= first.radius+second.radius       #O1O2 <= R1+R2
    

class Point:
    def __init__(self, x, y):
        super().__init__()      # Needed for cooperative inheritance   
        self.x=x
        self.y=y

    @classmethod        
    def fromTuple(cls, coord_tuple):
        return cls(*coord_tuple)
    
    def dist(self, other):
        return math.sqrt((self.x-other.x)*(self.x-other.x)+(self.y-other.y)*(self.y-other.y))
        
    def __add__(self, other):
        try:
            return Point(self.x+other.x,
                            self.y+other.y)            
        except:
            # If other has no (x,y), assume it's scalar
            return Point(self.x+other, self.y+other)
                
    def __iadd__(self, other):
        try:
            self.x += other.x
            self.y += other.y
        except AttributeError:
            self.x += other
            self.y += other
        return self
        
    def __sub__(self, other):
        try:
            return Point(self.x-other.x,
                         self.y-other.y)
        except AttributeError:
            # If other has no (x,y), assume it's scalar 
            return Point(self.x-other, self.y-other)
    
    def __isub__(self, other):
        try:
            self.x -= other.x
            self.y -= other.y
        except:
            self.x -= other
            self.y -= other
        return self        
        
    def __mul__(self, other):
        try:
            # If this type is a container, do matrix multiplication
            return vec(self, other)
        except AttributeError:
            # Else, assume that other is scalar
            return Point(self.x*other, self.y*other)

    def __imul__(self, other):
        self = self*other
        return self
            
    def __truediv__(self, other):
        return Point(self.x/other, self.y/other)
        
    def __itruediv__(self, other):
        self.x/=other
        self.y/=other
        return self
    
    def __iter__(self):
        self.index=-1     
        return self
        
    def __next__(self):
        if(self.index<1):
            self.index+=1
            return self[self.index]
        else:
            raise StopIteration
    
    def __getitem__(self, index):
        if(index==0):
            return self.x
        elif(index==1):
            return self.y

    def __len__(self):
        return 2
    
    def __repr__(self):
        return '({0},{1})'.format(self.x, self.y)
        
# Vector are the same as points, for the purposes of this
class Vector(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._updateLength()
        
    def __iadd__(self, other):
        self=super().__iadd__(other)
        self._updateLength()
        return self
    
    def __isub__(self, other):
        self=super().__isub__(other)
        self._updateLength()
        return self
        
    def __imul__(self, other):
        self=super().__imul__(other)
        self._updateLength()
        return self
        
    def __itruediv__(self, other):
        self=super().__itruediv__(other)
        self._updateLength()
        return self
        
    def _updateLength(self):
        self.length = math.sqrt(self.x*self.x + self.y*self.y)
    
    def isNullVector(self):
        return self.x==0 and self.y==0
    
    def shortenBy(self, vector):
        self.x -= -vector.x if (self.x>0) != (vector.x>0) else vector.x
        self.y -= -vector.y if (self.y>0) != (vector.y>0) else vector.y
        self._updateLength()
    
    def normal(self):
        return Vector(self.y, -self.x)
        
    def normalize(self):
        if(self.length>0):
            self /= self.length
            self.length = 1
    
    def normalized(self):
        proxy=copy(self)
        proxy.normalize()
        return proxy

# Shapes will inherit from point, as they necessarily have a point-of-origin
class Rectangle(Point):
    def __init__(self, origin, width, height):
        super().__init__(*origin)
        self.width=width
        self.height=height
        
    setTo = __init__
    
    def contains(self, point):
        return (self.x<=point.x) and (self.x+self.width>=point.x)\
                and (self.y<=point.y) and (self.y+self.height>=point.y) #If X1...x...X2 and Y1...y...Y2.
                
    def __repr__(self):
        return 'Bottom-left @ {0} width={1} height={2}\n'.format(super().__repr__(), self.width, self.height)
        
        
class Circle(Point):
    def __init__(self, origin, radius):
        super().__init__(*origin)
        self.radius = radius
        
    def contains(self, point):
        return (point.x-self.x)*(point.x-self.x)+(point.y-self.y)*(point.y-self.y) <= self.radius*self.radius   # (x-m)^2+(y-n)^2 <= R^2
        
    def __repr__(self):
        return 'Center @ {0} radius={1}\n'.format(super().__repr__(), self.radius)

# Polygon will _not_ inherit from point: polygons have no origin        
class Polygon:
    def __init__(self, dots):
        if(dots[0] != dots[-1]):        
            dots.append(copy(dots[0]))        # Append first vertex to the end, making the polygon enclosed
        self.dots = dots
        self.normals = get_polygon_normals(self.dots)
        
    # Determine if the point tested lies within the polygon.
    # The algorithm is simple: for each two consecutive vertices of the polygon, we obtain
    # the equation for the line that contains the segment delimited by these two points:
    # (y-y1)    (x-x1)             (y-y1)
    # ------- = -------; Then X =  ------- * (x2-x1) + x1 is the equation for when X lies on the line.
    # (y2-y1)   (x2-x1)            (y2-y1)
    #
    # Therefore, X <> ... signifies cases when the point lies off on the side with respect to the line.
    # We consider all segments that have the examined point in their y-range. If the number of segments
    # for which the point lies on the same side is even, the point lies within the polygon.
    def contains(self, point):
        # But first, check if bounding rect contains the point.
        if(not self.bounds.contains(point)):
            return False
        
        prevertex = self.dots[-1]

        inside = False        
        
        for vertex in self.dots:
            if(((vertex.y>point.y) != (prevertex.y>point.y))  # Y1...y...Y2
                and (point.x < (prevertex.x-vertex.x)*(point.y-vertex.y)/(prevertex.y-vertex.y) + vertex.x)):
                    inside = not inside
            prevertex=vertex
        return inside
        
    @classmethod
    def fromRectangle(cls, origin, width, height):
        instance = cls([Point(origin.x, origin.y), Point(origin.x, origin.y+height), 
                    Point(origin.x+width, origin.y+height), Point(origin.x+width, origin.y)])
        instance.rectangle = True
        instance.width = width
        instance.height = height
        instance.x, instance.y = instance.dots[0]
        return instance
    
    def updateFromRectangle(self):
        try:
            Polygon.__init__(self, [Point(self.x, self.y), Point(self.x, self.y+self.height), 
                    Point(self.x+self.width, self.y+self.height), Point(self.x+self.width, self.y)])
        except:
            pass
                    
    @classmethod
    def fromList(cls, lst):
        return cls(list(map(Point.fromTuple, lst)))
        
    def add_point(self, point):
        self.dots.insert(len(self.dots)-1, point)
        self.dots = convex_hull(self.dots)
        self.dots.append(copy(self.dots[0]))
        self.updateBounds()
        self.normals = get_polygon_normals(self.dots)
    
    def get_gl_vertices(self):
        vertices = [coord for dot in self.dots for coord in dot]    # Transform list of tuples into a flat list
        vertices += [-1, -1]     # Restart trigger for OpenGL. Repeated twice because vertex data has to be 2-aligned
        return vertices
    
    # We shift a polygon by translating each point thereof by the translation vector
    def __iadd__(self, point):
        for dot in self.dots:
            dot += point
        return self

    def __isub__(self, point):
        for dot in self.dots:
            dot -= point
        return self
        
    def __repr__(self):
        representation = '\n'
        for dot in self.dots:
            representation += dot.__repr__()+'\n'
        return representation
    