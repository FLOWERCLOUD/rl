# generates commands to batch render via the command line

import maya.cmds as cmds
import maya.mel as mel

def UI():
	# check to see if window exists
	if (cmds.window("batch", exists=True)):
		cmds.deleteUI("batch")

	# create window
	window = cmds.window("batch", title="Ambient Occlusion", w=640, h=360, mxb=True, mnb=True, sizeable=True)
	
	# create layout
	mainLayout = cmds.columnLayout(w=640, h=360)
	
	# select render directory
	cmds.separator(h=15)
	cmds.text(label="Render Directory")
	cmds.textField("renderDirField", w=640, tx='')
	cmds.button(label="Select Render Directory", command=selRenderDir)
	
	# start and end frame
	cmds.separator(h=15)
	cmds.text(label="Start Frame")
	samplesField = cmds.intField("startFrame", v=0, min=0, max=512)
	cmds.text(label="End Frame")
	samplesField = cmds.intField("endFrame", v=0, min=0, max=512)
	
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
	cmds.textField("renderDirField", edit=True, tx=renderDir[0])
	
def addCommand(*args):
	# get values from input fields
	rd = cmds.textField('renderDirField', q=True, tx=True)
	# big string format
	comm = 'Render -v 0 -rd {0} -im {1} -r {2} -s {3} -e {4} -b {5} -pad {6} -cam {7} -rl {8} {9};'.format(rd, 'beauty', 'mr', '0', '24', '1', '4', 'perspShape', 'defaultRenderLayer', '~/Documents/maya/projects/test.ma')
	cmds.scrollField("commands", edit=True, tx=comm)
	
def clear(*args):
	cmds.scrollField("commands", edit=True, tx='')
	
