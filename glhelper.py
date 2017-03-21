# Original copyright Tristam Macdonald 2008.
# Modified by Dmytro Shynkevych 2015.
#
# Distributed under the Boost Software License, Version 1.0
# (see http://www.boost.org/LICENSE_1_0.txt)

import pyglet.gl as gl
from ctypes import *

class Shader:
    # We can theoretically have more that one source string per shader.
    # They will be concatenated later.
    def __init__(self, vert = [], frag = []):
        self.handle = gl.glCreateProgram()

        self.linked = False

        self.createShader(vert, gl.GL_VERTEX_SHADER)
        self.createShader(frag, gl.GL_FRAGMENT_SHADER)

        self.link()

    def createShader(self, strings, type):
        count = len(strings)

        #If no code
        if count < 1:
            return

        shader = gl.glCreateShader(type)

        # ctypes magic: convert python [strings] to C (char**).
        src = (c_char_p * count)(*strings)
        gl.glShaderSource(shader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)

        gl.glCompileShader(shader)

        # Retrieve the compile status
        status = c_int(0)
        gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, byref(status))

        # If compilation failed, get log and abort.
        if not status:
            gl.glGetShaderiv(shader, gl.GL_INFO_LOG_LENGTH, byref(status))
            log = create_string_buffer(status.value)
            gl.glGetShaderInfoLog(shader, status, None, log)

            raise Exception("Compiling shaders failed: {0}".format(log.value))
        else:
            # If all is well, attach the shader to the program
            gl.glAttachShader(self.handle, shader);

    def link(self):
        gl.glLinkProgram(self.handle)

        # Retrieve the link status
        status = c_int(0)
        gl.glGetProgramiv(self.handle, gl.GL_LINK_STATUS, byref(status))

        # If linking failed, get log and abort.
        if not status:
            #Retrieve the log and pass it up with an exception.
            gl.glGetProgramiv(self.handle, gl.GL_INFO_LOG_LENGTH, byref(status))
            log = create_string_buffer(status.value)
            gl.glGetProgramInfoLog(self.handle, status, None, log)

            raise Exception("Linking shaders failed {0}".format(log.value))
        else:
            self.linked = True

    def bind(self):
        gl.glUseProgram(self.handle)

    # Since we don't really care which program is bound when we unbind it,
    # this doesn't require an instance to be called on.
    @classmethod
    def unbind(self):
        gl.glUseProgram(0)

    # Upload an integer or a vector of integers as a uniform
    def uniformi(self, name, *vals):
        if len(vals) in range(1, 5):
            # Select the correct function
            { 1 : gl.glUniform1i,
                2 : gl.glUniform2i,
                3 : gl.glUniform3i,
                4 : gl.glUniform4i
                # Retrieve the uniform location, and set
            }[len(vals)](gl.glGetUniformLocation(self.handle, name), *vals)


    # Upload a float or a vector of floats as a uniform
    def uniformf(self, name, *vals):
        if len(vals) in range(1, 5):
            # Select the correct function
            { 1 : gl.glUniform1f,
                2 : gl.glUniform2f,
                3 : gl.glUniform3f,
                4 : gl.glUniform4f
                # Retrieve the uniform location, and set
            }[len(vals)](gl.glGetUniformLocation(self.handle, name), *vals)

    # Upload a uniform matrix
    def uniform_matrixf(self, name, mat):
        # Obtian the uniform location
        loc = gl.glGetUniformLocation(self.handle, name)
        # Uplaod the 4x4 floating point matrix
        gl.glUniformMatrix4fv(loc, 1, False, (c_float * 16)(*mat))
