# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty,
    PointerProperty,
)

# ------------------------------------------------------------------------------- #
# PROPS
# ------------------------------------------------------------------------------- #

class KBT_PROP_AddonSettings(PropertyGroup):
    prop : BoolProperty(name="Prop", default=False)
