"""
The structure is broken down recursively into interconnected subgroups.
"""

from random import random

from constants import *
from element import Element, ElementGroup, Connections

class WindowWall(ElementGroup):
  def __init__(self, start, width, facing = Facing.FRONT, connections=Connections()):
    ElementGroup.__init__(self, start, facing, connections=connections)

    self.append(Wall((start[0], start[1], start[2]), (start[0] + 40, start[1] + 6 * 24, start[2]), connections=Connections(left=connections.left)))
  
    last_solid = True
    x = 40
    while x < start[facing.x] + width * 40 - 40:
      if last_solid:
        last_solid = False
        if random() > .5:
          # Door
          self.append(Element((start[0] + x + 40, start[1], start[2] + 10), facing, part=DOOR_1X4X6_FRAME, color = TAN))
          if random() > .5:
            self.append(Element((start[0] + x + 20 - 12, start[1], start[2] + 10), facing, part=DOOR_1X4X6_4_PANE, color=BLACK))
          else:
            self.append(Element((start[0] + x + 40, start[1] + 4, start[2] + 10), facing,part=GLASS_1X4X6, color=TRANS_CLEAR))
        else:
          self.append(Wall((start[0] + x, start[1] + 4 * 24, start[2]), (start[0] + x + 80, start[1] + 6 * 24, start[2])))
          self.append(Element((start[0] + x + 20, start[1], start[2] + 10), facing,part=WINDOW_1X2X2, color=TAN))
          self.append(Element((start[0] + x + 20 + 40, start[1], start[2] + 10), facing,part=WINDOW_1X2X2, color=TAN))
          self.append(Element((start[0] + x + 20, start[1] + 48, start[2] + 10), facing,part=WINDOW_1X2X2, color=TAN))
          self.append(Element((start[0] + x + 20 + 40, start[1] + 48, start[2] + 10), facing,part=WINDOW_1X2X2, color=TAN))
        x += 80
      else:
        last_solid = True
        self.append(Wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2])))
        x += 40
  
    self.append(Wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2]), connections=Connections(right=connections.right)))

class Wall(ElementGroup):
  def __init__(self, pos, pos_b, facing = Facing.FRONT, connections=Connections()):
    ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

    pos = self.relative_pos(pos)
    pos_b = self.relative_pos(pos_b)

    for x in range(pos[0],pos_b[0],20*2):
      for y in range(pos[1],pos_b[1],24):
        offset = 20
        part = BRICK_1X2

        if connections.left and (y / 24) % 2 == int(connections.left != BRICK_EVEN):
          offset = 40
          if x == pos_b[0] - 40:
            if connections.right:
              continue
            else:
              offset = 30
              part = BRICK_1X1

        last_one = (abs(pos_b[0] - pos[0]) == 40)
  
        if last_one and connections.right and (y / 24) % 2 == int(connections.right != BRICK_EVEN):
          offset = 10
          part = BRICK_1X1 

        self.append(Element((x + offset,y,10 + pos[2]), facing, part=part, color=SAND_BLUE))

def el_to_line(el):
  if type(el) == tuple:
    if el[3] == Facing.LEFT:
      orientation = "0 0 1 0 1 0 -1 0 0"
    if el[3] == Facing.BACK:
      orientation = "-1 0 0 0 1 0 0 0 -1"
    if el[3] == Facing.FRONT:
      orientation = "1 0 0 0 1 0 0 0 1"
    if el[3] == Facing.RIGHT:
      orientation = "-0 0 -1 0 1 0 1 0 0"
  
    return "1 %d %d %d %d %s %s.dat" % (el[2], el[0][0], el[0][1], el[0][2], orientation, el[1])
  else:
    return el.to_ldr()

def as_ldr(els):
  lines = [el_to_line(e) for e in els]

  return '\n'.join(lines)

class WallBox(ElementGroup):
  def __init__(self, a, b, front=True, facing = Facing.FRONT, connections=Connections()):
    ElementGroup.__init__(self, a, facing, pos_b=b, connections=connections)

    if front:
      self.append(Wall(a,(b[0],b[1],a[2]), facing=Facing.FRONT, connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
    self.append(Wall(a,(a[0],b[1],b[2]), facing=Facing.LEFT, connections=Connections(left=BRICK_ODD, right=BRICK_ODD)))
    self.append(Wall((a[0],a[1],b[2] - 20),(b[0],b[1],b[2] - 20), facing=Facing.BACK, connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
    self.append(Wall((b[0] - 20,a[1],a[2]),(b[0] - 20,b[1],b[2]), facing=Facing.RIGHT, connections=Connections(left=BRICK_ODD, right=BRICK_ODD)))

def modular_building():
  els = []
  
  for y in range (0,8*8 * 24,8*24):
    els += [WallBox((0,y,0), (31 * 40, y + 24 * 8, 20 * 16), front=False)]

    els += [Wall((0,y,0), (31 * 40,y + 24 * 2, 0), connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN))]
    els += [WindowWall((0,y + 24 * 2,0), 31, connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN))]

  return els
    

def main():
  with open('test.ldr', 'w') as out:
    out.write(as_ldr(modular_building()))

if __name__ == '__main__':
  main()