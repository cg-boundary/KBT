# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Context, Event
from mathutils import Vector
from enum import Enum

# ------------------------------------------------------------------------------- #
# CONSTANTS
# ------------------------------------------------------------------------------- #

class ANCHOR(Enum):
    TOP_L = 0
    TOP_C = 1
    TOP_R = 2
    MID_L = 3
    MID_C = 4
    MID_R = 5
    BOT_L = 6
    BOT_C = 7
    BOT_R = 8

# ------------------------------------------------------------------------------- #
# TYPES
# ------------------------------------------------------------------------------- #

class Data:
    def __init__(self):
        # Builder
        self.pad = 0
        # State
        self.focused = None
        # Event
        self.context = None
        self.event = None
        self.mouse = None
        # Draw
        self.gpu = None

    def update(self, context, event):
        pass

    def draw(self):
        pass


class Colors:
    def __init__(self):
        self.color_a = Vector((0.0, 0.0, 0.0, 1.0))
        self.color_b = Vector((0.0, 0.0, 0.0, 1.0))


class Bounds:
    def __init__(self):
        self.anchor = ANCHOR.MID_C
        self.colors = Colors()
        self.width = 0
        self.height = 0
        self.position = Vector((0.0, 0.0))
        self.coords = []
        self.batch_lines = None
        self.batch_polys = None

    def move(self, offset:Vector):
        pass

    def expand(self, x_min:int, x_max:int, y_min:int, y_max:int):
        pass

    def point_intersection(self, point:Vector):
        pass

    def set_batch(self):
        pass

    def draw(self, DT:Data):
        pass


class Label:
    def __init__(self):
        self.anchor = ANCHOR.MID_C
        self.bounds = Bounds()
        self.colors = Colors()
        self.font_size = 12
        self.string = ""
        self.getter = None

    def build(self, DT:Data):
        pass

    def update(self, DT:Data):
        pass

    def draw(self, DT:Data):
        pass


class Prop:
    def __init__(self):
        self.anchor = ANCHOR.MID_C
        self.bounds = Bounds()
        self.colors = Colors()
        self.label = Label()
        self.font_size = 12
        self.string = ""
        self.attr_cls = None
        self.attr_name = ""
        self.attr_data_type = ""
        self.attr_min_value = None
        self.attr_max_value = None
        self.attr_data_items = []
        self.setter = None

    def build(self, DT:Data):
        pass

    def update(self, DT:Data):
        pass

    def draw(self, DT:Data):
        pass


class Row:
    def __init__(self):
        self.bounds = Bounds()
        self.colors = Colors()
        self.elements = []

    def label(self):
        label = Label()
        self.elements.append(label)
        return label

    def prop(self):
        prop = Prop()
        self.elements.append(prop)
        return prop

    def build(self, DT:Data):
        pass

    def update(self, DT:Data):
        pass

    def draw(self, DT:Data):
        pass


class Box:
    def __init__(self):
        self.bounds = Bounds()
        self.colors = Colors()
        self.max_display_rows = 0
        self.scroll_bar_bounds = Bounds()
        self.scroll_bar_handle = Bounds()
        self.rows = []

    def row(self):
        row = Row()
        self.rows.append(row)
        return row

    def build(self, DT:Data):
        pass

    def update(self, DT:Data):
        pass

    def draw(self, DT:Data):
        pass


class Menu:
    def __init__(self):
        self.data = Data()
        self.bounds = Bounds()
        self.colors = Colors()
        self.boxes = []

    def box(self):
        box = Box()
        self.boxes.append(box)
        return box

    def build(self, context:Context, event:Event):
        pass

    def update(self, context:Context, event:Event):
        pass

    def close(self, context:Context):
        pass

    def draw(self):
        pass
