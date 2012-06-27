# automatically creates an ambient occlusion render layer

import maya.cmds as cmds

# create a new render layer that includes all objects and all new objects
cmds.createRenderLayer(name='ao', g=True, makeCurrent=True)
# create a new surface shader for the ambient occlusion shader
surfShader = cmds.shadingNode('surfaceShader', asShader=True, name='amb_occl_surf_shader')
aoShader = cmds.shadingNode('mib_amb_occlusion', asShader=True, name='amb_occl')
cmds.connectAttr(aoShader+'.outValue', surfShader+'.outColor')
# increase the default samples from 16->128
cmds.setAttr(aoShader+'.samples', 128)

# create a new shading group for the ao shader
sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='aoSG')
cmds.connectAttr(surfShader+'.outColor', sg+'.surfaceShader')

# select all objects in the layer and attach the shader
cmds.select(all=True)
cmds.hyperShade(a=surfShader)

# switch to mental ray rendering
cmds.setAttr('defaultRenderGlobals.ren', 'mentalRay', type='string')
