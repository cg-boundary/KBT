# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

from bpy.types import Event
from mathutils import Vector

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def mouse_vector_from_region(event:Event):
    if isinstance(event, Event):
        return Vector((event.mouse_region_x, event.mouse_region_y))
    return Vector((0,0))


def mouse_vector_from_window(event:Event):
    if isinstance(event, Event):
        return Vector((event.mouse_x, event.mouse_y))
    return Vector((0,0))
