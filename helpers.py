'''
AUTHOR:         principio
LAST EDITED:	2015-05-28 00:34:18
DESCRIPTION:    Helper functions
KNOWN ISSUES:
'''

import constants as const

from random import uniform, seed
from glhelper import Shader

# Get a random RGBA vector. Alpha is constant and defined in constants.py, as well as generation bounds.
def getRandomColor():
    seed()
    assert(const.COLOR_LOWEST>=0 and const.COLOR_HIGHEST<=255)
    return tuple([round(uniform (const.COLOR_LOWEST, const.COLOR_HIGHEST)) for i in range(3)])+ (const.COLOR_ALPHA,)

# Normalize a vector with respect to a given factor. 
# By default, will normalize a [0..255] to [0.0...1.0] GL RGBA vector
def normalize(vector, factor=255):
    return [i/factor for i in vector]

# Set up vertex and geometry shaders from source files.
def load_GLshaders(vertex_src=const.VERTEX_SHADER_SRC, fragment_src=const.FRAGMENT_SHADER_SRC):
    vertex_f=open(vertex_src, 'rb')
    vertex_code=vertex_f.read()
    vertex_f.close()
    
    fragment_f=open(fragment_src, 'rb')
    fragment_code=fragment_f.read()
    fragment_f.close()
   
    return Shader([vertex_code], [fragment_code])
        