# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def get_addon_name():
    from .. import bl_info
    name = bl_info['name']
    return name


def user_prefs():
    name = get_addon_name()
    return bpy.context.preferences.addons[name].preferences
