# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

from . import addon
from . import algos
from . import debug
from . import event
from . import graphics
from . import handlers
from . import labels
from . import maths
from . import modules
from . import props
from . import screen
from . import text

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    handlers.register()


def unregister():
    handlers.unregister()
