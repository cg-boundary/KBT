# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

# R&D
from .rnd_modal import KBT_OT_RND_Modal
from .rnd_static import KBT_OT_RND_Static

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

CLASSES = (
    # R&D
    KBT_OT_RND_Modal,
    KBT_OT_RND_Static,
)


def register():
    from bpy.utils import register_class
    for cls in CLASSES:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(CLASSES):
        unregister_class(cls)
