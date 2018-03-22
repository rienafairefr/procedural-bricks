from ldraw.library.parts.others import Brick1X2, Brick1X1

from proceduralbricks.constants import Facing, stud, brick_height, BRICK_EVEN, Colors
from proceduralbricks.element import ElementGroup, Connections, Element


class Wall(ElementGroup):
    def __init__(self, pos, pos_b, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        pos = self.relative_pos(pos)
        pos_b = self.relative_pos(pos_b)

        for x in range(pos[0], pos_b[0], 20 * 2):
            for y in range(pos[1], pos_b[1], 24):
                offset = 20
                part = Brick1X2

                if connections.left and (y / 24) % 2 == int(connections.left != BRICK_EVEN):
                    offset = 40
                    if x == pos_b[0] - 40:
                        if connections.right:
                            continue
                        else:
                            offset = 30
                            part = Brick1X1

                last_one = (abs(pos_b[0] - pos[0]) == 40)

                if last_one and connections.right and (y / 24) % 2 == int(connections.right != BRICK_EVEN):
                    offset = 10
                    part = Brick1X1

                self.append(Element((x + offset, y, 10 + pos[2]), facing, part=part, color=Colors.Sand_Blue))


class CWall(ElementGroup):
    def __init__(self, pos, pos_b, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        pos = self.relative_pos(pos)
        pos_b = self.relative_pos(pos_b)

        for x in range(pos[0], pos_b[0], 20 * 2):
            for y in range(pos[1], pos_b[1], 24):
                color = Colors.Tan
                offset = 20
                part = Brick1X2

                if connections.left and (y / 24) % 2 == int(connections.left != BRICK_EVEN):
                    offset = 40
                    if x == pos_b[0] - 40:
                        if connections.right:
                            continue
                        else:
                            color = Colors.Green
                            offset = 30
                            part = Brick1X1

                last_one = (abs(pos_b[0] - pos[0]) == 40)

                if last_one and connections.right and (y / 24) % 2 == int(connections.right != BRICK_EVEN):
                    color = Colors.Red
                    offset = 10
                    part = Brick1X1

                self.append(Element((x + offset, y, 10 + pos[2]), facing, part=part, color=Colors.Sand_Blue))