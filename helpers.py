'''
AUTHOR:         principio
LAST EDITED:
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
def getRandomNormalizedColor():
    color = getRandomColor()
    return (color[0]/255, color[1]/255, color[2]/255, color[3]/255)

#This is 
def load_GLshaders(vertex_src=const.VERTEX_SHADER_SRC, fragment_src=const.FRAGMENT_SHADER_SRC):
    vertex_f=open(vertex_src, 'rb')
    vertex_code=vertex_f.read()
    vertex_f.close()
    
    fragment_f=open(fragment_src, 'rb')
    fragment_code=fragment_f.read()
    fragment_f.close()
   
    return Shader([vertex_code], [fragment_code])
        