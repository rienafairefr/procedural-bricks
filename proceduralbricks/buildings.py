from random import random

from ldraw.library.parts.others import Door1X4X6Frame

from proceduralbricks.constants import Facing, BRICK_EVEN, BRICK_ODD, Window1X2X2, Colors, Door1X4X6With4Panes, \
    Glass1X4X6, brick_height, stud
from proceduralbricks.element import Element, ElementGroup, Connections
from proceduralbricks.walls import Wall


class WindowWall(ElementGroup):
    def __init__(self, start, width, facing=Facing.FRONT, connections=Connections(), cls_wall=Wall):
        ElementGroup.__init__(self, start, facing, connections=connections)

        self.append(cls_wall((start[0], start[1], start[2]), (start[0] + 40, start[1] + 6 * 24, start[2]),
                             connections=Connections(left=connections.left)))

        last_solid = True
        x = 40
        while x < start[facing.x] + width * 40 - 40:
            if last_solid:
                last_solid = False
                if random() > .5:
                    # Door
                    self.append(Element((start[0] + x + 40, start[1], start[2] + 10), facing, part=Door1X4X6Frame,
                                        color=Colors.Tan))
                    if random() > .5:
                        self.append(
                            Element((start[0] + x + 20 - 12, start[1], start[2] + 10), facing, part=Door1X4X6With4Panes,
                                    color=Colors.Black))
                    else:
                        self.append(Element((start[0] + x + 40, start[1] + 4, start[2] + 10), facing, part=Glass1X4X6,
                                            color=Colors.Trans_Clear))
                else:
                    self.append(cls_wall((start[0] + x, start[1] + 4 * 24, start[2]),
                                         (start[0] + x + 80, start[1] + 6 * 24, start[2])))
                    for wx in [start[0] + x + 20, start[0] + x + 60]:
                        for wy in [start[1], start[1] + 48]:
                            self.append(Element((wx, wy, start[2] + 10), facing, part=Window1X2X2, color=Colors.Tan))
                x += 80
            else:
                last_solid = True
                self.append(Wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2])))
                x += 40

        self.append(cls_wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2]),
                             connections=Connections(right=connections.right)))


class WallBox(ElementGroup):
    def __init__(self, a, b, cls_wall=Wall, front=True, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, a, facing, pos_b=b, connections=connections)

        if front:
            self.append(cls_wall(a, (b[0], b[1], a[2]),
                                 facing=Facing.FRONT,
                                 connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
        self.append(cls_wall(a, (a[0], b[1], b[2]),
                             facing=Facing.LEFT,
                             connections=Connections(left=BRICK_ODD, right=BRICK_ODD)))
        self.append(cls_wall((a[0], a[1], b[2] - 20), (b[0], b[1], b[2] - 20),
                             facing=Facing.BACK,
                             connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
        self.append(cls_wall((b[0] - 20, a[1], a[2]), (b[0] - 20, b[1], b[2]),
                             facing=Facing.RIGHT,
                             connections=Connections(left=BRICK_ODD, right=BRICK_ODD)))


class ModularBuilding(ElementGroup):
    def __init__(self, cls_Wall=Wall, width=31, height=64, depth=8):
        ElementGroup.__init__(self, (0, 0, 0), Facing.FRONT)

        for y in range(0, height * brick_height, 8 * brick_height):
            self.append(WallBox((0, y, 0), (width * 2 * stud, y + brick_height * 8, stud * 2 * depth),
                                front=False,
                                cls_wall=cls_Wall))

            self.append(
                cls_Wall((0, y, 0), (width * 2 * stud, y + brick_height * 2, 0),
                         connections=Connections(left=BRICK_EVEN,
                                                 right=BRICK_EVEN)))
            self.append(WindowWall((0, y + 24 * 2, 0), width,
                                   cls_wall=cls_Wall,
                                   connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
