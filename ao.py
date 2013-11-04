# automatically creates an ambient occlusion render layer

import maya.cmds as cmds
import maya.mel as mel

def UI():
    """generates UI window"""
    # check to see if window exists
    if (cmds.window('ao', exists=True)):
        cmds.deleteUI('ao')

    # create window
    window = cmds.window('ao', title='Ambient Occlusion', w=300, h=300, mxb=False, mnb=False, sizeable=False)
    
    # create layout
    main_layout = cmds.columnLayout(w=300, h=300)
    
    # if AO exists, get attributes from shader, otherwise provide defaults
    num_samples = 128
    spread = 0.8
    max_distance = 0
    if (ao_exists()):
        num_samples = cmds.getAttr('amb_occl.samples')
        spread = cmds.getAttr('amb_occl.spread')
        max_distance = cmds.getAttr('amb_occl.max_distance')
        
    # create input fields
    cmds.separator(h=15)
    cmds.text(label='Number of samples')
    samples_field = cmds.intField('num_samples', v=num_samples, min=0, max=512)
    cmds.text(label='Spread')
    spread_field = cmds.floatField('spread', v=spread)
    cmds.text(label='Max Distance')
    max_distance_field = cmds.intField('max_distance', v=max_distance)
    
    # create buttons
    cmds.separator(h=15)
    cmds.button(label='Add Ambient Occlusion', w=300, h=30, command=add_amb_occ)
    cmds.button(label='Update Objects/Settings', w=300, h=30, command=add_amb_occ)
    cmds.separator(h=15)
    
    cmds.showWindow(window)
    
def create_rl(num_samples, spread, max_distance):
    """
    create a new render layer that includes all objects and all new objects

    keyword args:
    num_samples -- number of samples in the AO shader, higher samples == longer render times
    spread -- angle at which the rays are cast out from the surface, smaller angle creates a harsher transition
    max_distance -- how far the ray traces out into the scene before determining a collision

    """
    cmds.createRenderLayer(name='ao', g=True, makeCurrent=True)
    # create a new surface shader for the ambient occlusion shader
    surf_shader = cmds.shadingNode('surfaceShader', asShader=True, name='amb_occl_surf_shader')
    ao_shader = cmds.shadingNode('mib_amb_occlusion', asShader=True, name='amb_occl')
    cmds.connectAttr(ao_shader + '.outValue', surf_shader + '.outColor')

    # create a new shading group for the ao shader
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='aoSG')
    cmds.connectAttr(surf_shader + '.outColor', sg + '.surfaceShader')
    
    # add objects to render layer and adjust settings
    re_add(num_samples, spread, max_distance)

    
def change_ao_settings(num_samples=128, spread=0.8, max_distance=0):
    """changes settings of mib_amb_occlusion"""
    cmds.setAttr('amb_occl.samples', num_samples)
    cmds.setAttr('amb_occl.spread', spread)
    cmds.setAttr('amb_occl.max_distance', max_distance)

# changes default render settings to get a decent render
def change_rs():
    """changes mental ray render settings to appropriate defaults"""
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
    
def add_amb_occ(*args):
    """adds ambient occlusion to the scene, if it already exists, just update the objects"""
    # get the values entered from the UI
    samples_field = cmds.intField('num_samples', q=True, v=True)
    spread_field = cmds.floatField('spread', q=True, v=True)
    max_distance_field = cmds.intField('max_distance', q=True, v=True)
    
    # if AO already exists, just re add all objects
    if(ao_exists()):
        re_add(samples_field, spread_field, max_distance_field)
    else:
        create_rl(samples_field, spread_field, max_distance_field)
        change_rs()

def re_add(samples_field, spread_field, max_distance_field):
    """if AO already has been setup, just add all the objects to the AO layer"""
    # switch to the ao render layer
    cmds.editRenderLayerGlobals(currentRenderLayer='ao')
    objects = cmds.ls(g=True)
    cmds.select(objects)
    cmds.hyperShade(a='amb_occl_surf_shader')
    
    change_ao_settings(samples_field, spread_field, max_distance_field)
    
def ao_exists():
    """returns True if AO exists"""
    all_shaders = cmds.ls(mat=1)
    for shader in all_shaders:
        if (shader == 'amb_occl_surf_shader'):
            return True
    return False

def main():
    """calls the UI function to generate the UI"""
    UI()
