'''
AUTHOR: 	 	principio
LAST EDITED:	2015-06-04 22:23:32
DESCRIPTION: 	Button class for UI
KNOWN ISSUES: 	*> Barely tested
'''

import constants as const

import pyglet
from pyglet.graphics import draw
from pyglet.gl import GL_QUADS, GL_LINE_LOOP, glColor4f

class Button:
    ''' Params:
        text - the text to display
        x, y - lower bottom point
        width, height - dimensions of the button
        oncallback, offcallback - callback functions to be called when the button is toggled on/off
        *_params - params to pass to the respective functions
    '''
    def __init__(self, text, x, y, width, height, oncallback=lambda:None, oncallback_param=[], offcallback=lambda:None, offcallback_param=[], toggled=False):
        self.text = text
        self.setCoords(x, y, width, height)
        self.toggled = toggled
        self.oncallback = oncallback
        self.oncallback_param = oncallback_param
        self.offcallback = offcallback
        self.offcallback_param = offcallback_param
    
    # Tell that a click was performed. The button will claim it (returning True) or reject it (False)
    def tellClicked(self, x, y):
        # IF bound containt the point
        if (self.x<=x) and (self.x+self.width>=x)\
                and (self.y<=y) and (self.y+self.height>=y):
                    self.toggled = not self.toggled
                    if(self.toggled):
                        self.oncallback(*self.oncallback_param)
                    else:
                        self.offcallback(*self.offcallback_param)
                    return True
        return False
                        
    def setCoords(self, x, y, width, height):
        self.x, self.y = x,y
        self.height, self.width = height, width
        # The label is centered
        self.label = pyglet.text.Label(self.text, color=const.COLOR_BUTTON_TEXT, 
                                       x=x+width/2, y=y+height/2,
                                       anchor_x='center', anchor_y='center')                            
        self.gl_vertices = [self.x, self.y, self.x+width, self.y,
                            self.x+width, self.y+height, self.x, self.y+height]
    
    def render(self):
        if(self.toggled):
            glColor4f(*const.COLOR_BUTTON_TOGGLED)
        else:
            glColor4f(*const.COLOR_BUTTON)
        draw(4, GL_QUADS, ('v2f', self.gl_vertices))
        glColor4f(*const.COLOR_BUTTON_BORDER)
        draw(4, GL_LINE_LOOP, ('v2f', self.gl_vertices))
        self.label.draw()
        