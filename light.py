import maya.cmds as cmds
import maya.mel as mel
from functools import partial

lights = cmds.ls(type='light')
WIDTH = 800
HEIGHT = 600

def UI():
	# check to see if window exists
	if (cmds.window('lights', exists=True)):
		cmds.deleteUI('lights')

	# create window
	window = cmds.window('lights', title='Lights', w=WIDTH, h=HEIGHT, mxb=False, mnb=False, sizeable=False)
	
	createLayout()
	
	cmds.showWindow(window)
	
def createLayout():
	numLights = len(lights)
	cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 200), (2, 100), (3, 100)], cs=[3, 5], rs=[5, 5] )
	for light in lights:
		cmds.text(label=light, w=200, al='left')
		cmds.floatField(light + 'intensity', v=cmds.getAttr(light + '.intensity'), cc=partial(updateIntensity, light), ec=partial(updateIntensity, light))
		#cmds.floatField(light + 'intensity2', v=cmds.getAttr(light + '.intensity'))	
		cmds.button(label='Color', command=partial(colorPicker, light))
		
def updateIntensity(light, *args):
	cmds.setAttr(light + '.intensity', args[0])
	
def colorPicker(light, *args):
	currColor = cmds.getAttr(light + '.color')
	print currColor
	#setAttr "ambientLightShape1.color" -type double3 1 0.09375 0 ;
	cmds.colorEditor(rgbValue=currColor[0])
	if cmds.colorEditor(query=True, result=True):
		values = cmds.colorEditor(query=True, rgb=True)
		print 'RGB = ' + str(values)
		#values = cmds.colorEditor(query=True, hsv=True)
		#print 'HSV = ' + str(values)
		#alpha = cmds.colorEditor(query=True, alpha=True)
		#print 'Alpha = ' + str(alpha)
		cmds.setAttr(light + '.color', *values)
	else:
		print 'Editor was dismissed'