# automatically creates an ambient occlusion render layer

import maya.cmds as cmds
import maya.mel as mel

def UI():
	# check to see if window exists
	if (cmds.window("ao", exists=True)):
		cmds.deleteUI("ao")

	# create window
	window = cmds.window("ao", title="Ambient Occlusion", w=300, h=300, mxb=False, mnb=False, sizeable=False)
	
	# create layout
	mainLayout = cmds.columnLayout(w=300, h=300)
	
	# if AO exists, get attributes from shader, otherwise provide defaults
	numSamples = 128
	spread = 0.8
	maxDistance = 0
	if (aoExists()):
		numSamples = cmds.getAttr('amb_occl.samples')
		spread = cmds.getAttr('amb_occl.spread')
		maxDistance = cmds.getAttr('amb_occl.max_distance')
		
	# create input fields
	cmds.separator(h=15)
	cmds.text(label="Number of samples")
	samplesField = cmds.intField("numSamples", v=numSamples, min=0, max=512)
	cmds.text(label="Spread")
	spreadField = cmds.floatField("spread", v=spread)
	cmds.text(label="Max Distance")
	maxDistanceField = cmds.intField("maxDistance", v=maxDistance)
	
	# create buttons
	cmds.separator(h=15)
	cmds.button(label="Add Ambient Occlusion", w=300, h=30, command=addAmbOcc)
	cmds.button(label="Update Objects/Settings", w=300, h=30, command=addAmbOcc)
	cmds.separator(h=15)
	
	cmds.showWindow(window)
	
# creates a new ambient occlusion render layer
def createRL(numSamples, spread, maxDistance):
	# create a new render layer that includes all objects and all new objects
	cmds.createRenderLayer(name='ao', g=True, makeCurrent=True)
	# create a new surface shader for the ambient occlusion shader
	surfShader = cmds.shadingNode('surfaceShader', asShader=True, name='amb_occl_surf_shader')
	aoShader = cmds.shadingNode('mib_amb_occlusion', asShader=True, name='amb_occl')
	cmds.connectAttr(aoShader+'.outValue', surfShader+'.outColor')

	# create a new shading group for the ao shader
	sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='aoSG')
	cmds.connectAttr(surfShader+'.outColor', sg+'.surfaceShader')
	
	# add objects to render layer and adjust settings
	reAdd(numSamples, spread, maxDistance)

	
# changes settings of mib_amb_occlusion
def changeAOSettings(numSamples=128, spread=0.8, maxDistance=0):
	cmds.setAttr('amb_occl.samples', numSamples)
	cmds.setAttr('amb_occl.spread', spread)
	cmds.setAttr('amb_occl.max_distance', maxDistance)

# changes default render settings to get a decent render
def changeRS():
	# switch to mental ray rendering
	cmds.setAttr('defaultRenderGlobals.ren', 'mentalRay', type='string')
	# create the mental ray rendering nodes so they can be changed
	mel.eval('miCreateDefaultNodes')
	# set filter to gaussian as layer overide
	cmds.editRenderLayerAdjustment( 'miDefaultOptions.filter', layer='ao' )
	cmds.setAttr('miDefaultOptions.filter', 2);
	# set the max/min samples
	cmds.setAttr('miDefaultOptions.maxSamples', 2)
	cmds.setAttr('miDefaultOptions.minSamples', 0)
	
def addAmbOcc(*args):
	# get the values entered from the UI
	samplesField = cmds.intField("numSamples", q=True, v=True)
	spreadField = cmds.floatField("spread", q=True, v=True)
	maxDistanceField = cmds.intField("maxDistance", q=True, v=True)
	
	# if AO already exists, just re add all objects
	if(aoExists()):
		reAdd(samplesField, spreadField, maxDistanceField)
	else:
		createRL(samplesField, spreadField, maxDistanceField)
		changeRS()

# adds all objects to the ao layer	
def reAdd(samplesField, spreadField, maxDistanceField):
	# switch to the ao render layer
	cmds.editRenderLayerGlobals(currentRenderLayer='ao')
	cmds.select(ado=True)
	cmds.hyperShade(a='amb_occl_surf_shader')
	
	changeAOSettings(samplesField, spreadField, maxDistanceField)
	
# returns True if ao has been generated 
def aoExists():
	allShaders = cmds.ls(mat=1)
	for shader in allShaders:
		if (shader == 'amb_occl_surf_shader'):
			return True
	return False
	
	