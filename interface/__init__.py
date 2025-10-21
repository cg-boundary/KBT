# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

from .text_panel import KBT_PT_TextPanel
from .view_panel import KBT_PT_ViewPanel

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

CLASSES = (
    # Text
    KBT_PT_TextPanel,
    # View 3D
    KBT_PT_ViewPanel,
)


def register():
    from bpy.utils import register_class
    for cls in CLASSES:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(CLASSES):
        unregister_class(cls)
