'''
AUTHOR: 	 	principio
LAST EDITED: 	
DESCRIPTION: 	Circle item class.
KNOWN ISSUES: 	Not implemented.
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
		uniform mat4 mvMatrix;
		uniform mat4 pMatrix;
		layout(location=0) in vec2 vertex;
		out vec2 fPos;
		void main()
		{
		  vec4 pos = pMatrix * mvMatrix * vec4(vertex, 0.0, 1.0);
		  fPos = pos.xy;
		  gl_Position = scaleMatrix * scaleMatrix * pos;
		}'''
		fragment=b'''#version 330		
		        uniform float radius;
		        in vec2 fPos;
		        
		        uniform vec4 circleColor;
			out vec4 fColor;
			
			void main() 
			{
		                float dist = distance(fPos, vec2(0.0, 0.0));
		                float delta= fwidth(dist)*1.5;
		                float alpha = smoothstep(radius-delta, radius, dist);
		                fColor = mix(circleColor, vec4(0.0, 0.0, 0.0, 0.0), alpha);
			}
		'''
		self.shader=Shader([vertex], [fragment])
		
	def render(self, window):		
		scalex, scaley= window.get_size()
		scalex = 2/scalex
		scaley = 2/scaley
		
		self.shader.bind()
		print(0.7/pow(scalex*scalex + scaley*scaley, 0.5))
		self.shader.uniformf(b'radius', 0.7)
		self.shader.uniformf(b'circleColor',  *self.color)
		
		self.shader.uniform_matrixf(b'scaleMatrix', [0, 0, 0, 1,\
		                                             0, 0, 1, 0,\
		                                             0, 1, 0, 0,\
		                                             1, 0, 0, 0])				

		self.shader.uniform_matrixf(b'pMatrix', [0, 0, 0, 1,\
		                                        0, 0, 1, 0,\
		                                        0, 1, 0, 0,\
		                                        1, 0, 0, 0])		
		
		self.shader.uniform_matrixf(b'mvMatrix', [0, 0, 0, 1,\
		                                           0, 0, 1, 0,\
		                                           0, 1, 0, 0,\
		                                           1, 0, -1, -1])


		glEnable(GL_TEXTURE_2D)
		tex=pyglet.image.Texture.create(2, 2)
		tex.blit(0, 0)
		#draw(4, GL_QUADS, ('v2f', (-0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5)))
		self.shader.unbind()
		
window = pyglet.window.Window(resizable=True)

circle=Circle((100, 100), 50)

@window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT)
	circle.render(window)
pyglet.app.run()