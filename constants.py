'''
AUTHOR:         principio
LAST EDITED:	2015-05-31 23:06:26
DESCRIPTION:    This holds the constants that pertain to this program
KNOWN ISSUES:
'''

FPS = 120    #Smooth enough on my machine, subject to decrement if drawing code becomes too bloated.

VERTEX_SHADER_SRC="vertex.vert"
FRAGMENT_SHADER_SRC="fragment.frag"

MAIN_TITLE="Collision detector"
MAIN_MIN_SIZE = (100, 100)  #Width could be larger, depending on the window dectorations. Let the WM handle that.

BORDER_WIDTH = 2.0  #Outline width for colliding shapes
SMOOTH_WIDTH = 2.0  #Transition span for circles

COLOR_WHITE = (255, 255, 255, 255)
COLOR_BLACK = (0, 0, 0, 255)
COLOR_RED = (255, 0, 0, 255)

COLOR_LOWEST = 100      #Lower and upper limits for color generation
COLOR_HIGHEST = 200
COLOR_ALPHA = 177       #Let alpha be uniform for all shapes
COLOR_COLLIDING = COLOR_RED    #The color for when shapes collide
