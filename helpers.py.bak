'''
AUTHOR: 	 	principio
LAST EDITED: 	
DESCRIPTION:            Helper functions
KNOWN ISSUES: 	
'''

import constants as const

from random import uniform, seed

def getRandomColor():
	seed()
	return tuple([round(uniform (const.COLOR_LOWEST, const.COLOR_HIGHEST)) for i in range(3)])+ (const.COLOR_ALPHA,)

def getRandomNormalizedColor():
	color = getRandomColor()
	return (color[0]/255, color[1]/255, color[2]/255, color[3]/255)