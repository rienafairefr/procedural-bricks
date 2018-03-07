from random import choice

from constants import *
from element import Element, ElementGroup, Connections, get_points, parts as ldrawparts, get_bounding_box

WallColors = list(AllColors)
WallColors.remove(Colors.Red)
WallColors.remove(Colors.Purple)

parts = [Brick1X1, Brick1X2, Brick1X3, Brick1X4, Brick2X2, Brick2X3, Brick2X4, Brick1X1X3]


def get_width(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int((bb.max-bb.min).x)


def get_depth(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int((bb.max-bb.min).z)


def get_height(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int((bb.max-bb.min).y)


widths = {code:get_width(code) for code in parts}

z_offsets = {code:(20-get_depth(code))/2 for code in parts}

heights = {code:get_height(code)-4 for code in parts}

current_height = {}

class RandomWall(ElementGroup):
    def __init__(self, pos, pos_b, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        x = 0
        y = 0
        z = 0
        max_x = 500
        max_y = 60
        while y < max_y:
            y = current_height.get(x, 0)
            part = choice(parts)
            width = widths[part]
            if x == 0:
                color = Colors.Red
            else:
                color = choice(WallColors)

            element = Element((x + width / 2, y, z+z_offsets[part]), facing, part=part, color=color)

            if x + width <= max_x:
                if x + width == max_x:
                    element.color = Colors.Purple
                    x = 0
                else:
                    x = x + width
                if not self.collides_with(element):
                    for pos_x in range(x-width, x, 20):
                        current_height[pos_x] = current_height.get(pos_x, 0) + heights[part]
                    self.append(element)
                continue


if __name__ == '__main__':
    wall = RandomWall((0, 0, 0), (0, 0, 0))
    with open('random_wall.ldr', 'w') as out:
        out.write(wall.to_ldr())
