# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def print_attrs_and_values(obj, magic=False):
    # Attrs
    rows = []
    for attr in dir(obj):
        if not magic and attr.startswith('_'):
            continue
        value = getattr(obj, attr)
        rows.append((attr, str(value)))
    # Cols
    attr_width = max(len("ATTR"), max((len(a) for a, _ in rows), default=0))
    value_width = max(len("VALUE"), max((len(v) for _, v in rows), default=0))
    # Headers
    print(f"{'ATTR':<{attr_width}} | {'VALUE':<{value_width}}")
    print(f"{'-' * attr_width}-+-{'-' * value_width}")
    # Rows
    for attr, value in rows:
        print(f"{attr:<{attr_width}} | {value:<{value_width}}")
