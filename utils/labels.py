
# ---------------------------------------- Imports

import bpy
import gpu
import blf
from bpy.types import Context, Event
from mathutils import Vector
from uuid import uuid4
from enum import Enum

# ---------------------------------------- Enums

class STATUS(Enum):
    ACTIVE = 0
    LOCKED = 1
    CLOSED = 2

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

class DTYPE(Enum):
    NONE    = 0
    BOOL    = 1
    INT     = 2
    FLOAT   = 3
    STRING  = 4
    VECTOR  = 5
    LIST    = 6
    COLOR   = 7

class ETYPE(Enum):
    NONE   = 0
    LABEL  = 1
    BUTTON = 2
    INPUT  = 3
    COLOR  = 4

# ---------------------------------------- Utils

keygen = lambda : str(uuid4())

def user_prefs():
    return bpy.context.preferences.addons['KBT'].preferences

def screen_factor():
    return bpy.context.preferences.system.ui_scale

def ensure_anchor(anchor:ANCHOR):
    if anchor and isinstance(anchor, ANCHOR):
        return anchor
    return ANCHOR.MID_C

def ensure_dtype(dtype:DTYPE):
    if dtype and isinstance(dtype, DTYPE):
        return dtype
    return DTYPE.NONE

def ensure_etype(etype:ETYPE):
    if etype and isinstance(etype, ETYPE):
        return etype
    return ETYPE.NONE

def mouse_region_vector(event:Event):
    if isinstance(event, Event):
        return Vector((event.mouse_region_x, event.mouse_region_y))
    return Vector((0,0))

ALPHANUMERIC = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()-_=+,./?;:'\"[]{}\\|"

def get_text_max_height(size:int):
    size = int(size * screen_factor())
    blf.size(0, size)
    return blf.dimensions(0, ALPHANUMERIC)[1]

def get_text_descender_height(size:int):
    size = int(size * screen_factor())
    blf.size(0, size)
    full_descend = blf.dimensions(0, ALPHANUMERIC)[1]
    none_descend = blf.dimensions(0, "ABC123!`")[1]
    return full_descend - none_descend

# ---------------------------------------- Data

class Data:
    def __init__(self, context:Context, event:Event):
        # State
        self.status = STATUS.ACTIVE
        self.locked_widget = None
        # User
        self.prefs = user_prefs()
        # Context
        self.context = context
        self.area  = context.area
        self.space = context.space_data
        # Event
        self.event = event
        self.mouse = mouse_region_vector(event)
        self.key_type = event.type
        self.key_press = event.value
        # Builder
        self.factor = screen_factor()

    def update(self, context:Context, event:Event):
        # Context
        self.context = context
        self.area  = context.area
        self.space = context.space_data
        # Event
        self.event = event
        self.mouse = mouse_region_vector(event)
        self.key_type = event.type
        self.key_press = event.value

    def locked_widget_active(self):
        if isinstance(self.locked_widget, (Box, Row, Element)):
            return True
        self.locked_widget = None
        return False

# ---------------------------------------- Components

class Label:
    def __init__(self, anchor:ANCHOR, text:str):
        prefs = user_prefs()
        self.anchor = ensure_anchor(anchor)
        self.text = text
        self.size = int(prefs.font_size * screen_factor())
        self.color_primary = prefs.font_color_primary
        self.color_secondary = prefs.font_color_secondary
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def build(self):
        if not self.text or not isinstance(self.text, str):
            self.w = 0
            self.h = 0
        else:
            factor = screen_factor()
            size = int(self.size * factor)
            blf.size(0, size)
            self.w, self.h = blf.dimensions(0, self.text)

    def draw(self):
        blf.size(0, self.size)
        blf.position(0, self.x, self.y, 0)
        blf.color(0, *self.color_primary)
        blf.draw(0, self.text)

class Prop:
    def __init__(self, obj:object, attr:str, dtype:DTYPE, index:int, callback:None):
        self.obj = obj
        self.attr = attr
        self.dtype = dtype
        self.index = index
        self.callback = callback
        self.label = Label(ANCHOR.MID_C, text="")

    def get_value(self):
        if isinstance(self.attr, str):
            if hasattr(self.obj, self.attr):
                value = getattr(self.obj, self.attr)
                if isinstance(value, list) and isinstance(self.index, int):
                    if self.index >= 0 and self.index < len(value):
                        return value[self.index]
                return value
        return None

    def set_label_text(self):
        value = self.get_value()
        if self.dtype == DTYPE.NONE:
            self.label.text = ""
        elif self.dtype == DTYPE.BOOL:
            self.label.text = "On" if value else "Off"
        elif self.dtype == DTYPE.INT:
            self.label.text = str(int(value))
        elif self.dtype == DTYPE.FLOAT:
            self.label.text = str(float(value))
        elif self.dtype == DTYPE.STRING:
            self.label.text = str(value)
        elif self.dtype == DTYPE.LIST:
            self.label.text = str(value)
        elif self.dtype in {DTYPE.VECTOR, DTYPE.COLOR}:
            if len(value) == 2:
                self.label.text = f"({value[0]}, {value[1]})"
            elif len(value) == 3:
                self.label.text = f"({value[0]}, {value[1]}, {value[2]})"
            elif len(value) == 4:
                self.label.text = f"({value[0]}, {value[1]}, {value[2]}, {value[3]})"

