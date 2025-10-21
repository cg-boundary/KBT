# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bmesh
from bpy.types import Object
from mathutils import Vector, Quaternion, Matrix
from mathutils import geometry
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
import math
import random

# ------------------------------------------------------------------------------- #
# VALUE
# ------------------------------------------------------------------------------- #

def clamp_value(value:float=0.0, min_val:float=0.0, max_val:float=0.0):
    """Returns the value clamped between min and max"""
    if min_val > max_val:
        min_val, max_val = max_val, min_val 
    return max(min_val, min(value, max_val))


def remap_value(value:float=0.0, min_a:float=0.0, max_a:float=0.0, min_b:float=0.0, max_b:float=0.0):
    """Returns the value remapped from min/max A -> min/max B"""
    if min_a == max_a:
        return min_b
    return min_b + ((value - min_a) / (max_a - min_a)) * (max_b - min_b)


def round_value_to_increment(value:float=0.0, increment:float=15.0):
    """Returns a rounded value aligned with the increment"""
    if increment == 0:
        return round(value)
    return round(value / increment) * increment


def random_float(min_val:float=0.0, max_val:float=1.0):
    """Returns a random float value in the range of min_val and max_val"""
    return random.uniform(min_val, max_val)

# ------------------------------------------------------------------------------- #
# VECTOR
# ------------------------------------------------------------------------------- #

def center_of_points(points=None):
    """Returns the center point of the points or None on failure"""
    if not points or not isinstance(points, (list, tuple, set)):
        return None
    summed = Vector((0,0,0))
    for point in points:
        summed += point
    return summed / len(points)


def random_vector(min_val:float=0.0, max_val:float=1.0):
    """Returns a random vector in the range of min_val and max_val"""
    gen = random.uniform
    return Vector((gen(min_val, max_val), gen(min_val, max_val), gen(min_val, max_val)))


def random_uniform_vector(min_val:float=0.0, max_val:float=1.0):
    """Returns a random uniform vector in the range of min_val and max_val"""
    gen = random.uniform
    val = gen(min_val, max_val)
    return Vector((val, val, val))

# ------------------------------------------------------------------------------- #
# MATRIX
# ------------------------------------------------------------------------------- #

def loc_to_matrix_4x4(loc:Vector):
    """Returns a 4x4 translation matrix from the location vector or None on failure"""
    if not isinstance(loc, Vector) or len(loc) != 3:
        return None
    return Matrix.Translation(loc)


def quat_to_matrix_4x4(quat:Quaternion):
    """Returns a 4x4 rotation matrix from the quaternion value or None on failure"""
    if not isinstance(quat, Quaternion):
        return None
    return quat.to_matrix().to_4x4()


def sca_to_matrix_4x4(sca:Vector):
    """Returns a 4x4 diagonal matrix from the scale vector or None on failure"""
    if not isinstance(sca, Vector) or len(sca) != 3:
        return None
    return Matrix.Diagonal(sca).to_4x4()


def loc_sca_to_matrix_4x4(loc:Vector, sca:Vector):
    """Returns a 4x4 matrix from the location and scale vectors or None on failure"""
    if not isinstance(loc, Vector) or len(loc) != 3:
        return None
    if not isinstance(sca, Vector) or len(sca) != 3:
        return None
    return Matrix.Translation(loc) @ Matrix.Diagonal(sca).to_4x4()


def vectors_to_matrix_4x4(dir_1:Vector, dir_2:Vector):
    """Returns a 4x4 rotation matrix aligning direction 1 and 2 or None on failure"""
    if not isinstance(dir_1, Vector) or len(dir_1) != 3:
        return None
    if not isinstance(dir_2, Vector) or len(dir_2) != 3:
        return None
    if dir_1.length == 0 or dir_2.length == 0:
        return Matrix.Identity(4)
    dir_1 = dir_1.normalized()
    dir_2 = dir_2.normalized()
    return dir_1.rotation_difference(dir_2).to_matrix().to_4x4()


def plane_matrix(point:Vector, normal:Vector):
    """Returns a 4x4 matrix for a plane at point with given normal (Z-axis aligned) or None on failure"""
    if not isinstance(point, Vector) or len(point) != 3:
        return None
    if not isinstance(normal, Vector) or len(normal) != 3:
        return None
    if normal.length == 0:
        return None
    loc_mat = Matrix.Translation(point)
    rot_quat = normal.normalized().to_track_quat('Z', 'Y')
    rot_mat = rot_quat.to_matrix().to_4x4()
    return loc_mat @ rot_mat


