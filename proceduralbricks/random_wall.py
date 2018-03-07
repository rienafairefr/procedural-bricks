from random import choice, random

from constants import *
from element import Element, ElementGroup, Connections, get_points, parts as ldrawparts, get_bounding_box

WallColors = list(AllColors)
WallColors.remove(Colors.Red)
WallColors.remove(Colors.Purple)

parts = [
    Brick1X1, Brick1X2, Brick1X3, Brick1X4,
    # Brick2X2, Brick2X3, Brick2X4,
    Brick2X2,
    Brick1X1X3,
    SlopeBrick752X2X3WithHollowStuds,
    SlopeBrick452X1Inverted,
    SlopeBrick452X2Inverted,
    SlopeBrick752X1X3Inverted,
]


def get_width(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int((bb.max - bb.min).x)


def get_depth(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int((bb.max - bb.min).z)


def get_height(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int((bb.max - bb.min).y)


def get_z_offset(code):
    bb = get_bounding_box(get_points(ldrawparts.part(code=code)))
    return int(bb.max.z)


widths = {code: get_width(code) / 20 for code in parts}
depths = {code: get_depth(code) / 20.0 for code in parts}
heights = {code: (get_height(code) - 4) / 24 for code in parts}
z_offsets = {code: get_z_offset(code) / 20.0 for code in parts}

max_x = 20
max_y = 20

current_height = [0] * (max_x)
top_part = {}


def ldux(stud):
    return stud * 20


def lduy(brickheight):
    return - brickheight * 24


lduz = ldux


def ldu(pos):
    return ldux(pos[0]), lduy(pos[1]), lduz(pos[2])


class RandomWall(ElementGroup):
    def __init__(self, pos, pos_b, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        x = 0
        y = 0
        z = 0

        while True:
            if all(h == max_y for h in current_height):
                break

            y = current_height[x]

            for xi in range(0, max_x, 1):
                if current_height[xi] < y:
                    x = xi
                    y = current_height[xi]
                    break

            part = choice(parts)

            width = widths[part]
            height = heights[part]
            depth = depths[part]

            if x == 0:
                color = Colors.Red
            else:
                color = choice(WallColors)

            x_element = x
            y_element = y
            z_offset = -z_offsets[part]
            pos_element = (x_element + width / 2.0, y_element + height, z_offset)

            element = Element(ldu(pos_element), facing, part=part, color=color)

            if x + width <= max_x:
                if x + width == max_x:
                    element.color = Colors.Purple
                    x = 0
                else:
                    x = x + width

                fits = True
                for xi in range(x_element, x_element + width, 1):
                    if current_height[xi] > y_element:
                        fits = False
                    if current_height[xi] + height > max_y:
                        fits = False

                if fits:
                    for xi in range(x_element, x_element + width, 1):
                        try:
                            current_height[xi] = y + height
                        except IndexError:
                            pass
                    self.append(element)
                    top_part[x] = part


if __name__ == '__main__':
    wall = RandomWall((0, 0, 0), (0, 0, 0))
    with open('random_wall.ldr', 'w') as out:
        out.write(wall.to_ldr())
