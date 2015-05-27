# Original copyright Tristam Macdonald 2008.
# Modified by Dmytro Shynkevych 2015.
#
# Distributed under the Boost Software License, Version 1.0
# (see http://www.boost.org/LICENSE_1_0.txt)
'''
AUTHOR:         principio
LAST EDITED:
DESCRIPTION:    OpenGL shader program convenience class.
KNOWN ISSUES:   * VERY liberal in terms of error-checking; better pray that nothing fails.
                * Barely tested
'''

from pyglet.gl import *
from ctypes import *

class Shader:
    # We can theoretically have more that one source string per shader.
    # They will be concatenated later.
    def __init__(self, vert = [], frag = []):
        self.handle = glCreateProgram()
        
        self.linked = False

        self.createShader(vert, GL_VERTEX_SHADER)
        self.createShader(frag, GL_FRAGMENT_SHADER)
        
        self.link()

    def createShader(self, strings, type):
        count = len(strings)
        
        #If no code 
        if count < 1:
            return

        shader = glCreateShader(type)

        # ctypes magic: convert python [strings] to C (char**).
        src = (c_char_p * count)(*strings)
        glShaderSource(shader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)

        glCompileShader(shader)

        # Retrieve the compile status
        status = c_int(0)
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))

        # If compilation failed, get log and abort.
        if not status:
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(status))
            log = create_string_buffer(status.value)
            glGetShaderInfoLog(shader, status, None, log)
            
            raise Exception(log)
        else:
            # If all is well, attach the shader to the program
            glAttachShader(self.handle, shader);

    def link(self):
        glLinkProgram(self.handle)

        # Retrieve the link status
        status = c_int(0)
        glGetProgramiv(self.handle, GL_LINK_STATUS, byref(status))

        # If linking failed, get log and abort.
        if not status:
            #Retrieve the log and pass it up with an exception.
            glGetProgramiv(self.handle, GL_INFO_LOG_LENGTH, byref(status))
            log = create_string_buffer(status.value)
            glGetProgramInfoLog(self.handle, status, None, log)
            
            raise Exception(log)
        else:
            self.linked = True

    def bind(self):
        glUseProgram(self.handle)

    # Since we don't really care which program is bound when we unbind it,
    # this doesn't require an instance to be called on.
    @classmethod
    def unbind():
        glUseProgram(0)

    # Upload a float or a vector of floats as a uniform
    def uniformf(self, name, *vals):
        if len(vals) in range(1, 5):
            # Select the correct function
            { 1 : glUniform1f,
                2 : glUniform2f,
                3 : glUniform3f,
                4 : glUniform4f
                # Retrieve the uniform location, and set
            }[len(vals)](glGetUniformLocation(self.handle, name), *vals)

    # Upload a uniform matrix
    def uniform_matrixf(self, name, mat):
        # Obtian the uniform location
        loc = glGetUniformLocation(self.handle, name)
        # Uplaod the 4x4 floating point matrix
        glUniformMatrix4fv(loc, 1, False, (c_float * 16)(*mat))
