from ldraw.geometry import Vector
from ldraw.lines import MetaCommand
from ldraw.parts import Parts
from ldraw.config import get_config
from ldraw.pieces import Piece

from constants import *

config = get_config()

parts = Parts(config['parts.lst'])


class Connections:
    def __init__(self, top=None, bottom=None, left=None, right=None, front=None, back=None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.front = front
        self.back = back


class BoudingBox(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __add__(self, other):
        if isinstance(other, Vector):
            self.min = self.min + other
            self.max = self.max + other
            return self
        raise ValueError('Can only add a Vector to a BoundingBox')


def get_bounding_box(points):
    return BoudingBox(Vector(min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)),
                      Vector(max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)),
                      )


def bounding_boxes_collide(box1, box2):
    return (box1.max.x > box2.min.x and
            box1.min.x < box2.max.x and
            box1.max.y > box2.min.y and
            box1.min.y < box2.max.y and
            box1.max.z > box2.min.z and
            box1.min.z < box2.max.z)


def get_points(part):
    returnvalue = []
    for line in part.objects:
        if not isinstance(line, MetaCommand):
            for i in range(1, 5):
                attr = 'point%i' % i
                val = getattr(line, attr, None)
                if val:
                    returnvalue.append(val)
        if isinstance(line, Piece):
            subpart = parts.part(code=line.part)
            subpoints = get_points(subpart)
            subpoints = [line.matrix * p + line.position for p in subpoints]
            returnvalue.extend(subpoints)
    return returnvalue


def get_width_ldu(code):
    bb = get_bounding_box(get_points(parts.part(code=code)))
    return int((bb.max - bb.min).x)


def get_depth_ldu(code):
    bb = get_bounding_box(get_points(parts.part(code=code)))
    return int((bb.max - bb.min).z)


def get_height_ldu(code):
    bb = get_bounding_box(get_points(parts.part(code=code)))
    return int((bb.max - bb.min).y)


def get_z_offset_ldu(code):
    bb = get_bounding_box(get_points(parts.part(code=code)))
    return int(bb.max.z)


def get_z_offset(code):
    return get_z_offset_ldu(code) / 24


def get_width(code):
    return get_width_ldu(code) / 20


def get_depth(code):
    return get_depth_ldu(code) / 20


def get_height(code):
    return get_height_ldu(code) / 24


def ldux(stud):
    return stud * 20


def lduy(brickheight):
    return - brickheight * 24


lduz = ldux


def ldu(pos):
    return ldux(pos[0]), lduy(pos[1]), lduz(pos[2])


class Element:
    def __init__(self, pos, facing=Facing.FRONT, part=Brick1X2, color=Colors.Black, pos_b=None,
                 connections=Connections()):
        self.pos = pos
        self.facing = facing
        self.connections = connections
        self.part = part
        self.color = color

    def to_ldr(self):
        if self.facing == Facing.FRONT:
            orientation = "1 0 0 0 1 0 0 0 1"
        elif self.facing == Facing.BACK:
            orientation = "-1 0 0 0 1 0 0 0 -1"
        elif self.facing == Facing.LEFT:
            orientation = "0 0 1 0 1 0 -1 0 0"
        elif self.facing == Facing.RIGHT:
            orientation = "0 0 -1 0 1 0 1 0 0"
        else:
            pass

        return ("1 %d %d %d %d %s %s.dat" % (
            self.color.code, self.pos[0], self.pos[1], self.pos[2], orientation, self.part))

    def collides_with(self, other):
        bb1 = get_bounding_box(get_points(parts.part(code=self.part))) + Vector(*tuple(self.pos))
        bb2 = get_bounding_box(get_points(parts.part(code=other.part))) + Vector(*tuple(other.pos))
        return bounding_boxes_collide(bb1, bb2)


class ElementGroup:
    def __init__(self, pos, facing, pos_b=None, connections=Connections()):
        self.pos = pos
        self.pos_b = pos_b
        self.facing = facing
        self.connections = connections
        self.children = []

    def relative_pos(self, v):
        ret = [0, 0, 0]

        ret[self.facing.x] = v[0]
        ret[self.facing.y] = v[1]
        ret[self.facing.z] = v[2]

        return ret

    def append(self, child):
        child.pos = self.relative_pos(child.pos)

        self.children.append(child)

    def to_ldr(self):
        return ('\n'.join([c.to_ldr() for c in self.children]))

    def collides_with(self, element):
        for child in self.children:
            if child.collides_with(element):
                return True
        return False
