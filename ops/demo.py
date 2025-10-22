# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import bmesh
import blf
import gpu
from gpu_extras.batch import batch_for_shader
import gc

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def ensure_bmesh_type_tables_normals_selections(bm):
    if isinstance(bm, bmesh.types.BMesh) and bm.is_valid:
        tool_sel_mode = bpy.context.tool_settings.mesh_select_mode
        bm.select_mode = {mode for mode, sel in zip(['VERT', 'EDGE', 'FACE'], tool_sel_mode) if sel}
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        bm.verts.index_update()
        bm.edges.index_update()
        bm.faces.index_update()
        bm.select_history.validate()
        bm.select_flush_mode()
        bm.normal_update()
        return True
    return False

def ensure_bmesh_normals_selections(bm):
    if isinstance(bm, bmesh.types.BMesh) and bm.is_valid:
        tool_sel_mode = bpy.context.tool_settings.mesh_select_mode
        bm.select_mode = {mode for mode, sel in zip(['VERT', 'EDGE', 'FACE'], tool_sel_mode) if sel}
        bm.select_flush_mode()
        bm.normal_update()
        return True
    return False

# ------------------------------------------------------------------------------- #
# EDITOR
# ------------------------------------------------------------------------------- #

class BmeshEditor:
    def __init__(self, obj):
        # SETTINGS
        self.undo_limit = 32
        # ID Data
        self.uid = obj.session_uid
        self.obj = obj
        # MATRICES
        self.mat_ws = obj.matrix_world.copy()
        self.mat_ws_inv = obj.matrix_world.inverted_safe()
        self.mat_ws_trs = obj.matrix_world.transposed()
        # ORIGINAL BACKUP
        self.ogmesh = obj.data.copy()
        self.ogmesh_uid = self.ogmesh.session_uid
        self.ogmesh.calc_loop_triangles()
        # MESH BACKUPS
        self.backups = []
        # BMESH
        self.BM = None

    def validator(self):
        # ID DATA
        if not isinstance(self.obj, bpy.types.Object):
            return False
        try:
            # UID
            if self.obj.session_uid != self.uid:
                return False
            # OBJ TYPE
            if self.obj.type != 'MESH':
                return False
            # BACKUP MESH
            if not isinstance(self.ogmesh, bpy.types.Mesh):
                return False
            # BACKUP ID
            if self.ogmesh.session_uid != self.ogmesh_uid:
                return False
        except Exception as e:
            print(e)
            return False
        # BMESH
        return self.ensure_bmesh()

    def ensure_bmesh(self):
        if not isinstance(self.BM, bmesh.types.BMesh):
            return False
        if not self.BM.is_valid:
            self.BM.free()
            self.BM = None
            gc.collect()
            return False
        if self.obj.data.is_editmode:
            self.BM = bmesh.from_edit_mesh(self.obj.data)
        else:
            self.BM = bmesh.new(use_operators=True)
            self.BM.from_mesh(self.obj.data, face_normals=True, vertex_normals=True, use_shape_key=False, shape_key_index=0)
        if ensure_bmesh_type_tables_normals_selections(self.BM):
            return True
        return False

    def restore(self):
        if not self.validator():
            return False
        backup = self.backups[-1] if self.backups else self.ogmesh
        bmesh.ops.delete(self.BM, geom=self.BM.verts, context='VERTS')
        self.BM.from_mesh(backup, face_normals=True, vertex_normals=True, use_shape_key=False, shape_key_index=0)
        return ensure_bmesh_type_tables_normals_selections(self.BM)

    def update(self):
        if not self.validator():
            return False
        ensure_bmesh_normals_selections(self.BM)
        if self.obj.data.is_editmode:
            bmesh.update_edit_mesh(self.obj.data, loop_triangles=True, destructive=True)
        elif not self.BM.is_wrapped:
            self.BM.to_mesh(self.obj.data)
            self.obj.data.calc_loop_triangles()
        return True

    def save(self):
        if not self.update():
            return False
        if self.obj.data.is_editmode:
            self.obj.update_from_editmode()
        backup = self.obj.data.copy()
        backup.calc_loop_triangles()
        self.backups.append(backup)
        # Undo Limit
        if len(self.backups) > self.undo_limit:
            backup = self.backups[0]
            self.backups.remove(backup)
            if isinstance(backup, bpy.types.Mesh):
                if backup.session_uid != self.uid and backup.session_uid != self.ogmesh_uid:
                    if backup.name in bpy.data.meshes:
                        bpy.data.meshes.remove(backup, do_unlink=True, do_id_user=True, do_ui_user=True)
        return True

    def undo(self):
        if self.backups:
            backup = self.backups.pop()
            if isinstance(backup, bpy.types.Mesh):
                if backup.session_uid != self.uid and backup.session_uid != self.ogmesh_uid:
                    if backup.name in bpy.data.meshes:
                        bpy.data.meshes.remove(backup, do_unlink=True, do_id_user=True, do_ui_user=True)
        if self.restore():
            if self.update():
                return True
        return False

    def close(self, revert=False):
        # Remove Backups
        for backup in self.backups:
            if isinstance(backup, bpy.types.Mesh):
                if backup.session_uid != self.uid and backup.session_uid != self.ogmesh_uid:
                    if backup.name in bpy.data.meshes:
                        bpy.data.meshes.remove(backup)
        self.backups = []
        # Revert to Original Mesh
        if revert: self.restore()
        # Update Edit / Object mode mesh
        self.update()
        # Free the Bmesh
        if isinstance(self.BM, bmesh.types.BMesh):
            self.BM.free()
        self.BM = None
        if isinstance(self.obj, bpy.types.Object):
            try:
                self.obj.data.calc_loop_triangles()
            except: pass
        self.obj = None
        if isinstance(self.ogmesh, bpy.types.Mesh):
            try:
                if self.ogmesh.session_uid != self.uid:
                    if self.ogmesh.name in bpy.data.meshes:
                        bpy.data.meshes.remove(self.ogmesh)
            except: pass
        self.ogmesh = None
        # Delete
        del self.uid
        del self.obj
        del self.mat_ws
        del self.mat_ws_inv
        del self.mat_ws_trs
        del self.ogmesh
        del self.backups
        del self.BM

