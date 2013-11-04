# common render settings GUI

import maya.cmds as cmds
import maya.mel as mel

from functools import partial

# get render globals
curr_rl = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
curr_width = cmds.getAttr('defaultResolution.width')
curr_height = cmds.getAttr('defaultResolution.height')

def UI():
    """generates simple button UI"""
    # check to see if window exists
    if (cmds.window('render', exists=True)):
        cmds.deleteUI('render')

    # create window
    window = cmds.window('render', title='Render', w=120, h=300, mxb=False, mnb=False, sizeable=False)
    
    # create layout
    main_layout = cmds.columnLayout(w=120, h=300)
    
    cmds.separator(h=15)
    cmds.columnLayout()
    
    cmds.button(label='Render', w=120, h=30, command=partial(render, curr_rl, curr_width, curr_height))
    cmds.button(label='Render Square', w=120, h=30, command=partial(render, curr_rl, 1024, 1024))
    cmds.button(label='Render AO', w=120, h=30, command=partial(render, 'ao', 1024, 1024))
    cmds.setParent('..')
    cmds.separator(h=15)
    
    cmds.showWindow(window)
    
def render(rl, width, height, *args):
    """
    renders the scene with the given attributes

    keyword args:
    width -- width of render image in pixels
    height -- height of render image in pixels
    *args -- additional args

    """
    dar = width / float(height)
    cmds.setAttr('defaultResolution.deviceAspectRatio', dar)
    mel.eval('RenderViewWindow')
    cmds.Mayatomr(preview=True, layer=rl, xResolution=width, yResolution=height, camera='perspShape')
    editor = 'renderView'
    cmds.renderWindowEditor(editor, e=True, si=True)

def main():
    """calls the UI function to generate the UI"""
    UI()
