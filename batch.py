# generates commands to batch render via the command line

import maya.cmds as cmds
import maya.mel as mel

def UI():
	# check to see if window exists
	if (cmds.window('batch', exists=True)):
		cmds.deleteUI('batch')

	# create window
	window = cmds.window('batch', title='Batch Render Commands', w=640, h=480, mxb=True, mnb=True, sizeable=True)
	
	# create layout
	mainLayout = cmds.columnLayout(w=640, h=480)
	
	# get the current render layer
	currLayer = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
	
	# select render directory
	cmds.separator(h=15)
	cmds.rowLayout(numberOfColumns=3, columnWidth3=(160, 320, 160))
	cmds.text(label='Render Directory', w=145, al='right')
	imageDirectory = cmds.workspace(q=True, rd=True)
	imageDirectory += 'images/'
	cmds.textField('renderDirField', w=320, tx=imageDirectory)
	cmds.button(label='Select Render Directory', w=160, command=selRenderDir)
	cmds.setParent('..')
	
	# define folder name
	cmds.rowLayout(numberOfColumns=2, columnWidth2=(160, 320))
	cmds.text(label='Name', w=145, al='right')
	cmds.textField('name', w=320, tx=currLayer)
	cmds.setParent('..')
	
	# select renderer
	cmds.rowLayout(numberOfColumns=2, columnWidth2=(160, 320))
	cmds.text(label='Renderer', w=145, al='right')
	cmds.optionMenu('renderer')
	cmds.menuItem(label='mr', parent='renderer')
	cmds.setParent('..')
	
	# select render layer
	cmds.rowLayout(numberOfColumns=2, columnWidth2=(160, 320))
	cmds.text(label='Render Layer', w=145, al='right')
	cmds.optionMenu('rl', changeCommand=updateName)
	populateOption('renderLayer', 'rl')
	selectCurrent('rl', 'renderLayer', currLayer)
	cmds.setParent('..')
	
	# select camera
	cmds.rowLayout(numberOfColumns=2, columnWidth2=(160, 320))
	cmds.text(label='Camera', w=145, al='right')
	cmds.optionMenu('cam')
	populateOption('camera', 'cam')
	cmds.setParent('..')
	
	currPanel = cmds.getPanel( withFocus=True )
	panelType = cmds.getPanel(typeOf=currPanel)
	# default to persp, otherwise try to find the cam of the current panel
	currCam = 'persp'
	if(panelType == 'modelPanel'):
		currCam = cmds.modelEditor( currPanel, q=True, camera=True )
	
	currCam = cmds.listRelatives(currCam, s=True)[0]	
	selectCurrent('cam', 'camera', currCam)
	
	# file format
	cmds.rowLayout(numberOfColumns=2, columnWidth2=(160, 320))
	cmds.text(label='File Format', w=145, al='right')
	cmds.optionMenu('ff')
	cmds.menuItem(label='exr', parent='ff')
	cmds.menuItem(label='tif', parent='ff')
	cmds.menuItem(label='iff', parent='ff')
	cmds.menuItem(label='tga', parent='ff')
	cmds.menuItem(label='psd', parent='ff')
	cmds.setParent('..')
	
	# start and end frame, by, padding	
	cmds.separator(h=15)
	cmds.rowLayout(numberOfColumns=4, columnWidth4=(160, 160, 160, 160))
	cmds.text(label='Start Frame', w=145, al='center')
	cmds.text(label='End Frame', w=145, al='center')
	cmds.text(label='By Frame Step', w=145, al='center')
	cmds.text(label='Padding', w=145, al='center')
	cmds.setParent('..') # this "ends" or "closes" the current layout (rowLayout)
	cmds.rowLayout(numberOfColumns=4, columnWidth4=(160, 160, 160, 160))
	cmds.intField('startFrame', w=145, v=cmds.getAttr('defaultRenderGlobals.startFrame'))
	cmds.intField('endFrame', w=145, v=cmds.getAttr('defaultRenderGlobals.endFrame'))
	cmds.intField('by', w=145, v=cmds.getAttr('defaultRenderGlobals.byFrameStep'))
	# set default padding to 4
	cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
	cmds.intField('padding', w=145, v=cmds.getAttr('defaultRenderGlobals.extensionPadding'))
	cmds.setParent('..') # this "ends" or "closes" the current layout (rowLayout)
	
	# scroll field to display commands
	cmds.separator(h=15)
	cmds.scrollField('commands', editable=True, wordWrap=True, tx='', w=640)
	
	# create buttons
	cmds.separator(h=15)
	cmds.rowLayout(numberOfColumns=3, columnWidth3=(213, 214, 213))
	cmds.button(label='Append Command', w=213, h=30, command=addCommand)
	cmds.button(label='Clear All', w=214, h=30, command=clear)
	cmds.button(label='Save Script', w=213, h=30, command=saveScript)
	cmds.setParent('..')
	cmds.separator(h=15)
	
	cmds.showWindow(window)
	
def selRenderDir(*args):
	# open a file browser to select a directory
	imageDirectory = cmds.workspace(q=True, rd=True)
	imageDirectory += 'images/'
	renderDir = cmds.fileDialog2(ds=2, dir=imageDirectory, fm=3)
	cmds.textField('renderDirField', edit=True, tx=renderDir[0] + '/')
	
def addCommand(*args):
	# get values from input fields
	rd = cmds.textField('renderDirField', q=True, tx=True)
	name = cmds.textField('name', q=True, tx=True)
	rend = cmds.optionMenu('renderer', q=True, v=True)
	s = cmds.intField('startFrame', q=True, v=True)
	e = cmds.intField('endFrame', q=True, v=True)
	b = cmds.intField('by', q=True, v=True)
	p = cmds.intField('padding', q=True, v=True)
	ff = cmds.optionMenu('ff', q=True, v=True)
	rl = cmds.optionMenu('rl', q=True, v=True)
	cam = cmds.optionMenu('cam', q=True, v=True)
	file = cmds.file(q=True, sn=True)
	
	# big string format
	comm = 'Render -v 0 -rd {0} -im {1} -r {2} -s {3} -e {4} -b {5} -pad {6} -of {7} -cam {8} -rl {9} {10};\n'.format(rd, name, rend, s, e, b, p, ff, cam, rl, file)
	
	# get the current commands and add on the new one
	currCommands = cmds.scrollField('commands', q=True, tx=True)
	currCommands += comm
	
	cmds.scrollField('commands', edit=True, tx=currCommands)

# resets the scrollField
def clear(*args):
	cmds.scrollField('commands', edit=True, tx='')

# saves commands as a shell script in your data directory as render.sh
def saveScript(*args):
	dataDirectory = cmds.workspace(q=True, rd=True)
	dataFile = dataDirectory + 'data/render.sh'
	f = open(dataFile, 'w')
	f.write(cmds.scrollField('commands', q=True, tx=True))
	f.close()
	
# updates the name based on currently selected render layer
def updateName(*args):
	rl = cmds.optionMenu('rl', q=True, v=True)
	name = cmds.textField('name', e=True, tx=rl)

# populates optionMenu items given a type of object (t) and a parent menu (p)
def populateOption(t, p):
	options = cmds.ls(type=t)
	for o in options:
		cmds.menuItem(label=o, parent=p)

# selects the appropriate item in a optionMenu
def selectCurrent(optionMenuName, t, current):
	options = cmds.ls(type=t)
	for x in range(len(options)):
		if(options[x] == current):
			cmds.optionMenu(optionMenuName, edit=True, sl=x+1)
