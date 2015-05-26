'''
AUTHOR: 	 	principio
LAST EDITED: 	
DESCRIPTION: 	
KNOWN ISSUES: 	
'''

'''
AUTHOR:          principio
LAST EDITED:
DESCRIPTION:     Circle item class.
KNOWN ISSUES:     Not implemented.
'''

import constants as const

from helpers import *

from pyglet.graphics import draw
from pyglet.gl import *
import pyglet.image
from glhelper import *
import sys

class Circle:
    def __init__(self, center, radius):
        self.x = center[0]
        self.y = center[1]
        self.radius = radius

        #self.vertex = self._make_vertex_list()

        self.color = getRandomNormalizedColor()

        vertex=b'''#version 400
        uniform mat4 scaleMatrix;
        uniform vec2 center;
        layout(location=0) in vec2 vertex;
        out vec2 fPos;
        void main()
        {
          gl_Position = scaleMatrix * vec4(vertex+center, 0.0, 1.0);
          fPos = (vertex+center);
        }'''
        fragment=b'''#version 330
                uniform float radius;
                uniform vec2 center;
                in vec2 fPos;

                uniform vec4 circleColor;
            out vec4 fColor;

            void main()
            {
                        float dist = distance(fPos, center);
                        float delta = fwidth(dist)*1.5;
                        float alpha = smoothstep(radius-delta, radius, dist);
                        fColor = mix(circleColor, vec4(0.0, 0.0, 0.0, 0.0), alpha);
            }
        '''
        self.shader=Shader([vertex], [fragment])

    def render(self, window):
        self.shader.bind()
        scalex,scaley=window.get_size()        
        scalex = 2/scalex
        scaley = 2/scaley        
        print((-1+self.x*scalex), (-1+self.y*scaley))
        self.shader.uniformf(b'center', (-1+self.x*scalex)/(self.radius*scalex), (-1+self.y*scaley)/(self.radius*scaley))
        self.shader.uniformf(b'radius',  1)        
        self.shader.uniformf(b'circleColor',  *self.color)

        self.shader.uniform_matrixf(b'scaleMatrix', [(self.radius*scalex), 0, 0, 0,\
                                                     0, (self.radius*scaley), 0, 0,\
                                                     0, 0, 1, 0,\
                                                     0, 0, 0, 1])

        tex=pyglet.image.Texture.create(2, 2)
        tex.blit(-1, -1)
        #draw(4, GL_QUADS, ('v2f', (-0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5)))
        self.shader.unbind()
        
        

window=pyglet.window.Window(200, 200, resizable=True)
circle=Circle((100, 100), 100)

@window.event
def on_draw():
    circle.render(window)

pyglet.app.run()