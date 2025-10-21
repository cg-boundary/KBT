# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import (
    Context, Event, Operator,
)
from ..utils.handlers import (
    SPACE_TYPES, REGION_TYPES, DRAW_TYPES, ShaderHandler,
)
from ..utils.modal import (
    STATUS, add_shader_handles, remove_shader_handles,
)

# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class KBT_OT_RND_Modal(Operator):
    '''KBT R&D Modal'''
    bl_label = "KBT R&D Modal"
    bl_idname = 'kbt.rnd_modal'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context:Context):
        return True


    def invoke(self, context:Context, event:Event):
        # State
        self.status = STATUS.RUNNING
        # Handlers
        add_shader_handles(self, context, SPACE_TYPES.VIEW_3D, REGION_TYPES.WINDOW)
        # Modal
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    def modal(self, context:Context, event:Event):
        # State
        self.status = STATUS.RUNNING
        # Escape
        if event.type == 'ESC' and event.value == 'PRESS':
            self.status = STATUS.CANCELLED
        # Enter
        elif event.type == 'RET' and event.value == 'PRESS':
            self.status = STATUS.FINISHED
        # Exit
        if self.status in STATUS.FINISHED | STATUS.CANCELLED:
            return self.close(context)
        # Running
        return {'RUNNING_MODAL'}


    def close(self, context:Context):
        # Handlers
        remove_shader_handles(self)
        # State
        if self.status == STATUS.CANCELLED:
            return {'CANCELLED'}
        return {'FINISHED'}


    def cancel(self, context:Context):
        pass


    def draw_3d(self, context:Context):
        pass


    def draw_2d(self, context:Context):
        pass

