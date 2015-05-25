'''
AUTHOR: 	 	principio
LAST EDITED: 	
DESCRIPTION: 	Helper functions
KNOWN ISSUES: 	
'''

import constants as const

from random import uniform, seed

def getRandomColor():
	seed()
	return tuple([round(uniform (const.COLOR_LOWEST, const.COLOR_HIGHEST)) for i in range(3)])+ (const.COLOR_ALPHA,)