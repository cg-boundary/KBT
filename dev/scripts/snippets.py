

import bpy

# ------------------------------------------------------------------------------- #
# NODE TREE
# ------------------------------------------------------------------------------- #

tree = None
for area in bpy.context.screen.areas:
    if area.type == 'NODE_EDITOR':
        for space in area.spaces:
            if space.type == 'NODE_EDITOR' and hasattr(space, 'node_tree'):
                if space.node_tree and space.node_tree.bl_idname == 'PYN_NodeTree':
                    tree = space.node_tree
                    break

node = tree.nodes.active

# ------------------------------------------------------------------------------- #
# TEXT EDITOR
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Text

def get_text_editor():
    for area in bpy.context.screen.areas:
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
            return True
    return False

# ------------------------------------------------------------------------------- #
# GEN SPACE TYPES
# ------------------------------------------------------------------------------- #

#--- Space Types Generator ---#
space_types = {}
area = [area for area in bpy.context.screen.areas if area.type == 'OUTLINER'][0]
for key in bpy.types.Area.bl_rna.properties['type'].enum_items.keys():
    area.type = key
    for space in area.spaces:
        space_types[space.type] = type(space)

for sn, st in sorted(space_types.items()):
    print(sn, st)

#--- Region Types Generator ---#
reg_types = set()
area = [area for area in bpy.context.screen.areas if area.type == 'OUTLINER'][0]
for key in bpy.types.Area.bl_rna.properties['type'].enum_items.keys():
    area.type = key
    for region in area.regions:
        reg_types.add(region.type)

for rn in sorted(reg_types):
    print(rn)

# ------------------------------------------------------------------------------- #
# ALL GEO NODES
# ------------------------------------------------------------------------------- #

tree = None
for area in bpy.context.screen.areas:
    if area.type == 'NODE_EDITOR':
        for space in area.spaces:
            if space.type == 'NODE_EDITOR' and hasattr(space, 'node_tree'):
                if space.node_tree.bl_idname == 'GeometryNodeTree':
                    tree = space.node_tree
                    break

nodes = []
if tree:
    for attr in dir(bpy.types):
        if not attr.startswith('_'):
            node = getattr(bpy.types, attr)
            if issubclass(node, bpy.types.Node):
                if node.poll(tree):
                    try:
                        node = tree.nodes.new(attr)
                        nodes.append(node)
                    except: pass

cat_nodes = {}
for node in nodes:
    cat_nodes.setdefault(node.color_tag, []).append(node)

y = 0
for nodes_list in cat_nodes.values():
    x = 0
    max_h = 0
    for node in nodes_list:
        node.location = (x, y)
        x += node.dimensions.x + 20
        if node.dimensions.y > max_h:
            max_h = node.dimensions.y
    y -= max_h
