import random

import sys

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

    SlopeBrick452X2Inverted,
    SlopeBrick452X2
]

parts_dict = {c: ldrawparts.part(code=c) for c in set(parts)}

depth1 = [Brick1X1, Brick1X2, Brick1X3, Brick1X4, Brick1X1X3]
accepts_depth1 = [Brick1X1, Brick1X2, Brick1X3, Brick1X4, SlopeBrick452X2Inverted, Brick1X1X3]

accepts = {
    Brick2X2: [Brick2X2, SlopeBrick752X2X3WithHollowStuds, SlopeBrick452X2],
    Brick1X1X3: [Brick1X1, Brick1X1X3],
    SlopeBrick752X2X3WithHollowStuds: depth1,
    SlopeBrick452X2Inverted: [Brick2X2, SlopeBrick752X2X3WithHollowStuds, SlopeBrick452X2],
    SlopeBrick452X2: depth1
}
for brick1 in depth1:
    accepts[brick1] = accepts_depth1

accepted_on = {
    SlopeBrick452X2Inverted: [Brick1X2, Brick1X3, Brick1X4]
}


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

n_x = 10
n_y = 10




def ldux(stud):
    return stud * 20


def lduy(brickheight):
    return - brickheight * 24


lduz = ldux

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
print("Seed was:", seed)


def ldu(pos):
    return ldux(pos[0]), lduy(pos[1]), lduz(pos[2])


class RandomWall(ElementGroup):
    def __init__(self, pos, pos_b, facing=Facing.FRONT, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        x = 0
        y = 0
        z = 0

        nfails = 0
        self.current_height = [0] * (n_x)
        self.top_part = {}

        while True:
            if all(h == n_y for h in self.current_height):
                break

            def try_place(x, part):

                y = self.current_height[x]
                current_top_part = self.top_part.get(x)
                print((x, y))
                print('trying placing %s' % (ldrawparts.parts_by_code[part],))

                width = widths[part]
                height = heights[part]

                if self.current_height[x] == n_y:
                    if x >= n_x:
                        return 0
                    else:
                        return x+1
                for xi in range(x, min(n_x, x + width), 1):
                    if self.current_height[xi] < y:
                        print('overhang')
                        return None

                if x == 0:
                    color = Colors.Red
                else:
                    color = random.choice(WallColors)

                x_element = x
                y_element = y
                z_offset = -z_offsets[part]
                pos_element = (x_element + width / 2.0, y_element + height, z_offset)

                element = Element(ldu(pos_element), facing, part=part, color=color)

                if x + width <= n_x:
                    if x + width == n_x:
                        print('end of the line')
                        element.color = Colors.Purple
                        x = 0
                    else:
                        x = x + width

                    fits = True
                    for xi in range(x_element, x_element + width, 1):
                        if xi >= n_x:
                            fits = False
                        if self.current_height[xi] > y_element:
                            fits = False
                        if self.current_height[xi] + height > n_y:
                            fits = False

                    if fits:
                        if current_top_part is not None:
                            accepted = accepts.get(current_top_part)
                            if accepted is not None and part not in accepted:
                                print('not accepted')
                                return

                        print('placing %s (%i %i)' % (ldrawparts.parts_by_code[part], x_element, y_element))
                        for xi in range(x_element, x_element + width, 1):
                            try:
                                self.current_height[xi] = y + height
                            except IndexError:
                                pass
                            self.top_part[xi] = part
                        self.append(element)
                        return x
                    else:
                        print('doesnt fit')
                        return
                else:
                    print('too wide')
                    return

            result = try_place(x, random.choice(parts))
            if result is None:
                nfails += 1
            else:
                x = result
            if nfails > 5:
                all_fail = True
                for part in parts:
                    result = try_place(x, part)
                    if result is not None:
                        all_fail = False
                        x = result
                        break
                if all_fail:

                    for part in parts:
                        result = try_place(x, part)

                    print('Aborting after failing to place anything')
                    break


if __name__ == '__main__':
    wall = RandomWall((0, 0, 0), (0, 0, 0))
    with open('random_wall.ldr', 'w') as out:
        out.write(wall.to_ldr())
