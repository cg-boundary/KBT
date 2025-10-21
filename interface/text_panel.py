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
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "KBT"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context:Context):
        return True

# ------------------------------------------------------------------------------- #
# PANELS
# ------------------------------------------------------------------------------- #

class KBT_PT_TextPanel(KBT_Panel):
    bl_label = "Editor"

    def draw(self, context:Context):
        box = self.layout.box()
        row = box.row()
        row.label(text="KBT Panel")
