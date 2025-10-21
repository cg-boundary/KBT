# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Context, Panel

# ------------------------------------------------------------------------------- #
# BASE
# ------------------------------------------------------------------------------- #

class KBT_Panel(Panel):
    bl_label = 'KBT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KBT"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context:Context):
        return True

# ------------------------------------------------------------------------------- #
# PANELS
# ------------------------------------------------------------------------------- #

class KBT_PT_ViewPanel(KBT_Panel):
    bl_label = "Operators"

    def draw(self, context:Context):
        box = self.layout.box()
        row = box.row()
        row.operator('kbt.rnd_modal', text="R&D Modal")
        row = box.row()
        row.operator('kbt.rnd_static', text="R&D Static")
