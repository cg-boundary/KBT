# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Context, Region, Area
from mathutils import Vector

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def screen_factor():
    return bpy.context.preferences.system.ui_scale


def point_within_region(point:Vector, region:Region):
    if isinstance(point, Vector) and isinstance(region, Region):
        if point.x >= region.x:
            if point.x <= region.x + region.width:
                if point.y >= region.y:
                    if point.y <= region.y + region.height:
                        return True
    return False


def tag_area_for_redraw(context:Context):
    if isinstance(context, Context):
        if hasattr(context, 'area'):
            if isinstance(context.area, Area):
                context.area.tag_redraw()


def tag_all_areas_of_type_for_redraw(area_type='TEXT_EDITOR'):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == area_type:
                area.tag_redraw()


def create_new_window():
    original_windows = bpy.context.window_manager.windows[:]
    bpy.ops.wm.window_new()
    window = None
    for window in bpy.context.window_manager.windows:
        if window not in original_windows:
            return window
    return None