class Bounds:
    def __init__(self, anchor:ANCHOR):
        prefs = user_prefs()
        self.anchor = ensure_anchor(anchor)
        self.color_border = prefs.border_color
        self.color_background = prefs.background_color
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def test_point_intersect(self, point:Vector):
        if point.x >= self.x:
            if point.x <= self.x + self.w:
                if point.y >= self.y:
                    if point.y <= self.y + self.h:
                        return True
        return False

    def to_quad_points(self):
        lx = self.x
        by = self.y
        rx = self.x + self.w
        ty = self.y + self.h
        bot_L = Vector((lx, by))
        top_L = Vector((lx, ty))
        top_R = Vector((rx, ty))
        bot_R = Vector((rx, by))
        return bot_L, top_L, top_R, bot_R

    def gen_batches(self, tris=True, lines=True):
        bot_L, top_L, top_R, bot_R = self.to_quad_points()

    def draw(self):
        pass

# ---------------------------------------- Widgets

class Element:
    def __init__(self, etype:ETYPE, prop:Prop):
        self.key = keygen()
        self.etype = ensure_etype(etype)
        self.prop = prop
        self.label = Label()
        self.bounds = Bounds(anchor=ANCHOR.MID_C)

    def build(self, dt:Data):
        if self.etype == ETYPE.NONE:
            pass
        elif self.etype == ETYPE.LABEL:
            pass
        elif self.etype == ETYPE.BUTTON:
            pass
        elif self.etype == ETYPE.INPUT:
            pass
        elif self.etype == ETYPE.COLOR:
            pass

    def update(self, dt:Data):
        return True

    def draw(self, dt:Data):
        self.bounds.draw()

class Row:
    def __init__(self):
        self.key = keygen()
        self.bounds = Bounds(ANCHOR.MID_C)
        self.elements = []

    def element(self, etype:ETYPE, prop:Prop):
        element = Element()
        self.elements.append(element)
        return element

    def build(self, dt:Data):
        for element in self.elements:
            element.build(dt)

    def update(self, dt:Data):
        if self.bounds.test_point_intersect(dt.mouse):
            for element in self.elements:
                if not element.update(dt):
                    return False
        return True

    def draw(self, dt:Data):
        self.bounds.draw()
        for element in self.elements:
            element.draw(self.dt)

class Box:
    def __init__(self):
        self.key = keygen()
        self.bounds = Bounds(ANCHOR.MID_C)
        self.rows = []

    def row(self):
        row = Row()
        self.rows.append(row)
        return row

    def build(self, dt:Data):
        for row in self.rows:
            row.build(dt)

    def update(self, dt:Data):
        if self.bounds.test_point_intersect(dt.mouse):
            for row in self.rows:
                if not row.update(dt):
                    return False
        return True

    def draw(self, dt:Data):
        self.bounds.draw()
        for row in self.rows:
            row.draw(self.dt)

class Window:
    def __init__(self, context:Context, event:Event):
        self.dt = Data(context, event)
        self.key = keygen()
        self.bounds = Bounds(ANCHOR.MID_C)
        self.boxes = []

    def box(self):
        box = Box()
        self.boxes.append(box)
        return box

    def build(self):
        for box in self.boxes:
            box.build(self.dt)

    def update(self, context:Context, event:Event):
        self.dt.update(context, event)
        if self.dt.locked_widget_active():
            self.dt.status = STATUS.LOCKED
            widget = self.dt.locked_widget
            if not widget.update(self.dt):
                self.dt.locked_widget = None
        elif self.bounds.test_point_intersect(self.dt.mouse):
            for box in self.boxes:
                if not box.update(self.dt):
                    break
        return self.dt.status

    def draw(self, context:Context):
        self.bounds.draw()
        for box in self.boxes:
            box.draw(self.dt)

    def close(self, context:Context):
        pass
