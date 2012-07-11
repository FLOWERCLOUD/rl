# generates commands to batch render via the command line

import maya.cmds as cmds
import maya.mel as mel

def UI():
	# check to see if window exists
	if (cmds.window("batch", exists=True)):
		cmds.deleteUI("batch")

	# create window
	window = cmds.window("batch", title="Batch Render Commands", w=640, h=360, mxb=True, mnb=True, sizeable=True)
	
	# create layout
	mainLayout = cmds.columnLayout(w=640, h=360)
	
	# select render directory
	cmds.separator(h=15)
	cmds.text(label="Render Directory")
	cmds.textField("renderDirField", w=640, tx='')
	cmds.button(label="Select Render Directory", command=selRenderDir)
	
	# define folder name
	cmds.separator(h=15)
	cmds.text(label="Name")
	cmds.textField("name", w=640, tx='')
	
	# select camera
	cmds.separator(h=15)
	cmds.text(label="Renderer")
	cmds.optionMenu("renderer")
	cmds.menuItem(label='mr', parent='renderer')
	
	# select render layer
	cmds.separator(h=15)
	cmds.text(label="Render Layer")
	cmds.optionMenu("rl")
	populateOption('renderLayer', 'rl')
	
	# select camera
	cmds.separator(h=15)
	cmds.text(label="Camera")
	cmds.optionMenu("cam")
	populateOption('camera', 'cam')
	
	# start and end frame, by, padding
	cmds.separator(h=15)
	cmds.text(label="Start Frame")
	cmds.intField("startFrame", v=cmds.getAttr('defaultRenderGlobals.startFrame'))
	cmds.text(label="End Frame")
	cmds.intField("endFrame", v=cmds.getAttr('defaultRenderGlobals.endFrame'))
	cmds.text(label="By Frame Step")
	cmds.intField("by", v=cmds.getAttr('defaultRenderGlobals.byFrameStep'))
	cmds.text(label="Padding")
	cmds.intField("padding", v=cmds.getAttr('defaultRenderGlobals.extensionPadding'))
	
	# file format
	cmds.separator(h=15)
	cmds.optionMenu("ff")
	cmds.menuItem(label='exr', parent='ff')
	cmds.menuItem(label='tif', parent='ff')
	cmds.menuItem(label='iff', parent='ff')
	cmds.menuItem(label='tga', parent='ff')
	cmds.menuItem(label='psd', parent='ff')
	
	# scroll field to display commands
	cmds.separator(h=15)
	cmds.scrollField("commands", editable=True, wordWrap=True, tx='', w=640)
	
	# create buttons
	cmds.separator(h=15)
	cmds.button(label="Add Command", w=300, h=30, command=addCommand)
	cmds.button(label="Clear", w=300, h=30, command=clear)
	cmds.separator(h=15)
	
	cmds.showWindow(window)
	
def selRenderDir(*args):
	# open a file browser to select a directory
	renderDir = cmds.fileDialog2(ds=2, dir='~/', fm=3)
	cmds.textField("renderDirField", edit=True, tx=renderDir[0] + '/')
	
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
	comm = 'Render -v 0 -rd {0} -im {1} -r {2} -s {3} -e {4} -b {5} -pad {6} -of {7} -cam {8} -rl {9} {10};'.format(rd, name, rend, s, e, b, p, ff, cam, rl, file)
	cmds.scrollField("commands", edit=True, tx=comm)
	
def clear(*args):
	cmds.scrollField("commands", edit=True, tx='')
	
def populateOption(t, p):
	renderLayers = cmds.ls(type=t)
	for rl in renderLayers:
		cmds.menuItem(label=rl, parent=p)
	
