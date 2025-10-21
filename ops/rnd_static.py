# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import (
    Context, Event, Operator,
)
from bpy.props import (
    BoolProperty, IntProperty, FloatProperty,
)
from .. import utils

# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class KBT_OT_RND_Static(Operator):
    '''KBT R&D Static'''
    bl_label = "KBT R&D Static"
    bl_idname = 'kbt.rnd_static'
    bl_options = {'REGISTER', 'UNDO'}
    prop_1 : BoolProperty(default=False)
    prop_2 : IntProperty(default=0)
    prop_3 : FloatProperty(default=0.0)

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
