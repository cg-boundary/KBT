# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

# Addon
from .addon_prefs import KBT_ADDON_Prefs
from .addon_settings import KBT_PROP_AddonSettings

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

CLASSES = (
    # Addon
    KBT_PROP_AddonSettings,
    KBT_ADDON_Prefs,
)


def register():
    # Classes
    from bpy.utils import register_class
    for cls in CLASSES:
        register_class(cls)


def unregister():
    # Classes
    from bpy.utils import unregister_class
    for cls in reversed(CLASSES):
        unregister_class(cls)
