import maya.cmds as cmds
import maya.mel as mel
from functools import partial

lights = []
swatches = []
rows = []
WIDTH = 800
HEIGHT = 600
main_layout = ''

def UI(*args):
	# check to see if window exists
	if (cmds.window('lights', exists=True)):
		cmds.deleteUI('lights')

	# create window
	window = cmds.window('lights', title='Lights', w=WIDTH, h=HEIGHT, mxb=False, mnb=False, sizeable=True)
	
	createLayout()
	
	cmds.showWindow(window)
	
def createLayout():
	numLights = len(lights)
	global main_layout
	main_layout = cmds.scrollLayout(verticalScrollBarThickness=16, horizontalScrollBarThickness=0)
	# create buttons
	cmds.rowLayout( numberOfColumns=5, h=40)
	cmds.button(label='Spotlight', command=partial(addLight, 'spot'))
	cmds.button(label='Directional', command=partial(addLight, 'dir'))
	cmds.button(label='Point', command=partial(addLight, 'point'))
	cmds.button(label='Ambient', command=partial(addLight, 'amb'))
	cmds.button(label='Refresh', al='right', command=refresh)
	cmds.setParent('..')
	# create column labels
	cmds.rowLayout( numberOfColumns=4, columnWidth4=[100, 150, 100, 100], h=40)
	cmds.text(label='Enabled', w=80, al='left')
	cmds.text(label='Name', w=130, al='left')
	cmds.text(label='Intensity')
	cmds.text(label='Color')
	cmds.setParent('..')
	createLights()

def createLights():
	global rows
	rows = []
	
	global lights
	lights = cmds.ls(type='light')
	
	global swatches
	swatches = []
	
	global main_layout
	cmds.setParent(main_layout)
	# create rows of individual lights
	for i, light in enumerate(lights):
		light_row = cmds.rowLayout( numberOfColumns=4, columnWidth4=[100, 150, 100, 50], h=40)
		rows.append(light_row)
		# check if light is enabled
		enabled = cmds.getAttr(light + '.visibility')
		cmds.checkBox(label='', v=enabled, onc=partial(turnOn, light), ofc=partial(turnOff, light), al='center')
		cmds.text(label=light, w=130, al='left')
		cmds.floatField(light + 'intensity', v=cmds.getAttr(light + '.intensity'), cc=partial(updateIntensity, light), ec=partial(updateIntensity, light), w=80)
		swatch = cmds.button(label='', bgc=cmds.getAttr(light + '.color')[0], ebg=True, w=30, h=30, command=partial(colorPicker, light, i))
		swatches.append(swatch)
		cmds.setParent('..')
		
def refresh(*args):
	global rows
	global lights
	for row in rows:
		cmds.deleteUI(row)
	rows = []
	lights = cmds.ls(type='light')
	createLights()

def updateIntensity(light, *args):
	cmds.setAttr(light + '.intensity', args[0])
	
def turnOff(light, *args):
	cmds.setAttr(light + '.visibility', False)
	
def turnOn(light, *args):
	cmds.setAttr(light + '.visibility', True)
	
def colorPicker(light, index, *args):
	currColor = cmds.getAttr(light + '.color')
	cmds.colorEditor(rgbValue=currColor[0])
	if cmds.colorEditor(query=True, result=True):
		values = cmds.colorEditor(query=True, rgb=True)
		cmds.setAttr(light + '.color', *values)
		cmds.button(swatches[index], e=True, bgc=cmds.getAttr(light + '.color')[0])
		
def addLight(kind, *args):
	if kind == 'spot':
		cmds.spotLight()
	elif kind == 'dir':
		cmds.directionalLight()
	elif kind == 'point':
		cmds.pointLight()
	elif kind == 'amb':
		cmds.ambientLight()
	refresh()
		