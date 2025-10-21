# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Context, Event, Operator
from .. import utils

# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class KBT_OT_RND_Static(Operator):
    '''KBT R&D Static'''
    bl_label = "KBT R&D Static"
    bl_idname = 'kbt.rnd_static'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True


    def invoke(self, context:Context, event:Event):
        return self.execute(context)


    def execute(self, context:Context):
        self.report({'INFO'}, "")
        return {'FINISHED'}


    def draw(self, context:Context):
        pass
