# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

from bpy.types import AddonPreferences
from bpy.props import EnumProperty, PointerProperty
from ..utils import addon
from .addon_settings import KBT_PROP_AddonSettings

# ------------------------------------------------------------------------------- #
# ADDON
# ------------------------------------------------------------------------------- #

TAB_OPTS = (
    ('SETTINGS', "Settings", ""),
)


class KBT_ADDON_Prefs(AddonPreferences):
    bl_idname = addon.get_addon_name()
    settings : PointerProperty(type=KBT_PROP_AddonSettings)
    tabs: EnumProperty(items=TAB_OPTS, default='SETTINGS')


    def draw(self, context):
        layout = self.layout
        if self.tabs == 'SETTINGS':
            pass
