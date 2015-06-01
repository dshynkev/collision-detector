'''
AUTHOR:         principio
LAST EDITED:	2015-06-01 00:10:17
DESCRIPTION:    Geometrical classes and algorithms
KNOWN ISSUES:   Names will collide, import by name only.
'''
import math
from copy import copy

import pyglet.graphics
import pyglet.gl
 
def get_polygon_normals(polygon):
    normals = []
    prevertex=polygon[0]
    for vertex in polygon[1:]:
        normal = Vector.fromTuple(prevertex-vertex).normal()
        normal.normalize()
        print(normal)
        normals.append(normal)
        prevertex=vertex
    return normals

def _dot(vertex, axis):
    return (vertex.x*axis.x+vertex.y*axis.y)
    
def _project(polygon, axis):
    min_point = _dot(axis, polygon[0])
    max_point = min_point    
    
    for vertex in polygon:
        current_point = _dot(vertex, axis)
        min_point = min(min_point, current_point)
        max_point = max(max_point, current_point)
    return (min_point, max_point)

def _overlap(proj1, proj2):
    return proj1[0]<=proj2[0] or proj2[1]<=proj1[1]
            

def check_collide_polygons(first, second):
    normals = first.normals+second.normals
    
    for normal in normals:
        first_p = _project(first.dots, normal)
        second_p = _project(second.dots, normal)
        
        if(not _overlap(first_p, second_p)):
            return False
    
    return True

# Non-SAT stuff starts here

def check_collide_rectangles(first, second):
        return  (((first.x>=second.x and first.x<=second.x+second.width) or    #X1...x3...X2
                    (second.x>=first.x and second.x<=first.x+first.width)) and    #x3...X1...x4
                    ((first.y>=second.y and first.y<=second.y+second.height) or    #Y1...y3...Y2
                    (second.y>=first.y and second.y<=first.y+first.height)))      #y3...Y1...y4
                
def check_collide_circles(first, second):
    dist = math.sqrt(pow(first.x-second.x, 2) + pow(first.y-second.y, 2))
    return dist <= first.radius+second.radius       #O1O2 <= R1+R2
    

class Point:
    def __init__(self, x, y):
        super().__init__()      # Needed for cooperative inheritance   
        self.x=x
        self.y=y

    @classmethod        
    def fromTuple(cls, coord_tuple):
        return cls(*coord_tuple)
        
    def __add__(self, other):
        return Point(self.x+other.x,
                self.y+other.y)
                
    def __iadd__(self, other):
        self.x+=other.x
        self.y+=other.y
        return self
        
    def __sub__(self, other):
        return Point(self.x-other.x,
                     self.y-other.y)
    
    def __isub__(self, other):
        self.x+=other.x
        self.y+=other.y
        return self        
        
    def __mul__(self, other):
        try:
            # If this type is a container, do matrix multiplication
            len(other)
            return numpy.dot(self, other)
        except:
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
    
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    
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
        self.length = math.sqrt(self.x*self.x + self.y*self.y)
    
    def isNullVector(self):
        return self.x==0 and self.y==0
    
    def normal(self):
        return Vector(self.y, -self.x)
        
    def normalize(self):
        self /= self.length
        self.length = 1

# Shapes will inherit from point, as they necessarily have a point-of-origin
class Rectangle(Point):
    def __init__(self, origin, width, height):
        super().__init__(*origin)
        self.width=width
        self.height=height
    
    def contains(self, point):
        return (self.x<=point.x) and (self.x+self.width>=point.x)\
                and (self.y<=point.y) and (self.y+self.height>=point.y) #If X1...x...X2 and Y1...y...Y2.
        
    def __repr__(self):
        return 'Bottom-left @ {0}, width={1}, height={2}'.format(super().__repr__(), self.width, self.height)
        
        
class Circle(Point):
    def __init__(self, origin, radius):
        super().__init__(*origin)
        self.radius = radius
        
    def contains(self, point):
        return (point.x-self.x)*(point.x-self.x)+(point.y-self.y)*(point.y-self.y) <= self.radius*self.radius   # (x-m)^2+(y-n)^2 <= R^2
        
    def __repr__(self):
        return 'Center @ {0}, radius={1}'.format(super().__repr__(), self.radius)

# Polygon will _not_ inherit from point: polygons have no origin        
class Polygon:
    def __init__(self, dots):
        if(dots[0] != dots[-1]):        
            dots += [copy(dots[0])]        # Append first vertex to the end, making the polygon enclosed
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
    
    # We shift a polygon by translating each point thereof by the translation vector
    def __iadd__(self, point):
        for dot in self.dots:
            dot += point
        return self
        
    def __repr__(self):
        representation = ''
        for dot in self.dots:
            representation += dot.__repr__()+'\n'
        return representation
    