# ------------------------------------------------------------------------------- #
# MODAL
# ------------------------------------------------------------------------------- #

class SimpleModalOperator(bpy.types.Operator):
    bl_idname = "view3d.simple_modal"
    bl_label = "Simple Modal"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'EDIT_MESH'

    def invoke(self, context, event):
        # Props
        self.mouse_path = []
        self.prev_mouse = event.mouse_region_x
        self.bevel_width = 0
        # Handle
        add = bpy.types.SpaceView3D.draw_handler_add
        self._handle = add(self.draw_2d, (context, ), 'WINDOW', 'POST_PIXEL')
        self.shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
        # Editor
        obj = context.edit_object
        self.editor = BmeshEditor(obj)
        # Modal
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # Draw
        context.area.tag_redraw()
        # Update
        if not self.update(context, event):
            return self.close(context)
        # Mouse
        if event.type == 'MOUSEMOVE':
            coord = (event.mouse_region_x, event.mouse_region_y)
            self.mouse_path.append(coord)
        # Exit
        elif event.type == 'ESC':
            return self.close(context)
        # Run
        return {'RUNNING_MODAL'}

    def close(self, context):
        # Draw
        context.area.tag_redraw()
        # Handle
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        # Editor
        self.editor.close(revert=True)
        # Cancel
        return {'CANCELLED'}

    def update(self, context, event):
        # Error
        if not self.editor.validator():
            print("Not Validated")
            return False
        # Offset
        self.bevel_width += event.mouse_region_x - self.prev_mouse
        self.prev_mouse = event.mouse_region_x
        # Editor
        if not self.editor.restore():
            print("Not Restored")
            return False
        bm = self.editor.BM
        # edges
        edges = [edge for edge in bm.edges if edge.select]
        if not edges:
            return False
        # Ops
        bmesh.ops.bevel(
            bm,
            geom=edges,
            offset=self.bevel_width,
            offset_type='OFFSET',
            profile_type='SUPERELLIPSE',
            segments=3,
            profile=1,
            affect='EDGES',
            clamp_overlap=False,
            material=0,
            loop_slide=True,
            mark_seam=False,
            mark_sharp=False,
            harden_normals=False,
            face_strength_mode='NONE',
            miter_outer='SHARP',
            miter_inner='SHARP',
            spread=0,
            vmesh_method='ADJ')
        # Editor
        self.editor.update()
        # Valid
        return True

    def draw_2d(self, context):
        blf.position(0, 15, 30, 0)
        blf.size(0, 20.0)
        blf.draw(0, f"{self.bevel_width}")
        gpu.state.blend_set('ALPHA')
        self.shader.uniform_float("color", (0.0, 0.0, 0.0, 0.5))
        self.shader.uniform_float("viewportSize", (context.area.width, context.area.height))
        self.shader.uniform_float('lineWidth', 2.0)
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": self.mouse_path})
        batch.draw(self.shader)
        gpu.state.blend_set('NONE')

def register():
    bpy.utils.register_class(SimpleModalOperator)

def unregister():
    bpy.utils.unregister_class(SimpleModalOperator)

if __name__ == "__main__":
    register()
