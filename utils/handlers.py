# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import (
    Space,
    SpaceClipEditor,
    SpaceConsole,
    SpaceDopeSheetEditor,
    SpaceFileBrowser,
    SpaceGraphEditor,
    SpaceImageEditor,
    SpaceInfo,
    SpaceNLA,
    SpaceNodeEditor,
    SpaceOutliner,
    SpacePreferences,
    SpaceProperties,
    SpaceSequenceEditor,
    SpaceSpreadsheet,
    SpaceTextEditor,
    SpaceView3D,
)
from bpy.app.handlers import persistent
from typing import (
    Callable,
    Tuple,
)
import enum
import traceback
from uuid import uuid4

# ------------------------------------------------------------------------------- #
# ENUMS
# ------------------------------------------------------------------------------- #

class SPACE_TYPES(enum.Enum):
    CLIP_EDITOR      = SpaceClipEditor
    CONSOLE          = SpaceConsole
    DOPESHEET_EDITOR = SpaceDopeSheetEditor
    EMPTY            = Space
    FILE_BROWSER     = SpaceFileBrowser
    GRAPH_EDITOR     = SpaceGraphEditor
    IMAGE_EDITOR     = SpaceImageEditor
    INFO             = SpaceInfo
    NLA_EDITOR       = SpaceNLA
    NODE_EDITOR      = SpaceNodeEditor
    OUTLINER         = SpaceOutliner
    PREFERENCES      = SpacePreferences
    PROPERTIES       = SpaceProperties
    SEQUENCE_EDITOR  = SpaceSequenceEditor
    SPREADSHEET      = SpaceSpreadsheet
    TEXT_EDITOR      = SpaceTextEditor
    VIEW_3D          = SpaceView3D

class REGION_TYPES(enum.Enum):
    ASSET_SHELF        = 'ASSET_SHELF'
    ASSET_SHELF_HEADER = 'ASSET_SHELF_HEADER'
    CHANNELS           = 'CHANNELS'
    EXECUTE            = 'EXECUTE'
    FOOTER             = 'FOOTER'
    HEADER             = 'HEADER'
    NAVIGATION_BAR     = 'NAVIGATION_BAR'
    PREVIEW            = 'PREVIEW'
    TOOLS              = 'TOOLS'
    TOOL_HEADER        = 'TOOL_HEADER'
    TOOL_PROPS         = 'TOOL_PROPS'
    UI                 = 'UI'
    WINDOW             = 'WINDOW'

class DRAW_TYPES(enum.Enum):
    BACKDROP   = 'BACKDROP'
    POST_PIXEL = 'POST_PIXEL'
    POST_VIEW  = 'POST_VIEW'
    PRE_VIEW   = 'PRE_VIEW'

# ------------------------------------------------------------------------------- #
# UTILS
# ------------------------------------------------------------------------------- #

keygen = lambda : str(uuid4())

# ------------------------------------------------------------------------------- #
# SHADER
# ------------------------------------------------------------------------------- #

class ShaderHandler:
    _HANDLERS = {}

    @classmethod
    def add(cls, cbfunc:Callable, cbargs:Tuple, space:SPACE_TYPES, regtype:REGION_TYPES, drawtype:DRAW_TYPES):
        if isinstance(cbfunc, Callable) and isinstance(cbargs, tuple):
            if space in SPACE_TYPES and regtype in REGION_TYPES and drawtype in DRAW_TYPES:
                key = keygen()
                handler = cls(key, cbfunc, cbargs, space, regtype, drawtype)
                if handler.setup():
                    cls._HANDLERS[key] = handler
                    return handler
        return None

    @classmethod
    def remove_all_handles(cls):
        handlers = list(cls._HANDLERS.values())
        for handler in handlers:
            if hasattr(handler, 'remove'):
                handler.remove()
        cls._HANDLERS.clear()

    def __init__(self, key:str, cbfunc:Callable, cbargs:Tuple, space:SPACE_TYPES, regtype:SPACE_TYPES, drawtype:DRAW_TYPES):
        self.key = key
        self.cbfunc = cbfunc
        self.cbargs = cbargs
        self.space = space
        self.regtype = regtype
        self.drawtype = drawtype
        self.is_valid = False
        self.handle = None

    def setup(self):
        space = self.space.value
        self.handle = space.draw_handler_add(self._wrapper, tuple(), self.regtype.value, self.drawtype.value)
        if self.handle:
            self.is_valid = True
            return True
        return False

    def remove(self):
        self.is_valid = False
        if self.handle:
            if self.space in SPACE_TYPES and self.regtype in REGION_TYPES:
                space = self.space.value
                try: space.draw_handler_remove(self.handle, self.regtype.value)
                except: traceback.print_exc()
        self.draw_handle = None
        if self.key in ShaderHandler._HANDLERS:
            del ShaderHandler._HANDLERS[self.key]

    def _wrapper(self):
        if self.is_valid:
            if callable(self.cbfunc):
                if isinstance(self.cbargs, tuple):
                    self.cbfunc(*self.cbargs)

# ------------------------------------------------------------------------------- #
# LOAD_PRE
# ------------------------------------------------------------------------------- #

class LoadPreHandler:
    _HANDLERS = {}

    @classmethod
    @persistent
    def load_pre_callback(cls, *args):
        for handle in cls._HANDLERS.values():
            if handle.is_valid:
                if callable(handle.cbfunc):
                    if isinstance(handle.cbargs, tuple):
                        handle.cbfunc(*handle.cbargs)

    @classmethod
    def register(cls):
        if cls.load_pre_callback not in bpy.app.handlers.load_pre:
            bpy.app.handlers.load_pre.append(cls.load_pre_callback)

    @classmethod
    def unregister(cls):
        if cls.load_pre_callback in bpy.app.handlers.load_pre:
            bpy.app.handlers.load_pre.remove(cls.load_pre_callback)

    @classmethod
    def add(cls, cbfunc:Callable, cbargs:Tuple):
        if isinstance(cbfunc, Callable) and isinstance(cbargs, tuple):
            key = keygen()
            handler = cls(key, cbfunc, cbargs)
            cls._HANDLERS[key] = handler
            return handler

    def __init__(self, key:str, cbfunc:Callable, cbargs:Tuple):
        self.key = key
        self.cbfunc = cbfunc
        self.cbargs = cbargs
        self.is_valid = True

    def remove(self):
        self.is_valid = False
        if self.key in LoadPreHandler._HANDLERS:
            del LoadPreHandler._HANDLERS[self.key]

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    ShaderHandler.remove_all_handles()
    LoadPreHandler.register()


def unregister():
    ShaderHandler.remove_all_handles()
    LoadPreHandler.unregister()
