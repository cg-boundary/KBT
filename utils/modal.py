# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import enum
from .handlers import (
    SPACE_TYPES, REGION_TYPES, DRAW_TYPES, ShaderHandler,
)

# ------------------------------------------------------------------------------- #
# ENUMS
# ------------------------------------------------------------------------------- #

class STATUS(enum.Flag):
    RUNNING     = enum.auto()
    FINISHED    = enum.auto()
    INTERFACE   = enum.auto()
    CANCELLED   = enum.auto()
    PASSTHROUGH = enum.auto()

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def add_shader_handles(op, context, space=SPACE_TYPES.VIEW_3D, regtype=REGION_TYPES.WINDOW):
    op.handler_3d, op.handler_2d = None, None
    if hasattr(op, 'draw_3d'):
        op.handler_3d = ShaderHandler.add(op.draw_3d, (context,), space, regtype, DRAW_TYPES.POST_VIEW)
    if hasattr(op, 'draw_2d'):
        op.handler_2d = ShaderHandler.add(op.draw_2d, (context,), space, regtype, DRAW_TYPES.POST_PIXEL)


def remove_shader_handles(op):
    if hasattr(op, 'handler_3d'):
        if isinstance(op.handler_3d, ShaderHandler):
            op.handler_3d.remove()
    if hasattr(op, 'handler_2d'):
        if isinstance(op.handler_2d, ShaderHandler):
            op.handler_2d.remove()
