'''
AUTHOR:         principio
LAST EDITED:	2015-05-28 22:24:08
DESCRIPTION:    SAT colllision detection utilities
KNOWN ISSUES:   Not implemented.
'''

# 
def _get_polygon_normals(polygon):
    normals = []
    for v1, v2 in polygon:
        normal = (v1[0]-v2[0], v1[1]-v2[1])
        normal = (-normal[1], normal[0])
        normals.append(normal)
    return normals

def check_collide_polygons(first, second):
    axes_first = _get_polygon_normals(first)