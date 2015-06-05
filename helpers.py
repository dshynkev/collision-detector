'''
AUTHOR:         principio
LAST EDITED:	2015-06-04 22:26:08
DESCRIPTION:    Helper functions
KNOWN ISSUES:   *> Probably too small for a separate module
'''

import constants as const

from random import uniform, seed
from glhelper import Shader

# Get a random RGBA vector. Alpha is constant and defined in constants.py, as well as generation bounds.
def getRandomColor():
    seed()
    return tuple([round(uniform (const.COLOR_LOWEST, const.COLOR_HIGHEST)) for i in range(3)])+ (const.COLOR_ALPHA,)

def getRandomTranslation():
    dx = uniform(-const.AUTO_TRANS_MAX, const.AUTO_TRANS_MAX)
    dy = uniform(-const.AUTO_TRANS_MAX, const.AUTO_TRANS_MAX)
    return (dx, dy)

# Set up vertex and geometry shaders from source files.
def load_GLshaders(vertex_src=const.VERTEX_SHADER_SRC, fragment_src=const.FRAGMENT_SHADER_SRC):
    vertex_f=open(vertex_src, 'rb')
    vertex_code=vertex_f.read()
    vertex_f.close()
    
    fragment_f=open(fragment_src, 'rb')
    fragment_code=fragment_f.read()
    fragment_f.close()
   
    return Shader([vertex_code], [fragment_code])
