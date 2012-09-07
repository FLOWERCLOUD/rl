# common render settings GUI

import maya.cmds as cmds
import maya.mel as mel

from functools import partial

# get render globals
currRL = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
currWidth = cmds.getAttr('defaultResolution.width')
currHeight = cmds.getAttr('defaultResolution.height')

def UI():
	# check to see if window exists
	if (cmds.window('render', exists=True)):
		cmds.deleteUI('render')

	# create window
	window = cmds.window('render', title='Render', w=120, h=300, mxb=False, mnb=False, sizeable=False)
	
	# create layout
	mainLayout = cmds.columnLayout(w=120, h=300)
	
	cmds.separator(h=15)
	cmds.columnLayout()
	
	cmds.button(label='Render', w=120, h=30, command=partial(render, currRL, currWidth, currHeight))
	cmds.button(label='Render Square', w=120, h=30, command=partial(render, currRL, 1024, 1024))
	cmds.button(label='Render AO', w=120, h=30, command=partial(render, 'ao', 1024, 1024))
	cmds.setParent('..')
	cmds.separator(h=15)
	
	# create layout
	mainLayout = cmds.columnLayout(w=120, h=300)
	
	cmds.showWindow(window)
	
def render(rl, width, height, *args):
	dar = width / float(height)
	cmds.setAttr('defaultResolution.deviceAspectRatio', dar)
	mel.eval('RenderViewWindow')
	cmds.Mayatomr( preview=True, layer=rl, xResolution=width, yResolution=height, camera='perspShape' )
	editor = 'renderView'
	cmds.renderWindowEditor(editor, e=True, si=True)
