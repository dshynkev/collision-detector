'''
AUTHOR: 	 	principio
LAST EDITED: 	
DESCRIPTION: 	Circle item class.
KNOWN ISSUES: 	Not implemented.
'''

import constants as const

from helpers import getRandomColor

from pyglet.graphics import draw
from pyglet.gl import *
from glhelper import *

class Circle:
	def __init__(self, center, radius):
		self.x = center[0]
		self.y = center[1]
		self.radius = radius
		
		#self.vertex = self._make_vertex_list()
		
		self.color = getRandomColor()
		
		vertex=b'''#version 400
		uniform mat4 pMatrix;
		uniform mat4 mvMatrix;
		layout(location=0) in vec2 vertex;
		out vec2 fPos;
		void main()
		{
		  gl_Position = pMatrix * mvMatrix *vec4(vertex, 0, 1);
		  fPos = gl_Position;
		 // gl_TexCoord[0] = gl_MultiTexCoord
		}'''
		fragment=b'''#version 330
		//	uniform sampler2D tex0;		
		
			in vec2 fPos;
			out vec4 fColor;
			
			void main() 
			{
			    if(fPos.x*fPos.x + fPos.y*fPos.y <= 2500)
					fColor=vec4(255, 0, 0, 1);
				else
					fColor=vec4(0, 255, 0, 1);
			}
		'''
		self.shader=Shader([vertex], [fragment])
		
	def render(self, window):		
		self.shader.bind()
		self.shader.uniformf(b'radius', self.radius)

		scalex, scaley= window.get_size()
		scalex = 2/scalex
		scaley = 2/scaley
		
		self.shader.uniform_matrixf(b'pMatrix', [0, 0, 0, 1,\
									0, 0, 1, 0,\
									0, 1, 0, 0,\
									1, 0, 0, 0])		
		
		self.shader.uniform_matrixf(b'mvMatrix', [0, 0, 0, 1,\
									0, 0, 1, 0,\
									0, 1, 0, 0,\
									1, 0, -1, -1])
		'''
		self.shader.uniform_matrixf(b'mvMatrix', [0, 0, 0, 0.1,\
									0, 0, 0.1, 0,\
									0, 1, 0, 0,\
									1, 0, 0, 0])'''
		glEnable(GL_TEXTURE_2D)
		draw(4, GL_QUADS, ('v2f', (-50, -50, 50, -50, 50, 50, -50, 50)))
		self.shader.unbind()
		
window = pyglet.window.Window(resizable=True)

circle=Circle((100, 100), 50)

@window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT)
	circle.render(window)
	
pyglet.app.run()