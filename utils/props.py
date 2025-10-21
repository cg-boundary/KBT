# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import re
from uuid import uuid4

# ------------------------------------------------------------------------------- #
# UUID
# ------------------------------------------------------------------------------- #

def create_uuid():
    return str(uuid4())


def get_uuid(self):
    uuid = self.get("_uuid", '')
    if not uuid:
        self["_uuid"] = str(uuid4())
    return self["_uuid"]


def set_uuid(self, value):
    self["_uuid"] = str(value)

# ------------------------------------------------------------------------------- #
# NAME
# ------------------------------------------------------------------------------- #

def format_var_name(name: str) -> str:
    name = name.upper()
    name = re.sub(r'[^0-9A-Z_]', '_', name)
    if name and name[0].isdigit():
        name = "_" + name
    return name


def get_var_name(self):
    name = self.get("_name", "")
    if not name:
        return "VAR"
    return name


def set_var_name(self, value):
    self["_name"] = format_var_name(value)