def transposed_rot_matrix(matrix:Matrix):
    """Returns a 4x4 matrix from the transpose of the matrix or None on failure"""
    if not isinstance(matrix, Matrix):
        return None
    return matrix.to_3x3().transposed().to_4x4()


def normal_transform_matrix(matrix:Matrix):
    """Returns a 4x4 matrix for transforming normals from one space to another or None on failure"""
    if not isinstance(matrix, Matrix):
        return None
    return matrix.to_3x3().inverted_safe().transposed().to_4x4()


def remove_location_from_matrix(matrix:Matrix):
    """Returns a 4x4 matrix with location set to identity or None on failure"""
    if not isinstance(matrix, Matrix):
        return None
    if len(matrix) != 4:
        matrix = matrix.to_4x4()
    loc, rot, sca = matrix.decompose()
    rot_mat = rot.to_matrix().to_4x4()
    sca_mat = Matrix.Diagonal(sca).to_4x4()
    return rot_mat @ sca_mat


def remove_rotation_from_matrix(matrix:Matrix):
    """Returns a 4x4 matrix with rotation set to identity or None on failure"""
    if not isinstance(matrix, Matrix):
        return None
    if len(matrix) != 4:
        matrix = matrix.to_4x4()
    loc, rot, sca = matrix.decompose()
    loc_mat = Matrix.Translation(loc)
    sca_mat = Matrix.Diagonal(sca).to_4x4()
    return loc_mat @ sca_mat


def remove_scale_from_matrix(matrix:Matrix):
    """Returns a 4x4 matrix with scale set to identity or None on failure"""
    if not isinstance(matrix, Matrix):
        return None
    if len(matrix) != 4:
        matrix = matrix.to_4x4()
    loc, rot, sca = matrix.decompose()
    sca = Vector((1,1,1,))
    return Matrix.LocRotScale(loc, rot, sca)

# ------------------------------------------------------------------------------- #
# TRIANGLES
# ------------------------------------------------------------------------------- #

def normal_from_triangle(p1:Vector, p2:Vector, p3:Vector):
    """Returns the triangle's face normal or None on failure"""
    if not isinstance(p1, Vector) or len(p1) != 3:
        return None
    if not isinstance(p2, Vector) or len(p2) != 3:
        return None
    if not isinstance(p3, Vector) or len(p3) != 3:
        return None
    return geometry.normal((p1, p2, p3))


def triangles_from_object_bounds(obj:Object, transform=True):
    """Returns a list of vector triplets that represent the bounding box triangulated or None on failure"""
    if not isinstance(obj, Object) or not hasattr(obj, 'bound_box'):
        return None
    bb = obj.bound_box
    if not bb:
        return None
    mat = obj.matrix_world if transform else Matrix.Identity(3)
    p1 = mat @ Vector((bb[0][0], bb[0][1], bb[0][2]))
    p2 = mat @ Vector((bb[1][0], bb[1][1], bb[1][2]))
    p3 = mat @ Vector((bb[2][0], bb[2][1], bb[2][2]))
    p4 = mat @ Vector((bb[3][0], bb[3][1], bb[3][2]))
    p5 = mat @ Vector((bb[4][0], bb[4][1], bb[4][2]))
    p6 = mat @ Vector((bb[5][0], bb[5][1], bb[5][2]))
    p7 = mat @ Vector((bb[6][0], bb[6][1], bb[6][2]))
    p8 = mat @ Vector((bb[7][0], bb[7][1], bb[7][2]))
    return [
    (p2, p6, p7), (p2, p7, p3), # Top
    (p1, p4, p8), (p1, p8, p5), # Bottom
    (p5, p8, p7), (p5, p7, p6), # Right
    (p4, p1, p2), (p4, p2, p3), # Left
    (p1, p5, p6), (p1, p6, p2), # Front
    (p8, p4, p3), (p8, p3, p7)] # Back


def scale_triangle_from_center(p1:Vector, p2:Vector, p3:Vector, scalar:float=1.0):
    """Returns 3 vectors scaled uniformly from the center or (None, None, None) on failure"""
    if not isinstance(p1, Vector) or len(p1) != 3:
        return None, None, None
    if not isinstance(p2, Vector) or len(p2) != 3:
        return None, None, None
    if not isinstance(p3, Vector) or len(p3) != 3:
        return None, None, None
    center = (p1 + p2 + p3) / 3
    factor = math.sqrt(scalar)
    v1_offset = ((p1 - center) * factor) + center
    v2_offset = ((p2 - center) * factor) + center
    v3_offset = ((p3 - center) * factor) + center
    return v1_offset, v2_offset, v3_offset

