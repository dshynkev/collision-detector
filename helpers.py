'''
AUTHOR:         principio
LAST EDITED:	2015-05-27 23:38:07
DESCRIPTION:    Helper functions
KNOWN ISSUES:
'''

import constants as const

from random import uniform, seed
from glhelper import Shader

def getRandomColor():
    seed()
    assert(const.COLOR_LOWEST>=0 and const.COLOR_HIGHEST<=255)
    return tuple([round(uniform (const.COLOR_LOWEST, const.COLOR_HIGHEST)) for i in range(3)])+ (const.COLOR_ALPHA,)

#As opposed to getRandomColor(), this returns an OpenGL-ready color tuple normalized to [0...1]
def normalize(vector, factor=255):
    return [i/factor for i in vector]

#This is 
def load_GLshaders(vertex_src=const.VERTEX_SHADER_SRC, fragment_src=const.FRAGMENT_SHADER_SRC):
    vertex_f=open(vertex_src, 'rb')
    vertex_code=vertex_f.read()
    vertex_f.close()
    
    fragment_f=open(fragment_src, 'rb')
    fragment_code=fragment_f.read()
    fragment_f.close()
   
    return Shader([vertex_code], [fragment_code])
        