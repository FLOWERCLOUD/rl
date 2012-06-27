# automatically creates an ambient occlusion render layer

import maya.cmds as cmds

def UI():
	# check to see if window exists
	if (cmds.window("ao", exists=True)):
		cmds.deleteUI("ao")

	# create window
	window = cmds.window("ao", title="Add Ambient Occlusion Layer", w=300, h=300, mxb=False, mnb=False, sizeable=False)
	
	# create layout
	mainLayout = cmds.columnLayout(w=300, h=300)
	
	cmds.separator(h=15)
	cmds.text(label="Number of samples")
	samplesField = cmds.intField("numSamples", v=128, min=0, max=512)
	
	cmds.separator(h=15)
	cmds.button(label="Add Ambient Occlusion", w=300, h=30, command=addAmbOcc)
	cmds.separator(h=15)
	
	cmds.showWindow(window)
	
def createRL(numSamples):
	# create a new render layer that includes all objects and all new objects
	cmds.createRenderLayer(name='ao', g=True, makeCurrent=True)
	# create a new surface shader for the ambient occlusion shader
	surfShader = cmds.shadingNode('surfaceShader', asShader=True, name='amb_occl_surf_shader')
	aoShader = cmds.shadingNode('mib_amb_occlusion', asShader=True, name='amb_occl')
	cmds.connectAttr(aoShader+'.outValue', surfShader+'.outColor')
	# set the number of samples to value from UI
	cmds.setAttr(aoShader+'.samples', numSamples)

	# create a new shading group for the ao shader
	sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='aoSG')
	cmds.connectAttr(surfShader+'.outColor', sg+'.surfaceShader')

	# select all objects in the layer and attach the shader
	cmds.select(all=True)
	cmds.hyperShade(a=surfShader)

def changeRS():
	# switch to mental ray rendering
	cmds.setAttr('defaultRenderGlobals.ren', 'mentalRay', type='string')
	
def addAmbOcc(*args):
	# get the value entered into the number of samples field
	samplesField = cmds.intField("numSamples", q=True, v=True)
	createRL(samplesField)
	changeRS()
	
	
	
	