# ------------------------------------------------------------------------------- #
# BVH TREES
# ------------------------------------------------------------------------------- #

def bvh_tree_from_object_bounds(obj:Object, scalar:float=1.0):
    """Returns a BVH Tree from the objects bounding box or None on failure"""
    if not isinstance(obj, Object) or not hasattr(obj, 'bound_box'):
        return None
    bb = obj.bound_box
    if not bb:
        return None
    norm = 0.5773502588272095
    mat_ws = obj.matrix_world
    verts = [
        (mat_ws @ Vector((bb[0][0], bb[0][1], bb[0][2]))) + Vector((-norm, -norm, -norm)) * scalar,
        (mat_ws @ Vector((bb[1][0], bb[1][1], bb[1][2]))) + Vector((-norm, -norm,  norm)) * scalar,
        (mat_ws @ Vector((bb[2][0], bb[2][1], bb[2][2]))) + Vector((-norm,  norm,  norm)) * scalar,
        (mat_ws @ Vector((bb[3][0], bb[3][1], bb[3][2]))) + Vector((-norm,  norm, -norm)) * scalar,
        (mat_ws @ Vector((bb[4][0], bb[4][1], bb[4][2]))) + Vector(( norm, -norm, -norm)) * scalar,
        (mat_ws @ Vector((bb[5][0], bb[5][1], bb[5][2]))) + Vector(( norm, -norm,  norm)) * scalar,
        (mat_ws @ Vector((bb[6][0], bb[6][1], bb[6][2]))) + Vector(( norm,  norm,  norm)) * scalar,
        (mat_ws @ Vector((bb[7][0], bb[7][1], bb[7][2]))) + Vector(( norm,  norm, -norm)) * scalar
    ]
    polys = ((1, 5, 6), (1, 6, 2), (0, 3, 7), (0, 7, 4), (4, 7, 6), (4, 6, 5), (3, 0, 1), (3, 1, 2), (0, 4, 5), (0, 5, 1), (7, 3, 2), (7, 2, 6))
    return BVHTree.FromPolygons(verts, polys, all_triangles=True, epsilon=0.0)


def bvh_tree_from_bmesh_bounds(bm:bmesh.types.BMesh, mat_ws:Matrix, scalar:float=1.0):
    """Returns a BVH Tree from the bmesh bounding box or None on failure"""
    if not isinstance(bm, bmesh.types.BMesh):
        return None
    if not bm.is_valid:
        return None
    if not isinstance(mat_ws, Matrix):
        return None
    min_vec = Vector((float('inf'), float('inf'), float('inf')))
    max_vec = Vector((float('-inf'), float('-inf'), float('-inf')))
    for vert in bm.verts:
        if vert.is_valid:
            min_vec.x = min(min_vec.x, vert.co.x)
            min_vec.y = min(min_vec.y, vert.co.y)
            min_vec.z = min(min_vec.z, vert.co.z)
            max_vec.x = max(max_vec.x, vert.co.x)
            max_vec.y = max(max_vec.y, vert.co.y)
            max_vec.z = max(max_vec.z, vert.co.z)
    norm = 0.5773502588272095
    verts = [
        (mat_ws @ Vector((min_vec.x, min_vec.y, min_vec.z))) + Vector((-norm, -norm, -norm)) * scalar,
        (mat_ws @ Vector((min_vec.x, min_vec.y, max_vec.z))) + Vector((-norm, -norm,  norm)) * scalar,
        (mat_ws @ Vector((min_vec.x, max_vec.y, max_vec.z))) + Vector((-norm,  norm,  norm)) * scalar,
        (mat_ws @ Vector((min_vec.x, max_vec.y, min_vec.z))) + Vector((-norm,  norm, -norm)) * scalar,
        (mat_ws @ Vector((max_vec.x, min_vec.y, min_vec.z))) + Vector(( norm, -norm, -norm)) * scalar,
        (mat_ws @ Vector((max_vec.x, min_vec.y, max_vec.z))) + Vector(( norm, -norm,  norm)) * scalar,
        (mat_ws @ Vector((max_vec.x, max_vec.y, max_vec.z))) + Vector(( norm,  norm,  norm)) * scalar,
        (mat_ws @ Vector((max_vec.x, max_vec.y, min_vec.z))) + Vector(( norm,  norm, -norm)) * scalar
    ]
    polys = ((1, 5, 6), (1, 6, 2), (0, 3, 7), (0, 7, 4), (4, 7, 6), (4, 6, 5), (3, 0, 1), (3, 1, 2), (0, 4, 5), (0, 5, 1), (7, 3, 2), (7, 2, 6))
    return BVHTree.FromPolygons(verts, polys, all_triangles=True, epsilon=0.0)

