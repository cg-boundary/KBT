# ------------------------------------------------------------------------------- #
# ADDON
# ------------------------------------------------------------------------------- #

bl_info = {
    'name'        : "KBT",
    'author'      : "KenzoCG",
    'version'     : (1, 0, 0),
    'blender'     : (4, 5, 0),
    'location'    : "View3D",
    'category'    : "3D View",
    'description' : "KenzoCG Blender Tools",
}

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    # Utils
    from . import utils
    utils.register()
    # Resources
    from . import resources
    resources.register()
    # Props
    from . import props
    props.register()
    # Ops
    from . import ops
    ops.register()
    # Interface
    from . import interface
    interface.register()


def unregister():
    # Interface
    from . import interface
    interface.unregister()
    # Ops
    from . import ops
    ops.unregister()
    # Props
    from . import props
    props.unregister()
    # Resources
    from . import resources
    resources.unregister()
    # Utils
    from . import utils
    utils.unregister()
