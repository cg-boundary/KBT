# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def yield_item_with_frequency(items, parts:int=1, interrupter=None):
    if parts <= 0:
        raise ValueError("Parts must be greater than 0")
    n = len(items) // parts
    if n == 0:
        raise ValueError("Parts is greater than list length")
    for i, item in enumerate(items):
        yield item
        if i % n == 0:
            yield interrupter
