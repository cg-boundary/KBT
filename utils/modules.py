# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Operator
import sys
import pkgutil
import inspect
import importlib
from types import ModuleType

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def get_importable_module_names():
    modules = set(sys.builtin_module_names)
    for module_info in pkgutil.iter_modules():
        modules.add(module_info.name)
    return sorted(modules)


def get_public_root_module_names():
    names = get_importable_module_names()
    items = {n for n in names if not n.startswith('_') and '.' not in n}
    return sorted(items, key=lambda item: item.lower())


def get_blender_module_names(standard=True):
    names = ['bpy', 'aud', 'bgl', 'bl_math', 'blf', 'bmesh', 'bpy_extras', 'freestyle', 'gpu', 'gpu_extras', 'idprop', 'imbuf', 'mathutils']
    if standard:
        return sorted(names, key=lambda item: item.lower())
    names.extend([n for n in get_importable_module_names() if n.startswith('bl_')])
    items = {n for n in names if not n.startswith('_') and '.' not in n}
    return sorted(items, key=lambda item: item.lower())


def get_standard_library_module_names():
    names = sys.stdlib_module_names
    items = {n for n in names if not n.startswith('_') and '.' not in n}
    return sorted(items, key=lambda item: item.lower())


def get_math_module_names():
    items = {'mathutils', 'numpy', 'bl_math', 'numbers', 'math', 'cmath', 'decimal', 'fractions', 'random', 'statistics'}
    return sorted(items, key=lambda item: item.lower())


def get_submodules_names_from_module(module:ModuleType):
    if isinstance(module, ModuleType):
        items = [n for n, m in inspect.getmembers(module) if isinstance(m, ModuleType) and not n.startswith('_')]
        return sorted(items, key=lambda item: item.lower())
    return []


def get_attribute_names_from_module(module:ModuleType):
    if isinstance(module, ModuleType):
        items = [n for n, m in inspect.getmembers(module) if not isinstance(m, ModuleType) and not n.startswith('_')]
        return sorted(items, key=lambda item: item.lower())
    return []


def get_module_from_name(name: str):
    if not isinstance(name, str):
        return None
    # System
    module = sys.modules.get(name)
    if isinstance(module, ModuleType):
        return module
    # Direct
    try:
        module = importlib.import_module(name)
        return module
    except ImportError:
        pass
    # Iterative
    parts = name.split(".")
    base = importlib.import_module(parts[0])
    obj = base
    for part in parts[1:]:
        obj = getattr(obj, part, None)
        if obj is None:
            return None
    return obj


def compile_source_to_module(name:str, source:str, doc:str=None):
    if isinstance(name, str) and isinstance(source, str):
        module = ModuleType(name, doc)
        exec(source, module.__dict__)
        return module
    return None

# ------------------------------------------------------------------------------- #
# BPY OPS
# ------------------------------------------------------------------------------- #

def check_bpy_ops_category_name(category:str):
    return isinstance(category, str) and category in dir(bpy.ops)


def check_bpy_ops_operator_name(category:str, operator:str):
    return isinstance(category, str) and category in dir(bpy.ops) and isinstance(operator, str) and operator in dir(getattr(bpy.ops, category))


def get_bpy_ops_category_and_operator_names_from_path(path:str):
    names = [n for n in path.split('.') if n and n not in {'bpy', 'ops'} and not n.startswith('_')]
    category = names[0] if len(names) > 0 and check_bpy_ops_category_name(names[0]) else ''
    operator = names[1] if len(names) > 1 and check_bpy_ops_operator_name(category, names[1]) else ''
    return category, operator


def get_bpy_ops_category_names():
    return sorted(attr for attr in dir(bpy.ops) if not attr.startswith('_'))


def get_bpy_ops_operator_names(category:str):
    if isinstance(category, str) and category:
        if hasattr(bpy.ops, category):
            module = getattr(bpy.ops, category)
            return sorted(attr for attr in dir(module) if not attr.startswith('_'))
    return []


def get_bpy_ops_operator_object(category:str, operator:str):
    if isinstance(category, str) and isinstance(operator, str):
        if category and operator:
            if hasattr(bpy.ops, category):
                module = getattr(bpy.ops, category)
                if hasattr(module, operator):
                    op = getattr(module, operator)
                    return op
    return None


def get_bpy_ops_from_win_man():
    context = bpy.context
    wm = context.window_manager
    return [op for op in wm.operators.items()]


def get_bpy_ops_py_string(op:Operator):
    if not isinstance(op, Operator):
        return "", "", "", ""
    bl_idname = op.bl_idname
    mod_name, func_name = bl_idname.split("_OT_", 1)
    mod_name = mod_name.lower()
    op_path_py = f"bpy.ops.{mod_name}.{func_name}"
    return op_path_py


def get_bpy_ops_info_from_win_man_at_index(last=True, index=0):
    context = bpy.context
    wm = context.window_manager
    if not wm.operators:
        return None
    operator = None
    ops = enumerate(reversed(wm.operators)) if last else enumerate(wm.operators)
    for i, op in ops:
        if i == index:
            operator = op
            break
    if operator is None:
        return None
    ops_py_string = get_bpy_ops_py_string(operator)
    wm_props = wm.operator_properties_last(operator.bl_idname)
    prop_item_info = []
    rna_props = {k : v for k, v in wm_props.bl_rna.properties.items()}
    for k in wm_props.keys():
        prop = rna_props[k]
        if not prop.is_readonly:
            prop_info = {
                'IDENTIFIER' : prop.identifier,
                'NAME'       : prop.name,
                'VALUE'      : getattr(wm_props, k),
                'DATA_TYPE'  : prop.type,
                'SUB_TYPE'   : prop.subtype if hasattr(prop, 'subtype') else 'NONE',
                'ENUM_ITEMS' : list(prop.enum_items.keys()) if prop.type == 'ENUM' else []
            }
            prop_item_info.append(prop_info)
    info = {
        'OPERATOR'   : operator,
        'WM_PROPS'   : wm_props,
        'OPS_PY_STR' : ops_py_string,
        'PROP_INFO'  : prop_item_info
    }
    return info

