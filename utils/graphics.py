# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import blf
from typing import Iterable
from mathutils import Vector
from enum import Enum
from typing import Iterable
from .screen import screen_factor

# ------------------------------------------------------------------------------- #
# CONSTANTS
# ------------------------------------------------------------------------------- #

ALPHANUMERIC = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()-_=+,./?;:'\"[]{}\\|"

# ------------------------------------------------------------------------------- #
# 2D
# ------------------------------------------------------------------------------- #

def gen_points_batch_2D():
    pass


def gen_lines_batch_2D():
    pass


def gen_tris_batch_2D():
    pass

# ------------------------------------------------------------------------------- #
# TEXT
# ------------------------------------------------------------------------------- #

def draw_text(text:str, x:float, y:float, size:int=12, color:Iterable=(1.0, 1.0, 1.0, 1.0)):
    blf.size(0, int(size * screen_factor()))
    blf.position(0, x, y, 0)
    blf.color(0, *color)
    blf.draw(0, text)


def get_text_width(text:str, size:int):
    blf.size(0, int(size * screen_factor()))
    return blf.dimensions(0, text)[0]


def get_text_width_and_height(text:str, size:int):
    blf.size(0, int(size * screen_factor()))
    return blf.dimensions(0, text)


def get_text_max_height(size:int):
    blf.size(0, int(size * screen_factor()))
    return blf.dimensions(0, ALPHANUMERIC)[1]


def get_text_descender_height(size:int):
    blf.size(0, int(size * screen_factor()))
    standard = blf.dimensions(0, "ABC123!`")[1]
    descend = blf.dimensions(0, ALPHANUMERIC)[1]
    return descend - standard

# ------------------------------------------------------------------------------- #
# TYPES
# ------------------------------------------------------------------------------- #

class Msgs:
    def __init__(self, size=12, padding=10, color_a=(1.0, 1.0, 1.0, 1.0), color_b=(1.0, 1.0, 1.0, 1.0)):
        self.msgs = []
        self.size = size
        self.color_a = color_a
        self.color_b = color_b
        self.factor = screen_factor()
        self.padding = padding * self.factor
        self.text_height = get_text_max_height(self.size)
        self.y_offset = self.text_height + self.padding


    def clear(self):
        self.msgs.clear()


    def add(self, msg_a="", msg_b=""):
        msg_a = msg_a if isinstance(msg_a, str) else ""
        msg_b = msg_b if isinstance(msg_b, str) else ""
        x_offset = get_text_width(msg_a, self.size)
        x_offset += self.padding
        self.msgs.append((msg_a, x_offset, msg_b))


    def draw(self, x=0, y=0, reverse=True):
        msgs = reversed(self.msgs) if reverse else self.msgs
        for msg_a, x_offset, msg_b in msgs:
            draw_text(msg_a, x, y, self.size, self.color_a)
            draw_text(msg_b, x + x_offset, y, self.size, self.color_b)
            y += self.y_offset

