# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import bpy.utils.previews
import os

# ------------------------------------------------------------------------------- #
# CONSTANTS
# ------------------------------------------------------------------------------- #

ICONS = None
NAMES = {
    'flame.png',
    'knife.png',
    'loop.png',
    'wheel.png',
}

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def directory():
    return os.path.dirname(os.path.abspath(__file__))


def icon_preview(icon_name=""):
    if icon_name in ICONS:
        return ICONS[icon_name]
    icon_dir = directory()
    return ICONS.load(icon_name, os.path.join(icon_dir, icon_name + ".png"), "IMAGE")


def icon_identifier(icon_name=""):
    if icon_name in ICONS:
        return ICONS[icon_name].icon_id
    icon_dir = directory()
    return ICONS.load(icon_name, os.path.join(icon_dir, icon_name + ".png"), "IMAGE").icon_id

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    global ICONS
    if ICONS is None:
        ICONS = bpy.utils.previews.new()
    if ICONS:
        for icon_name in NAMES:
            icon_preview(icon_name)


def unregister():
    global ICONS
    if ICONS is not None:
        bpy.utils.previews.remove(ICONS)
        ICONS = None
