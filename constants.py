'''
AUTHOR:         principio
LAST EDITED:	2016-02-11 19:12:20
DESCRIPTION:    This holds the constants that pertain to this program
KNOWN ISSUES:
'''

FPS = 40    #Smooth enough on my machine, subject to decrement if drawing code becomes too bloated.

VERTEX_SHADER_SRC = "vertex.vert"
FRAGMENT_SHADER_SRC = "fragment.frag"

MAIN_TITLE = "Collision detector"
#Width could be larger, depending on the window dectorations. Let the WM handle that.
MAIN_MIN_SIZE = (100, 100)

BORDER_WIDTH = 2.0  #Outline width for colliding shapes
SMOOTH_WIDTH = 2.0  #Transition span for circles

BUTTON_WIDTH_FACTOR = 1/5
BUTTON_HEIGHT_FACTOR = 1/10

AUTO_TRANS_MAX = 300    # Maximum length of a random translation vector
AUTO_SPEED = 200/FPS    # Yes, this is ugly. No going to change anytime soon.

#The higher the number, the higher the priority when displaying
COLLISION_NONE, COLLISION_RECT, COLLISION_CIRCLE, COLLISION_SAT = 0, 1, 2, 3
CREATE_NONE, CREATE_RECT, CREATE_CIRCLE, CREATE_POLY = 0, 1, 2, 3

COLOR_WHITE = (1.0, 1.0, 1.0, 1.0)
COLOR_BLACK = (0, 0, 0, 1.0)
COLOR_RED = (1.0, 0, 0, 1.0)
COLOR_GREEN = (0, 1.0, 0, 1.0)
COLOR_BLUE = (0, 0, 1.0, 1.0)

COLOR_LOWEST = 100/255      #Lower and upper limits for color generation
COLOR_HIGHEST = 200/255
COLOR_ALPHA = 150/255       #Let alpha be uniform for all shapes
COLOR_COLLIDING = {COLLISION_RECT: COLOR_GREEN,
                   COLLISION_CIRCLE: COLOR_GREEN,
                   COLLISION_SAT: COLOR_GREEN}
COLOR_BUTTON = (0.0, 0.55, 0.45, COLOR_ALPHA)
COLOR_BUTTON_TOGGLED = (0.0, 0.35, 0.25, COLOR_ALPHA*1.2)
COLOR_BUTTON_BORDER = (0.0, 0.65, 0.55, COLOR_ALPHA)
# Pyglet.text.Label uses byte values instead of floats
COLOR_BUTTON_TEXT = (255, 255, 255, 255)