# ------------------------------------------------------------------------------- #
# KD TREES
# ------------------------------------------------------------------------------- #

def kd_tree_from_points(points=None):
    """Returns a KD Tree from the points, index for points is based on list order or None on failure"""
    if not points or not isinstance(points, (list, tuple, set)):
        return None
    points = [p for p in points if isinstance(p, Vector) and len(p) == 3]
    kd_tree = KDTree(len(points))
    for index, point in enumerate(points):
        kd_tree.insert(point, index)
    kd_tree.balance()
    return kd_tree

# ------------------------------------------------------------------------------- #
# SPHERES
# ------------------------------------------------------------------------------- #

def sphere_from_obj_bounds(obj:Object):
    """Returns (Center, Radius) from the object bounds or (None, None) on failure"""
    if not isinstance(obj, Object) or not hasattr(obj, 'bound_box'):
        return None, None
    bb = obj.bound_box
    if not bb:
        return None, None
    mat_ws = obj.matrix_world
    center = Vector((0, 0, 0))
    corners = [mat_ws @ Vector(corner) for corner in bb]
    for corner in corners:
        center += corner
    center /= 8.0
    radius = max((corner - center).length for corner in corners)
    return center, radius

# ------------------------------------------------------------------------------- #
# RECTANGLES
# ------------------------------------------------------------------------------- #

def rectangle_from_bounds_2d(points=None):
    """Returns (Top left vector 2D, Bottom right vector 2D) or (None, None) on failure"""
    if not points or not isinstance(points, (list, tuple, set)):
        return None, None
    points = [point for point in points if isinstance(point, Vector) and len(point) == 2]
    indices = geometry.convex_hull_2d(points)
    if not indices:
        return None, None
    corners = [points[index] for index in indices]
    x_coords = [point.x for point in corners]
    y_coords = [point.y for point in corners]
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    top_left = Vector((min_x, max_y))
    bot_right = Vector((max_x, min_y))
    return top_left, bot_right

# ------------------------------------------------------------------------------- #
# BOUNDS
# ------------------------------------------------------------------------------- #

def bounding_box_wires_and_corners(obj:Object, scalar:float=1.0):
    """Returns (List of bounding box points, List of bounding box edges for each face) or (None, None)"""
    if not isinstance(obj, Object) or not hasattr(obj, 'bound_box'):
        return None, None
    bb = obj.bound_box
    if not bb:
        return None, None
    mat_ws = obj.matrix_world
    norm = 0.5773502588272095
    p1 = (mat_ws @ Vector((bb[0][0], bb[0][1], bb[0][2]))) + Vector((-norm, -norm, -norm)) * scalar
    p2 = (mat_ws @ Vector((bb[1][0], bb[1][1], bb[1][2]))) + Vector((-norm, -norm,  norm)) * scalar
    p3 = (mat_ws @ Vector((bb[2][0], bb[2][1], bb[2][2]))) + Vector((-norm,  norm,  norm)) * scalar
    p4 = (mat_ws @ Vector((bb[3][0], bb[3][1], bb[3][2]))) + Vector((-norm,  norm, -norm)) * scalar
    p5 = (mat_ws @ Vector((bb[4][0], bb[4][1], bb[4][2]))) + Vector(( norm, -norm, -norm)) * scalar
    p6 = (mat_ws @ Vector((bb[5][0], bb[5][1], bb[5][2]))) + Vector(( norm, -norm,  norm)) * scalar
    p7 = (mat_ws @ Vector((bb[6][0], bb[6][1], bb[6][2]))) + Vector(( norm,  norm,  norm)) * scalar
    p8 = (mat_ws @ Vector((bb[7][0], bb[7][1], bb[7][2]))) + Vector(( norm,  norm, -norm)) * scalar
    points = [p1, p2, p3, p4, p5, p6, p7, p8]
    lines = [
        p2, p3, p3, p7, p7, p6, p6, p2, # Top
        p1, p4, p4, p8, p8, p5, p5, p1, # Bottom
        p5, p6, p6, p7, p7, p8, p8, p5, # Right
        p1, p2, p2, p3, p3, p4, p4, p1, # Left
        p1, p2, p2, p6, p6, p5, p5, p1, # Front
        p4, p3, p3, p7, p7, p8, p8, p4] # Back
    return points, lines
