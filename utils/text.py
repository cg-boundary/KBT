# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import (
    Space,
    Text,
    Window,
)
from .screen import create_new_window

# ------------------------------------------------------------------------------- #
# POLLS
# ------------------------------------------------------------------------------- #

def poll_text_editor(context):
    space = context.space_data
    if space and space.type == 'TEXT_EDITOR':
        return True
    return False


def poll_text_editor_and_text_block(context):
    space = context.space_data
    if space and space.type == 'TEXT_EDITOR':
        return isinstance(space.text, Text)
    return False

# ------------------------------------------------------------------------------- #
# DATA
# ------------------------------------------------------------------------------- #

def create_text_block(name:str=""):
    text_block = bpy.data.texts.new(name)
    return text_block

# ------------------------------------------------------------------------------- #
# SPACE
# ------------------------------------------------------------------------------- #

def get_text_block_from_active_space(context):
    space = context.space_data
    if space and space.type == 'TEXT_EDITOR':
        text = space.text
        if isinstance(text, Text):
            return text
    return None


def get_text_editor():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'TEXT_EDITOR':
                for space in area.spaces:
                    if space.type == 'TEXT_EDITOR':
                        return space
    return None


def set_text_editor_text(text_block:Text):
    if isinstance(text_block, Text):
        editor = get_text_editor()
        if editor is not None:
            editor.text = text_block
            editor.top = 0
            return True
    return False


def set_text_to_space(space:Space, text_block:Text):
    if isinstance(space, Space) and isinstance(text_block, Text):
        if space.type == 'TEXT_EDITOR':
            space.text = text_block
            space.top = 0
            return True
    return False


def create_text_editor_window_get_space():
    window = create_new_window()
    if isinstance(window, Window):
        area = window.screen.areas[0]
        area.type = 'TEXT_EDITOR'
        for space in area.spaces:
            if space.type == 'TEXT_EDITOR':
                return space
    return None
