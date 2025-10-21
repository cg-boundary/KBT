# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Context, Event, Operator
from .. import utils

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
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    def modal(self, context:Context, event:Event):
        return {'RUNNING_MODAL'}


    def close(self, context:Context):
        return {'FINISHED'}


    def cancel(self, context:Context):
        pass
