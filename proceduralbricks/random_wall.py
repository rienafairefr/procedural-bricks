from random import choice

from constants import *
from element import Element, ElementGroup, Connections

WallColors = list(Colors)
WallColors.remove(Colors.red)
WallColors.remove(Colors.purple)


class RandomWall(ElementGroup):
    def __init__(self, pos, pos_b, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        parts = [BRICK_1X1, BRICK_1X2, BRICK_1X3, BRICK_1X4, BRICK_2x2, BRICK_2x3, BRICK_2x4]

        widths = {BRICK_1X1: 20, BRICK_1X2: 40, BRICK_1X3: 60, BRICK_1X4: 80,
                  BRICK_2x2: 40, BRICK_2x3: 60, BRICK_2x4: 80}

        z_offsets = {BRICK_1X1: 0, BRICK_1X2: 0, BRICK_1X3: 0, BRICK_1X4: 0,
                  BRICK_2x2: -10, BRICK_2x3: -10, BRICK_2x4: -10}

        x = 0
        y = 0
        z = 0
        max_x = 500
        max_y = 500
        while y < max_y:
            part = choice(parts)
            width = widths[part]
            if x == 0:
                color = Colors.red
            else:
                color = choice(WallColors)

            element = Element((x + width / 2, y , z+z_offsets[part]), facing, part=part, color=color)

            if x + width <= max_x:
                if x + width == max_x:
                    element.color = Colors.purple
                    x = 0
                    y = y + 24
                else:
                    x = x + width
                if not self.collides_with(element):
                    self.append(element)
                continue


if __name__ == '__main__':
    wall = RandomWall((0, 0, 0), (0, 0, 0))
    with open('random_wall.ldr', 'w') as out:
        out.write(wall.to_ldr())
